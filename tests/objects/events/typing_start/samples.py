import json

user_typing_samples = json.loads('''[
  {
    "_id": {
      "$oid": "616c69e2ee2bf4afe2ede015"
    },
    "t": "TYPING_START",
    "s": 3,
    "op": 0,
    "d": {
      "user_id": "185846097284038656",
      "timestamp": 1634494946,
      "member": {
        "user": {
          "username": "Soton",
          "id": "185846097284038656",
          "discriminator": "2585",
          "avatar": "b437e9bd4b0e487a097c4538c6cdce3f"
        },
        "roles": [],
        "mute": false,
        "joined_at": "2021-01-28T16:48:04.105000+00:00",
        "hoisted_role": null,
        "deaf": false
      },
      "channel_id": "804392362629267458",
      "guild_id": "804392362054910047"
    }
  }
]''')
