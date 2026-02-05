import os
import argparse
from datetime import datetime

import googleapiclient.discovery
import googleapiclient.errors

from dotenv import load_dotenv


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class YouTube:

    def __init__(self, developer_key):
        self.developer_key = developer_key
        self._api = None

    @property
    def api(self):
        if not self._api:
            self._api = googleapiclient.discovery.build("youtube", "v3", developerKey=self.developer_key)
        return self._api


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class VideoStats:

    _date_format_ = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, published_at: str,
                       comments: str,
                       favorites: str,
                       likes: str,
                       views: str):

        self.published_at = published_at
        self.comments = int(comments)
        self.favorites = int(favorites)
        self.likes = int(likes)
        self.views = int(views)

        self._age_days = None

        self._views_per_day = None
        self._likes_per_day = None
        self._comments_per_day = None

        self._likestoviews_ratio = None
        self._commentstoviews_ratio = None
        self._viewstolikes_ratio = None
        self._viewstocomments_ratio = None

    @property
    def age_days(self):
        if not self._age_days:
            pa_dt = datetime.strptime(self.published_at, type(self)._date_format_)
            ago_td = datetime.now() - pa_dt
            self._age_days = ago_td.days
        return self._age_days

    #
    @property
    def views_per_day(self):
        if not self._views_per_day:
            self._views_per_day = round(self.views / self.age_days)
        return self._views_per_day

    @property
    def likes_per_day(self):
        if not self._likes_per_day:
            self._likes_per_day = round(self.likes / self.age_days)
        return self._likes_per_day

    @property
    def comments_per_day(self):
        if not self._comments_per_day:
            self._comments_per_day = round(self.comments / self.age_days)
        return self._comments_per_day

    #
    @property
    def likestoviews_ratio(self):
        if not self._likestoviews_ratio:
            self._likestoviews_ratio = self.likes / self.views
        return self._likestoviews_ratio

    @property
    def commentstoviews_ratio(self):
        if not self._commentstoviews_ratio:
            self._commentstoviews_ratio = self.comments / self.views
        return self._commentstoviews_ratio

    @property
    def viewstolikes_ratio(self):
        if not self._viewstolikes_ratio:
            self._viewstolikes_ratio = 1 / self.likestoviews_ratio
        return self._viewstolikes_ratio

    @property
    def viewstocomments_ratio(self):
        if not self._viewstocomments_ratio:
            self._viewstocomments_ratio = 1 / self.commentstoviews_ratio
        return self._viewstocomments_ratio



class Video:

    def __init__(self, viddata_item: dict):
        self.id = viddata_item['id']
        self.title = viddata_item['snippet']['title']

        self.stats = VideoStats(published_at=viddata_item['snippet']['publishedAt'],
                                comments=viddata_item['statistics']['commentCount'],
                                favorites=viddata_item['statistics']['favoriteCount'],
                                likes=viddata_item['statistics']['likeCount'],
                                views=viddata_item['statistics']['viewCount'])



class VideoDataFetcher:

    _part_ = "snippet,statistics"

    def __init__(self, yt_api):
        self.yt_api = yt_api

    def fetch(self, video_ids: list):
        # [https://developers.google.com/youtube/v3/docs/videos/list]
        videos_request = self.yt_api.videos().list(
            part=type(self)._part_,
            # maxResults=50,  # "not supported for use in conjunction with id"  # TODO no to przetestować na >50
            id=video_ids
        )
        return videos_request.execute()



