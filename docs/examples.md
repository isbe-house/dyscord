# Examples

## Getting Started

### Install

Run `pip install --upgrade dsycord` to get the latest version.

### Basic Bot

TODO: Link to instructions on getting a discord client token setup.

```python
import dyscord

token = "YOUR TOKEN GOES HERE"
application_id = "YOUR APPLICATION ID GOES HERE"

client = dyscord.client.DiscordClient(token=token, application_id=application_id)

@client.register_handler('MESSAGE_CREATE')
async def parse_message(client, message, raw_message):
    # Logic to handle the event goes here.
    print(f"I got a {message} from the client!")

client.run()
```

You should now be connected to the discord API and any `MESSAGE_CREATE` events your bot sees will trigger a call to the `parse_message` function.
