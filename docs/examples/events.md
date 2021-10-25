# Events

Discords preferred mode of interaction is for an application to respond to events. *The application should never poll discord to check if it needs to do something.*

Once the [DiscordClient][dyscord.client.DiscordClient] is connected to the discord API it will receive any events that are relevant to it's resources. For example, when another client sends a message the application will receive a `CREATE_MESSAGE` event. The application can then chose to respond to the event in some way. For a full list of the events supported, see the [events list][dyscord.objects.enumerations.DISCORD_EVENTS].

Dyscord enables you to listen to these events in a few different ways.

## Function Command Handler

```python3

# Not shown: Commands to setup the DiscordClient, bind it to a variable `client` and declare intent to listen to messages.

@client.decorate_handler('MESSAGE_CREATE')
async def my_message_create_handler(message: Message):
    print('We got a message!')
    print(message.content)
```

This function will be invoked any time the application sees a `MESSAGE_CREATE` event from the API. The raw data of the message is first parsed by Dyscord, and then given to the message as a `Message` object. Different events will result in different object types being provided to the function.

For a full list of the events supported, see the [events list][dyscord.objects.enumerations.DISCORD_EVENTS].

## Class Handler

In some situations it might be preferable for a *class* to handle your callbacks. You can register an entire class of callback functions at once.

```python3

# Not shown: Commands to setup the DiscordClient, bind it to a variable `client` and declare intent to listen to messages.


@client.decorate_class
class MyCallbacks:

    @classmethod
    async def on_message(message: Message):
        print('We got a message!')
        print(message.content)
```

This example is a full duplicate of above Functional Handler example.

## Subclass of DiscordClient

If deeper object support is needed, then the `DiscordClient` object can be subclassed and executed directly.

```python3

from dyscord.client import DiscordClient

class MyClient(DiscordClient):

    async def on_message(message: Message):
        print('We got a message!')
        print(message.content)

client = MyClient()

client.run()
```

## Callback Function Signature

Callback functions **should** be `async` functions. While you **can** use sync functions, it is **strongly** recommended that your code be async when ever possible.

The arguments of the callback are dynamic based on the number of arguments given. The following examples are all valid, and will work.

```python
@client.decorate_handler('MESSAGE_CREATE')
async def foo0():
    pass

@client.decorate_handler('MESSAGE_CREATE')
async def foo1(message):
    pass

@client.decorate_handler('MESSAGE_CREATE')
async def foo2(message, raw_message):
    pass

@client.decorate_handler('MESSAGE_CREATE')
async def foo3(message, raw_message, client):
    pass
```

The argument names **do not matter**. You can name them as you choose. As a result, the order is the only thing that matters. If you ask for `async def foo(client)`, you will NOT get the `DiscordClient` object as your first argument! If you need the `client` argument, you must accept three total arguments.