# Changelog

This project follows [Semantic Versioning](https://semver.org/) and [Keep A Change Log](https://keepachangelog.com/en/1.0.0/).

## [v0.4.0] WIP
### Added
- New set_all_intents() function in DiscordClient. Sets all intents to True.
- Better example code.
- User and Member now have all attributes set to `None` by default.
- Role now has all attributes set to `None` by default.
- Begin restructure of documentation to make some sense.

### Changed
- `InteractionStructure` renamed to `Interaction`.
- `InteractionDataStructure` renamed to `InteractionData`.

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
