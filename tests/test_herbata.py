from src.herbata import refine_videos_response
from src.herbata import likes_percent
from src.herbata import refine_playlistitems_response
from src.herbata import refine_channel_playlists_response


def test_refine_videos_response1():
    inputresp = {
        "kind": "youtube#videoListResponse",
        "etag": "viL9GMPz9fjH9EneyPDGjM2BfIc",
        "items": [{
            "kind": "youtube#video",
            "etag": "nbaq1oj-txFPYaIqOv3pwiXO9-c",
            "id": "bJFZqc4wAv8",
            "snippet": {
                "publishedAt": "2020-10-03T07:46:56Z",
                "channelId": "UCeHFfLZc7_wp1kPDKC_E6nw",
                "title": "Jak inwestować i zarabiać na akcjach? *podstawy z Trader21*",
                "description": "* Książka tradera, którą bardzo polecam! https://www.inteligentnyinwestor.pl/ zaznacz - skąd się dowiedziałeś : \"genetyk\" i otrzymaj dostęp do wszelkich dodatków!",
                "channelTitle": "Efekt Wytrwałości",
                "categoryId": "22",
                "liveBroadcastContent": "none",
                "localized": {
                    "title": "Jak inwestować i zarabiać na akcjach? *podstawy z Trader21*",
                    "description": "* Książka tradera, którą bardzo polecam! https://www.inteligentnyinwestor.pl/ zaznacz - skąd się dowiedziałeś : \"genetyk\" i otrzymaj dostęp do wszelkich dodatków!"
                }
            },
            "statistics": {
                "viewCount": "26984",
                "likeCount": "1063",
                "dislikeCount": "22",
                "favoriteCount": "0",
                "commentCount": "57"
            }
        }],
        "pageInfo": {
            "totalResults": 1,
            "resultsPerPage": 1
        }
    }

    expected = [
            {
                "id": "bJFZqc4wAv8",
                "title": "Jak inwestować i zarabiać na akcjach? *podstawy z Trader21*",
                "viewCount": "26984",
                "likeCount": "1063",
                "dislikeCount": "22",
                "commentCount": "57"
            }
        ]

    assert refine_videos_response(inputresp) == expected


