# DiscordLogEverything
## Info
#### This project is in alpha. Most functionality is incomplete, and bugs and errors are to be expected. Please let me know if you encounter any errors.
DiscordLogEverything is a program to log Discord objects (such as messages, channels, and users) and events (such as reactions, messages being sent, and messages being deleted). My eventual goal is to log all data the user can access, but currently the amount of things being logged is very limited.

This was created as an alternative to [MessageLoggerV2](https://github.com/1Lighty/BetterDiscordPlugins/tree/master/Plugins/MessageLoggerV2), which is no longer being maintained.

Warning: DiscordLogEverything requires automating a user account, which is against Discord's Terms of Service. You are very unlikely to be banned while using it, but it is a possibility.

## Setup
Run these commands
```
pip install discord.py-self
git clone https://github.com/LostXOR/DiscordLogEverything
cd DiscordLogEverything
```
Create a file in the repository directory named `token.txt` containing your Discord token. [Here's a guide on how to get your token by Tyrrrz.](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md)
## Usage
Run the logger with
```
python3 main.py
```
Logged objects and events are stored in an sqlite3 database at `data/objects.db`. Attachments are stored in `data/media/<attachment id>`. There is currently no viewer for the logs. You can query them using your favorite sqlite3 program.
## Planned Features (roughly in planned order of completion)
- [ ] Log all events
- [ ] Log all object data fully
- [ ] Command line options
- [ ] Customize events and objects being logged
- [ ] Event and object viewer
- [ ] Save channel and thread message history
- [ ] Export data in other formats (JSON compatible with [DiscordChatExporter-frontend](https://github.com/slatinsky/DiscordChatExporter-frontend)?)
