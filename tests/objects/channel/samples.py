dev_guild_text = {
    "id": "41771983423143937",
    "guild_id": "41771983423143937",
    "name": "general",
    "type": 0,
    "position": 6,
    "permission_overwrites": [],
    "rate_limit_per_user": 2,
    "nsfw": True,
    "topic": "24/7 chat about how to gank Mike #2",
    "last_message_id": "155117677105512449",
    "parent_id": "399942396007890945",
    "default_auto_archive_duration": 60
}

dev_guild_news = {
    "id": "41771983423143937",
    "guild_id": "41771983423143937",
    "name": "important-news",
    "type": 5,
    "position": 6,
    "permission_overwrites": [],
    "nsfw": True,
    "topic": "Rumors about Half Life 3",
    "last_message_id": "155117677105512449",
    "parent_id": "399942396007890945",
    "default_auto_archive_duration": 60
}

dev_guild_voice = {
    "id": "155101607195836416",
    "guild_id": "41771983423143937",
    "name": "ROCKET CHEESE",
    "type": 2,
    "nsfw": False,
    "position": 5,
    "permission_overwrites": [],
    "bitrate": 64000,
    "user_limit": 0,
    "parent_id": None,
    "rtc_region": None
}

dev_dm = {
    "last_message_id": "3343820033257021450",
    "type": 1,
    "id": "319674150115610528",
    "recipients": [
        {
          "username": "test",
          "discriminator": "9999",
          "id": "82198898841029460",
          "avatar": "33ecab261d4681afa4d85a04691c4a01"
        }
    ]
}

dev_group_dm = {
    "name": "Some test channel",
    "icon": None,
    "recipients": [
        {
            "username": "test",
            "discriminator": "9999",
            "id": "82198898841029460",
            "avatar": "33ecab261d4681afa4d85a04691c4a01"
        },
        {
            "username": "test2",
            "discriminator": "9999",
            "id": "82198810841029460",
            "avatar": "33ecab261d4681afa4d85a10691c4a01"
        }
    ],
    "last_message_id": "3343820033257021450",
    "type": 3,
    "id": "319674150115710528",
    "owner_id": "82198810841029460"
}

dev_category = {
    "permission_overwrites": [],
    "name": "Test",
    "parent_id": None,
    "nsfw": False,
    "position": 0,
    "guild_id": "290926798629997250",
    "type": 4,
    "id": "399942396007890945"
}

dev_store = {
    "id": "41771983423143937",
    "guild_id": "41771983423143937",
    "name": "buy dota-2",
    "type": 6,
    "position": 0,
    "permission_overwrites": [],
    "nsfw": False,
    "parent_id": None
}

dev_thread = {
    "id": "41771983423143937",
    "guild_id": "41771983423143937",
    "parent_id": "41771983423143937",
    "owner_id": "41771983423143937",
    "name": "don't buy dota-2",
    "type": 11,
    "last_message_id": "155117677105512449",
    "message_count": 1,
    "member_count": 5,
    "rate_limit_per_user": 2,
    "thread_metadata": {
            "archived": False,
            "auto_archive_duration": 1440,
            "archive_timestamp": "2021-04-12T23:40:39.855793+00:00",
            "locked": False
    }
}

partial_resolved = {'id': '889282264507248650',
                    'name': 'general2',
                    'parent_id': '804392362629267456',
                    'permissions': '1099511627775',
                    'type': 0}

all = [dev_category, dev_dm, dev_group_dm, dev_guild_news, dev_guild_text, dev_guild_voice, dev_store, dev_thread, partial_resolved]