def test_refine_videos_response2():
    inputresp = {
        "kind": "youtube#videoListResponse",
        "etag": "DXIUq_lkaZuWir6zoAJGbyf9JJU",
        "items": [{
                "kind": "youtube#video",
                "etag": "akbIWEP8axObCGgStR7PoUPxjRM",
                "id": "Ks-_Mh1QhMc",
                "snippet": {
                    "publishedAt": "2012-10-01T15:27:35Z",
                    "channelId": "UCAuUUnT6oDeKwE6v1NGQxug",
                    "title": "Your body language may shape who you are | Amy Cuddy",
                    "description": "Body language affects how others see us, but it may also change how we see ourselves. Social psychologist Amy Cuddy argues that \"power posing\" -- standing in a posture of confidence, even when we don't feel confident -- can boost feelings of confidence, and might have an impact on our chances for success. (Note: Some of the findings presented in this talk have been referenced in an ongoing debate among social scientists about robustness and reproducibility. Read Amy Cuddy's response here: http://ideas.ted.com/inside-the-debate-about-power-posing-a-q-a-with-amy-cuddy/)\n\nGet TED Talks recommended just for you! Learn more at https://www.ted.com/signup.\n\nThe TED Talks channel features the best talks and performances from the TED Conference, where the world's leading thinkers and doers give the talk of their lives in 18 minutes (or less). Look for talks on Technology, Entertainment and Design -- plus science, business, global issues, the arts and more.\n\nFollow TED on Twitter: http://www.twitter.com/TEDTalks\nLike TED on Facebook: https://www.facebook.com/TED\n\nSubscribe to our channel: https://www.youtube.com/TED",
                    "channelTitle": "TED",
                    "tags": [
                        "Amy Cuddy",
                        "TED",
                        "TEDTalk",
                        "TEDTalks",
                        "TED Talk",
                        "TED Talks",
                        "TEDGlobal",
                        "brain",
                        "business",
                        "psychology",
                        "self",
                        "success"
                    ],
                    "categoryId": "22",
                    "liveBroadcastContent": "none",
                    "defaultLanguage": "en",
                    "localized": {
                        "title": "Your body language may shape who you are | Amy Cuddy",
                        "description": "Body language affects how others see us, but it may also change how we see ourselves. Social psychologist Amy Cuddy argues that \"power posing\" -- standing in a posture of confidence, even when we don't feel confident -- can boost feelings of confidence, and might have an impact on our chances for success. (Note: Some of the findings presented in this talk have been referenced in an ongoing debate among social scientists about robustness and reproducibility. Read Amy Cuddy's response here: http://ideas.ted.com/inside-the-debate-about-power-posing-a-q-a-with-amy-cuddy/)\n\nGet TED Talks recommended just for you! Learn more at https://www.ted.com/signup.\n\nThe TED Talks channel features the best talks and performances from the TED Conference, where the world's leading thinkers and doers give the talk of their lives in 18 minutes (or less). Look for talks on Technology, Entertainment and Design -- plus science, business, global issues, the arts and more.\n\nFollow TED on Twitter: http://www.twitter.com/TEDTalks\nLike TED on Facebook: https://www.facebook.com/TED\n\nSubscribe to our channel: https://www.youtube.com/TED"
                    },
                    "defaultAudioLanguage": "en"
                },
                "statistics": {
                    "viewCount": "18704320",
                    "likeCount": "271734",
                    "dislikeCount": "5317",
                    "favoriteCount": "0",
                    "commentCount": "8356"
                }
            },
            {
                "kind": "youtube#video",
                "etag": "y_c40cJfK_6kyDuLB8q4Q_fqn8s",
                "id": "bJFZqc4wAv8",
                "snippet": {
                    "publishedAt": "2020-10-03T07:46:56Z",
                    "channelId": "UCeHFfLZc7_wp1kPDKC_E6nw",
                    "title": "Jak inwestować i zarabiać na akcjach? *podstawy z Trader21*",
                    "description": "* Książka tradera, którą bardzo polecam! https://www.inteligentnyinwestor.pl/ zaznacz - skąd się dowiedziałeś : \"genetyk\" i otrzymaj dostęp do wszelkich dodatków!",
                    "channelTitle": "Efekt Wytrwałości",
                    "categoryId": "22",
                    "liveBroadcastContent": "none",
                    "localized": {
                        "title": "Jak inwestować i zarabiać na akcjach? *podstawy z Trader21*",
                        "description": "* Książka tradera, którą bardzo polecam! https://www.inteligentnyinwestor.pl/ zaznacz - skąd się dowiedziałeś : \"genetyk\" i otrzymaj dostęp do wszelkich dodatków!"
                    }
                },
                "statistics": {
                    "viewCount": "26979",
                    "likeCount": "1063",
                    "dislikeCount": "22",
                    "favoriteCount": "0",
                    "commentCount": "57"
                }
            }
        ],
        "pageInfo": {
            "totalResults": 2,
            "resultsPerPage": 2
        }
    }

    expected = [
            {
                "id": "Ks-_Mh1QhMc",
                "title": "Your body language may shape who you are | Amy Cuddy",
                "viewCount": "18704320",
                "likeCount": "271734",
                "dislikeCount": "5317",
                "commentCount": "8356"
            },
            {
                "id": "bJFZqc4wAv8",
                "title": "Jak inwestować i zarabiać na akcjach? *podstawy z Trader21*",
                "viewCount": "26979",
                "likeCount": "1063",
                "dislikeCount": "22",
                "commentCount": "57"
            }
        ]

    assert refine_videos_response(inputresp) == expected


