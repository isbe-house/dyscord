# Changelog

This project follows [Semantic Versioning](https://semver.org/) and [Keep A Change Log](https://keepachangelog.com/en/1.0.0/).

## [v0.4.2] WIP
### Added
- `Activty` and friends.
- `Presence` and friends.
- Support `GUILD_MEMBER_UPDATE` events.

### Fixed
- Made reconnection more robust.

## [v0.4.1] 2021-10-27
### Added
- Added the `dyscord.command` alias to point to commonly used command interfaces.
- `Message.formatter.TIMESTAMP_FLAGS` was missing the `SHORT_DATE_TIME` option.

### Changed
- `MESSAGE_UPDATE` events now return a `MessageUpdate` object. This is a duplicate of `Message`, except most fields are annotated as `Optional`.
- `User` and `Member` objects now support mentions straight from the `__str__()` method. This allows you to do `f'Hello {user_variable}` and get a mention!\
- Unit testing coverage now > 70% for the project. On our way to 100%!

### Deprecated
- `Command.generate(options)` Argument is optional, and should be removed by `0.6.0`.

### Removed
- Unused `Cache()` function from `User` and `Member`.
- Nonfunctionl `edit_origional_response()` and `delete_initial_response()` from `InteractionResponse`, they are not in the discord API.

### Fixed
- Removed `ephemeral` from followup generate messages, discord ignores this flag anyway!
- `Message` objects assumed they would get a lot of fields, which is not true in `MESSAGE_UPDATE` events.

## [v0.4.0] 2021-10-27
### Added
- New set_all_intents() function in DiscordClient. Sets all intents to True.
- Better example code.
- User and Member now have all attributes set to `None` by default.
- Role now has all attributes set to `None` by default.
- Begin restructure of documentation to make some sense.
- Registering to a guild allows you to register different commands to different guilds.
- TTL Cache to API.get_user, API.get_guild and API.get_channel.

### Changed
- `InteractionStructure` renamed to `Interaction`.
- `InteractionDataStructure` renamed to `InteractionData`.
- `register_handler` renamed to `decorate_handler`.
- `DISCORD_EVENTS` moved from `dyscord.objects` to `discord.client`.
- Reworked the repo to be a bit cleaner.
- Moved Dockerfiles to their own folder, with a 4x speedup on initial build times.
- Attributes of classes updated to be `None` by default.
    - Channel (and subclasses).
    - Guild
    - Embed
- Removed `ingest_raw_dict()` from classes.
    - Channel (and subclasses).
    - Guild
    - Embed
    - Message
    - Ready
    - User
    - Member

### Fixed
- Exposed the `__version__` string at the top module level.

## [v0.3.1] 2021-10-22
### Added
- Handle invalid session events.
- Support for ReadTheDocs.

### Fixed
- Importing actually works again.

## [v0.3.0] 2021-10-22
### Added
- Built in reconnect support.
- Support giving an event loop to DiscordClient.run()

## [v0.2.0] 2021-10-18
### Added
- cachetools>=4.2.4 now required.
- validators>=0.18.2 now required.
- Helper classes to manage Questions and Confirmations.

### Changed
- Started the process of documenting out most of the existing codebase.

### Fixed
- Corrected typo in webhook intents.

## [v0.1.0] 2021-10-09
### Added
- Documentation!
- helper.CommandHandler added to bind Interaction responses from the API to local code in a sane way.
- client.DiscordClient.register_class wrapper added to allow users to wrap their handlers in classes.

### Changed
- Updated client.DiscordClient.register_handler to support async and sync functions.

### Removed
- Cleaned out some to_dict() functions from objects that we will never really need to turn into dicts.
