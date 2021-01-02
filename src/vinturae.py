#!/usr/bin/env python3

import os
import configparser

import argparse

import googleapiclient.discovery
import googleapiclient.errors

from colorama import Fore
from colorama import Style
from colorama import init as colorama_init
from colorama import deinit as colorama_deinit


from herbata import refine_videos_response
from herbata import refine_playlistitems_response
from herbata import refine_channel_playlists_response
from herbata import likes_percent


# VID_REGEX = r'[A-Za-z0-9_-]{11}'  # regex for video ID
# PLID_REGEX = r'[A-Za-z0-9_-]{34}'  # regex for playlist ID
# CHID_REGEX = r'[A-Za-z0-9_-]{24}'  # regex for channel ID


def format_vinfo(_vidstat, _like_prc, _votes_ttl, _focus=True, _indent=0):
    _id = _vidstat['id']
    _title = _vidstat['title']
    _views = int(_vidstat['viewCount'])
    _comms = int(_vidstat['commentCount'])
    idstr = white(f'{_id}') if _focus else f'{_id}'
    secondaryinfo = f'[ {_views:9} views , {_comms:7} comments]'
    infosection = f'{_votes_ttl:8} votes {dim(secondaryinfo)}'
    prcsection = f'{_like_prc:3}%'
    return f'{" "*_indent}{idstr} - {color_prc(prcsection, _like_prc, _votes_ttl)}   ({infosection})  ->  {_title}'


# -------------------------------------------------------------------
def crcwrap(_str, _color): return f'{_color}{_str}{Fore.RESET}'
def crswrap(_str, _style): return f'{_style}{_str}{Style.RESET_ALL}'
#
def red(_str): return crcwrap(_str, Fore.LIGHTRED_EX)
def green(_str): return crcwrap(_str, Fore.LIGHTGREEN_EX)
def yellow(_str): return crcwrap(_str, Fore.LIGHTYELLOW_EX)
def white(_str): return crcwrap(_str, Fore.LIGHTWHITE_EX)
def dim(_str): return crswrap(_str, Style.DIM)
#
def color_prc(_str, _prc, _votes):
    f = dim
    if _votes >= RELEVANCE_THR:
        f = red
        if _prc > SCORE_YELLOW_THR: f = yellow
        if _prc > SCORE_GREEN_THR: f = green
    return f(_str)
# -------------------------------------------------------------------


YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# -----------------------------------------------------------
cfg = configparser.ConfigParser()
cfg.read('config.ini')

DEVELOPER_KEY = cfg.get('creds', 'developer_key')

SCORE_YELLOW_THR = int(cfg.get('thresholds', 'score-yellow'))
SCORE_GREEN_THR = int(cfg.get('thresholds', 'score-green'))
RELEVANCE_THR = int(cfg.get('thresholds', 'relevance'))
# -----------------------------------------------------------


# --- videos stuff ----------------------------------------------
#
def retrieve_videos_stats(_youtube, _vid_ids):
    # https://developers.google.com/youtube/v3/docs/videos/list
    videos_request = _youtube.videos().list(
        part="snippet,statistics",
        # maxResults=50,  # "not supported for use in conjunction with id"
        id=_vid_ids
    )

    videos_response = videos_request.execute()
    return refine_videos_response(videos_response)


def parse_videos_stats(_videos_stats, _vfocus=True, _vindent=0):
    info = []

    for vidstat in _videos_stats:
        likes_prc, votes_ttl = likes_percent(vidstat)
        info.append(format_vinfo(vidstat, likes_prc, votes_ttl, _focus=_vfocus, _indent=_vindent))

    return info


def print_videos_stats(_info):
    print()
    for i in _info:
        print(i)
    print()
#
# ---------------------------------------------------------------


# --- playlist stuff --------------------------------------------
#
def retrieve_playlist_basedata(_youtube, _pl_id):
    # https://developers.google.com/youtube/v3/docs/playlists/list
    plbdata_request = _youtube.playlists().list(
        part="snippet,status",
        maxResults=50,
        id=_pl_id
    )

    plbdata_response = plbdata_request.execute()
    # assumption: a single playlist always requested, so one item returned
    pl_title = plbdata_response["items"][0]["snippet"]["title"]
    pl_privstatus = plbdata_response["items"][0]["status"]["privacyStatus"]
    return pl_title, pl_privstatus


def retrieve_plitems_stats(_youtube, _pl_id):
    # https://developers.google.com/youtube/v3/docs/playlistItems/list
    plitems_request = _youtube.playlistItems().list(
        part="contentDetails,status",
        maxResults=50,
        playlistId=_pl_id
    )

    plitems_response = plitems_request.execute()
    return refine_playlistitems_response(plitems_response)


def extract_plitems_ids(pl_items):
    return ','.join([x['videoId'] for x in pl_items])