def test_likes_percent():

    videoStatsInput1 = {
        'id': 'mJw1k6RGyvQ',
        'viewCount': '12899698',
        'likeCount': '57384',
        'dislikeCount': '4367'
    }

    expected1 = (92, 61751)

    assert likes_percent(videoStatsInput1) == expected1

    videoStatsInput2 = {
        # 'id': 'eujOPZRipi0',
        # 'viewCount': '4274250',
        'likeCount': '9946',
        'dislikeCount': '1611'
    }

    expected2 = (86, 11557)

    assert likes_percent(videoStatsInput2) == expected2


def test_refine_playlist_response():
    inputresp = {
        "kind": "youtube#playlistItemListResponse",
        "etag": "9WJrLGPzhFr5wG8FlcEISzHjiGE",
        "items": [{
                "kind": "youtube#playlistItem",
                "etag": "Bzw_ycPAXs1kV8vSkT09XSKFDAg",
                "id": "UEx4dUNyaE1iTW5hSU12T2lWTXgxNVFwS1FuaTE5d1N2dS41NkI0NEY2RDEwNTU3Q0M2",
                "contentDetails": {
                    "videoId": "bJFZqc4wAv8",
                    "videoPublishedAt": "2020-10-03T07:46:56Z"
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            {
                "kind": "youtube#playlistItem",
                "etag": "IXaT2VTNTTOafEQxP64bHtPjH4E",
                "id": "UEx4dUNyaE1iTW5hSU12T2lWTXgxNVFwS1FuaTE5d1N2dS4yODlGNEE0NkRGMEEzMEQy",
                "contentDetails": {
                    "videoId": "bU8_kSABxUM",
                    "videoPublishedAt": "2020-08-09T15:01:19Z"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        ],
        "pageInfo": {
            "totalResults": 2,
            "resultsPerPage": 5
        }
    }

    expected = [
        {
            "videoId": "bJFZqc4wAv8",
            "privacyStatus": "public"
        },
        {
            "videoId": "bU8_kSABxUM",
            "privacyStatus": "public"
        }
    ]

    assert refine_playlistitems_response(inputresp) == expected


def test_refine_channel_playlists_response():
    inputresp = {
        "kind": "youtube#playlistListResponse",
        "etag": "J1rme14beALRhB6Tyz_Ug25zzFU",
        "pageInfo": {
            "totalResults": 3,
            "resultsPerPage": 25
        },
        "items": [{
                "kind": "youtube#playlist",
                "etag": "kbUH-InUece8DF20qK1CxzmZGKY",
                "id": "PLxuCrhMbMnaIMvOiVMx15QpKQni19wSvu",
                "snippet": {
                    "publishedAt": "2020-09-29T14:14:16Z",
                    "channelId": "UCeHFfLZc7_wp1kPDKC_E6nw",
                    "title": "podstawy z Traderem!",
                    "description": "",
                    "channelTitle": "Efekt Wytrwałości",
                    "localized": {
                        "title": "podstawy z Traderem!",
                        "description": ""
                    }
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            {
                "kind": "youtube#playlist",
                "etag": "bLhkS8VE9kfMAY8ZODwDu_eYvCA",
                "id": "PLxuCrhMbMnaKqYG1ulOXWm3WQ5eZKXiIb",
                "snippet": {
                    "publishedAt": "2020-09-21T15:49:36Z",
                    "channelId": "UCeHFfLZc7_wp1kPDKC_E6nw",
                    "title": "Wynajem mieszkania *seria*",
                    "description": "",
                    "channelTitle": "Efekt Wytrwałości",
                    "localized": {
                        "title": "Wynajem mieszkania *seria*",
                        "description": ""
                    }
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        ]
    }

    expected = [
        {
            "id": "PLxuCrhMbMnaIMvOiVMx15QpKQni19wSvu",
            "title": "podstawy z Traderem!",
            "privacyStatus": "public"
        },
        {
            "id": "PLxuCrhMbMnaKqYG1ulOXWm3WQ5eZKXiIb",
            "title": "Wynajem mieszkania *seria*",
            "privacyStatus": "public"
        }
    ]

    assert refine_channel_playlists_response(inputresp) == expected