class VideoStatsFormatter:

    _col_labels_ = ('[ID]       ',  # -
                    'publAtDate',
                    'daysOld',  # |
                    'viewsCt',
                    'likesCt',
                    'commsCt',  # |
                    'views/d',
                    'likes/d',
                    'comms/d',  # |
                    'views4like',
                    'views4comm',  # ->
                    '[TITLE]')
    _row_template_ = '  {}  -  {}  {}  |  {}   {}   {}  |  {}   {}   {}  |  {}   {}  ->  {}'

    def __init__(self, videos: list):
        self.videos = videos
        self.col_lens = [len(c) for c in type(self)._col_labels_]

    def print(self):
        print(type(self)._row_template_.format(*type(self)._col_labels_))
        for video in self.videos:
            row_items = [video.id.rjust(self.col_lens[0]),
                         str(video.stats.published_at).split('T')[0].rjust(self.col_lens[1]),
                         str(video.stats.age_days).rjust(self.col_lens[2]),
                         str(video.stats.views).rjust(self.col_lens[3]),
                         str(video.stats.likes).rjust(self.col_lens[4]),
                         str(video.stats.comments).rjust(self.col_lens[5]),
                         str(video.stats.views_per_day).rjust(self.col_lens[6]),
                         str(video.stats.likes_per_day).rjust(self.col_lens[7]),
                         str(video.stats.comments_per_day).rjust(self.col_lens[8]),
                         str(int(video.stats.viewstolikes_ratio)).rjust(self.col_lens[9]),
                         str(int(video.stats.viewstocomments_ratio)).rjust(self.col_lens[10]),
                         video.title.rjust(self.col_lens[11])]
            print(type(self)._row_template_.format(*row_items))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Playlist:

    def __init__(self, pldata_elem, plcontent_elem):
        self.plcontent_elem = plcontent_elem

        self.id = pldata_elem['id']
        self.title = pldata_elem['snippet']['title']

        self.publishedAt = pldata_elem['snippet']['publishedAt']
        self.channelId = pldata_elem['snippet']['channelId']
        self.channelTitle = pldata_elem['snippet']['channelTitle']

        self._videos = []

    @property
    def videos(self):
        if not self._videos:
            for content_item in self.plcontent_elem['items']:
                self._videos.append(content_item['contentDetails']['videoId'])
        return self._videos

    def __str__(self):
        return (f'PLAYLIST: {self.id}  ->  "{self.title}"{os.linesep}'
                f'[channel: {self.channelId} / "{self.channelTitle}"]')


class PlaylistFetcher:

    _part_data_ = "snippet,status"
    _part_content_ = "contentDetails,status"

    def __init__(self, yt_api):
        self.yt_api = yt_api

    def fetch(self, playlist_id: str):
        """
        :param playlist_id: this is required (and assumed) to always be a single playlist ID
        """
        # base data
        # [https://developers.google.com/youtube/v3/docs/playlists/list]
        plbdata_request = self.yt_api.playlists().list(
            part=type(self)._part_data_,
            # maxResults=50,  # always one requested
            id=playlist_id
        )
        plbdata_response = plbdata_request.execute()

        # content
        # [https://developers.google.com/youtube/v3/docs/playlistItems/list]
        plcontent_request = self.yt_api.playlistItems().list(
            part=type(self)._part_content_,
            maxResults=50,  # TODO tu serio mamy takie ograniczenie?
            playlistId=playlist_id  # only a single ID is accepted
        )
        plitems_response = plcontent_request.execute()

        return plbdata_response['items'][0], plitems_response  # unwrap first data item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Channel:

    _date_format_ = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, chdata_elem, chcontent_elem):
        self.chcontent_elem = chcontent_elem

        self.id = chdata_elem['id']
        self.title = chdata_elem['snippet']['title']
        self.country = chdata_elem['snippet']['country']
        self.published_at = chdata_elem['snippet']['publishedAt']

        self.uploads_pl = chdata_elem['contentDetails']['relatedPlaylists']['uploads']

        self.subscriber_count = int(chdata_elem['statistics']['subscriberCount'])
        self.video_count = int(chdata_elem['statistics']['videoCount'])

        self._age_days = None
        self._subs_per_day = None
        self._videos_per_month = None

        self._playlists = []

    @property
    def age_days(self):
        if not self._age_days:
            pa_dt = datetime.strptime(self.published_at, type(self)._date_format_)
            ago_td = datetime.now() - pa_dt
            self._age_days = ago_td.days
        return self._age_days

    @property
    def subs_per_day(self):
        if not self._subs_per_day:
            self._subs_per_day = round(self.subscriber_count / self.age_days)
        return self._subs_per_day

    @property
    def videos_per_month(self):
        if not self._videos_per_month:
            self._videos_per_month = round(self.video_count / (self.age_days / 30))
        return self._videos_per_month

    @property
    def playlists(self):
        if not self._playlists:
            for content_item in self.chcontent_elem['items']:
                self._playlists.append((content_item['id'],
                                        content_item['snippet']['publishedAt'],
                                        content_item['snippet']['title']))
        return self._playlists

    def __str__(self):
        head = (f'  CHANNEL: /{self.country.lower()}/ {self.id}  ->  "{self.title}"{os.linesep}'
                f'   since : {self.published_at.split("T")[0]} ({self.age_days} days ago){os.linesep}'
                f'   vids  : {self.video_count}        ({self.videos_per_month}/month){os.linesep}'
                f'   subs  : {self.subscriber_count}     ({self.subs_per_day}/day){os.linesep}'
                f'{os.linesep}'
                f'  Uploads:   {self.uploads_pl}'
                f'{os.linesep}'
                f'  Playlists:')
        lists = os.linesep.join([f'   {plist[0]}  (cr:{plist[1].split("T")[0]})  ->  {plist[2]}' for plist in self.playlists])
        return os.linesep.join([head, lists])


