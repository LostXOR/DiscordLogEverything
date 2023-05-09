# DiscordLogEverything
[![Discord](https://img.shields.io/discord/1087868245618470955?color=5865f2&label=Discord&logo=Discord&logoColor=5865f2)](https://discord.gg/eJjgmt7C73)
#### This project is in pre-alpha. Most functionality is incomplete, versions are not thoroughly tested, and bugs and errors are to be expected.
DiscordLogEverything is a program to log Discord objects (such as messages, channels, and users) and events (such as reactions, messages being sent, and messages being deleted). My eventual goal is to log all data the user can access, but currently the amount of things being logged is very limited.

This was created as an alternative to [MessageLoggerV2](https://github.com/1Lighty/BetterDiscordPlugins/tree/master/Plugins/MessageLoggerV2), which is no longer being maintained.

Warning: DiscordLogEverything requires automating a user account, which is against Discord's Terms of Service. You are very unlikely to be banned while using it, but it is a possibility.

## Setup
1. Install [discord-py.self](https://pypi.org/project/discord.py-self).

2. Clone this repository.
## Usage
To start the logger, run
```
main.py --token <Discord token> --database-file <database path> --media-dir <media directory>
```
`--database-file` and `--media-dir` are optional and will default to `database.db` and `media` in the current directory respectively.

Logged objects and socket data are stored in an sqlite3 database at the path specified with `--database-file`. Attachments are ~~stored in the directory specified with `--media-dir`~~ not currently downloaded. There is currently no viewer for the logs. You can query them using your favorite sqlite3 program.

Due to changes to the database layout, new versions of DiscordLogEverything are usually not compatible with databases from previous versions. You should create a new database after updating to avoid errors.
## Planned Features (roughly in planned order of completion)
- [ ] Parse every event for assets/media and download them
- [ ] More command line options
- [ ] Save channel and thread message history
- [ ] Viewer
- [ ] Export data in other formats (JSON compatible with [DiscordChatExporter-frontend](https://github.com/slatinsky/DiscordChatExporter-frontend)?)