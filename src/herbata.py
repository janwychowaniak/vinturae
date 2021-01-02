def refine_videos_response(_response):
    items = _response['items']
    refined = []
    for i in items:
        ir = {'id': i['id']}
        ir['title'] = i['snippet']['title']
        ir['viewCount'] = i['statistics']['viewCount']
        ir['likeCount'] = i['statistics']['likeCount']
        ir['dislikeCount'] = i['statistics']['dislikeCount']
        ir['commentCount'] = i['statistics']['commentCount']
        refined.append(ir)
    return refined


def likes_percent(_arg):

    likes = int(_arg['likeCount'])
    dislikes = int(_arg['dislikeCount'])
    votesTotal = likes + dislikes

    likes_prc = likes * 100 // votesTotal

    return (likes_prc, votesTotal)


def refine_playlistitems_response(_response):
    items = _response['items']
    refined = []
    for i in items:
        ir = {'videoId': i['contentDetails']['videoId']}
        ir['privacyStatus'] = i['status']['privacyStatus']
        refined.append(ir)
    return refined


def refine_channel_playlists_response(_response):
    items = _response['items']
    refined = []
    for i in items:
        ir = {'id': i['id']}
        ir['title'] = i['snippet']['title']
        ir['privacyStatus'] = i['status']['privacyStatus']
        refined.append(ir)
    return refined