#
# ---------------------------------------------------------------


# --- channel stuff ---------------------------------------------
#
def retrieve_channel_playlists(_youtube, _ch_id):
    # https://developers.google.com/youtube/v3/docs/playlists/list
    chpls_request = _youtube.playlists().list(
        part="snippet,status",
        maxResults=50,
        channelId=_ch_id
    )

    chpls_response = chpls_request.execute()
    return refine_channel_playlists_response(chpls_response)


def print_channel_playlists(_chpls_info):
    print()
    for i in _chpls_info:
        print(f"    {i['id']}  ->  {i['title']}")
    print()


def retrieve_channel_basedata(_youtube, _ch_id):
    # https://developers.google.com/youtube/v3/docs/channels/list
    chuppl_request = _youtube.channels().list(
        part="brandingSettings,contentDetails,status",
        maxResults=50,
        id=_ch_id
    )

    chuppl_response = chuppl_request.execute()
    # assumption: a single channel always requested, so one item returned
    uploads_plid = chuppl_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ch_title = chuppl_response["items"][0]["brandingSettings"]["channel"]["title"]
    return uploads_plid, ch_title
#
# ---------------------------------------------------------------


def print_videos_summary(_youtube, _vid_ids):
    videos_stats = retrieve_videos_stats(_youtube, _vid_ids)
    info = parse_videos_stats(videos_stats)
    print_videos_stats(info)


def print_playlist_summary(_youtube, _pl_id):
    pl_title, pl_privstatus = retrieve_playlist_basedata(_youtube, _pl_id)
    pl_items = retrieve_plitems_stats(_youtube, _pl_id)
    vid_ids = extract_plitems_ids(pl_items)
    videos_stats = retrieve_videos_stats(_youtube, vid_ids)
    info = parse_videos_stats(videos_stats, _vfocus=False, _vindent=4)
    print(f'{os.linesep}Playlist: {white(_pl_id)}  ->  {pl_title}')
    print(f'{os.linesep}Videos:')
    print_videos_stats(info)


def print_channel_summary(_youtube, _ch_id):
    uploads_plid, ch_title = retrieve_channel_basedata(_youtube, _ch_id)
    chpls_info = retrieve_channel_playlists(_youtube, _ch_id)

    print(f'{os.linesep}Channel: {white(_ch_id)}  ->  {ch_title}')
    print(f'{os.linesep}Playlists:')
    print_channel_playlists(chpls_info)

    print('Uploads playlist:')
    print(f'{os.linesep}    {uploads_plid}')
    print()

###############################################################################


if __name__ == '__main__':

    # ----------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Like/dislike statistics of a YouTube video(s)/playlist(s)/channel(s).')

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

    ARG_VIDEOS = args.v
    ARG_PLAYLISTS = args.p
    ARG_CHANNELS = args.c

    if not (ARG_VIDEOS or ARG_PLAYLISTS or ARG_CHANNELS):
        parser.error('No resource requested, add -v or -p or -c (or -h for more info).')
    # ----------------------------------------------------------------------------------

    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME,
                                              YOUTUBE_API_VERSION,
                                              developerKey=DEVELOPER_KEY)

    colorama_init()

    if ARG_VIDEOS:
        vid_ids = ','.join(ARG_VIDEOS)
        print_videos_summary(youtube, vid_ids)

    if ARG_PLAYLISTS:
        for pl_id in ARG_PLAYLISTS:
            print_playlist_summary(youtube, pl_id)

    if ARG_CHANNELS:
        for ch_id in ARG_CHANNELS:
            print_channel_summary(youtube, ch_id)

# ---------------------------------------------------------------

    # # vid_ids = "bJFZqc4wAv8"
    # vid_ids = "Ks-_Mh1QhMc,bJFZqc4wAv8,Bd4VBIgByes,rK2QlHxo5Fc,IlU-zDU6aQ0,Y9LBUf1NzU0"

    # print_videos_summary(youtube, vid_ids)

# ---------------------------------------------------------------

    # # pl_id = 'PLxuCrhMbMnaIMvOiVMx15QpKQni19wSvu'  #
    # pl_id = 'OLAK5uy_mnVXq_ZT60M5PpSq0zoRigTIA6vYzJuBA'  # Zang  (ILE TO MA ZNAKÓW?)

    # print_playlist_summary(youtube, pl_id)

# ---------------------------------------------------------------

    # # ch_id = 'UCeHFfLZc7_wp1kPDKC_E6nw'  # -> EW
    # # ch_id = 'UCe8VykA_qDCBmg_08eIA8iQ'  # -> Iwuć
    # ch_id = 'UCFK7a4Nm1UW7_U_nUuf5XRw'  # -> ihanio

    # print_channel_summary(youtube, ch_id)

# ---------------------------------------------------------------

    colorama_deinit()