class ChannelFetcher:

    _part_data_ = "brandingSettings,contentDetails,snippet,status,statistics"
    _part_content_ = "snippet,status"

    def __init__(self, yt_api):
        self.yt_api = yt_api

    def fetch(self, channel_id: str):
        """
        :param channel_id: this is required (and assumed) to always be a single channel ID
        """
        # base data
        # [https://developers.google.com/youtube/v3/docs/channels/list]
        chbdata_request = self.yt_api.channels().list(
            part=type(self)._part_data_,
            # maxResults=50,  # always one requested
            id=channel_id
        )
        chbdata_response = chbdata_request.execute()

        # content
        # [https://developers.google.com/youtube/v3/docs/playlists/list]
        chcontent_request = self.yt_api.playlists().list(
            part=type(self)._part_content_,
            maxResults=50,  # TODO tu serio mamy takie ograniczenie?
            channelId=channel_id  # only a single ID is accepted
        )
        chitems_response = chcontent_request.execute()

        return chbdata_response['items'][0], chitems_response  # unwrap first data item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def serve_videos_stats(youtube_, vid_ids_: list):
    video_data = VideoDataFetcher(youtube_.api).fetch(vid_ids_)
    VideoStatsFormatter([Video(videodata_item) for videodata_item in video_data['items']]).print()


def serve_playlist_stats(youtube_, pl_id_: str):
    playlist_data = PlaylistFetcher(youtube_.api).fetch(pl_id_)
    playlist_ = Playlist(*playlist_data)
    video_data = VideoDataFetcher(youtube_.api).fetch(playlist_.videos)

    print(playlist_)
    print(f'{os.linesep}Videos:')
    VideoStatsFormatter([Video(videodata_item) for videodata_item in video_data['items']]).print()


def serve_channel_stats(youtube_, ch_id_: str):
    channel_data = ChannelFetcher(youtube_.api).fetch(ch_id_)
    print(Channel(*channel_data))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':

    print()
    # ----------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Basic statistics of a YouTube video(s)/playlist(s)/channel(s).')

    parser.add_argument('-v',
                        type=str,
                        action='append',
                        metavar='VIDEO_ID',
                        help='add a video id')
    parser.add_argument('-p',
                        type=str,
                        action='append',
                        metavar='PLAYLIST_ID',
                        help='add a playlist id')
    parser.add_argument('-c',
                        type=str,
                        action='append',
                        metavar='CHANNEL_ID',
                        help='add a channel id')

    args = parser.parse_args()

    arg_videos = args.v
    arg_playlists = args.p
    arg_channels = args.c

    if not (arg_videos or arg_playlists or arg_channels):
        parser.error('No resource requested, add -v or -p or -c (or -h for more info).')
    # ----------------------------------------------------------------------------------

    load_dotenv()
    api_key = os.getenv('VINTURAE_YOUTUBE_API_KEY')
    if not api_key:
        raise ValueError("VINTURAE_YOUTUBE_API_KEY not found in .env file or environment variables. Please set it.")

    youtube = YouTube(api_key)

    if arg_videos:
        serve_videos_stats(youtube, arg_videos)

    if arg_playlists:
        for pl_id in arg_playlists:
            serve_playlist_stats(youtube, pl_id)

    if arg_channels:
        for ch_id in arg_channels:
            serve_channel_stats(youtube, ch_id)

    print()
