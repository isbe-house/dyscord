# Examples

## Getting Started

### Install

Run `pip install --upgrade dsycord` to get the latest version.

### Basic Bot

TODO: Link to instructions on getting a discord client token setup.

```python
import dyscord

token = "YOUR TOKEN GOES HERE"

client = dyscord.DiscordClient(token=token)

client.set_all_intents()

@client.register_handler('MESSAGE_CREATE')
async def parse_message(client, message, raw_message):
    # Logic to handle the event goes here.
    print(f"I got a {message} from the client!")

client.run()
```

You should now be connected to the discord API and any `MESSAGE_CREATE` events your bot sees will trigger a call to the `parse_message` function.

### Complex Setup

This is a more complex setup. We set more exact intents, and register a global command when we boot. Note that your command won't actually work until you use the interaction to respond with something.

```python
import dyscord

token = "YOUR TOKEN GOES HERE"
application_id = "YOUR APPLICATION ID GOES HERE"

client = dyscord.DiscordClient(token=token, application_id=application_id)

client.configure_intents(
    guilds=True,
    guild_members=True,
    guild_messages=True,
    guild_message_reactions=True,
    guild_message_typeing=True,
    direct_messages=True,
)

async def test_callback(client, interaction):
    # Handle your interaction
    pass

@client.register_handler('ON_READY')
async def get_bot_ready(client, message, raw_message):

    guild_id = '1234' # REPLACE ME WITH YOUR GUILD ID!

    new_command = dyscord.objects.interactions.Command()
    new_command.generate(
        name='test',
        description='Generic test slash command.',
        type=dyscord.objects.interactions.enumerations.COMMAND_TYPE.CHAT_INPUT,
    )
    new_command.add_option_typed(new_command.COMMAND_OPTION.BOOLEAN, 'cleanup', 'Cleanup commands after execution?', required=False)

    new_command.validate()

    registration = await new_command.register_to_guild(guild_id)

    dyscord.helper.CommandHandler.register_guild_callback('test', test_callback)

client.run()
```
