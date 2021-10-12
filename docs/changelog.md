# Changelog

This project follows [Semantic Versioning](https://semver.org/) and [Keep A Change Log](https://keepachangelog.com/en/1.0.0/).

## [v0.1.1] WIP
### Added
- cachetools now required.

## [v0.1.0] 2021-10-09
### Added
- Documentation!
- helper.CommandHandler added to bind Interaction responses from the API to local code in a sane way.
- client.DiscordClient.register_class wrapper added to allow users to wrap their handlers in classes.

### Changed
- Updated client.DiscordClient.register_handler to support async and sync functions.

### Removed
- Cleaned out some to_dict() functions from objects that we will never really need to turn into dicts.
