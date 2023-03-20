import discord, os, datetime, argparse, signal, gb
from createDatabase import createDatabase
from discordClient import discordClient

# Parse CLI arguments
parser = argparse.ArgumentParser(description = "Discord logger aiming to log as much as possible.")
parser.add_argument("-t", "--token", help = "Discord token", required = True)
parser.add_argument("-d", "--database-file", help = "Database file", default = "database.db")
parser.add_argument("-m", "--media-dir", help = "Media directory", default = "media/")
args = parser.parse_args()

# Set global variables
gb.cursor = createDatabase(args.database_file)
gb.mediaPath = args.media_dir
os.makedirs(gb.mediaPath, exist_ok = True)

# Start bot
bot = discordClient()
bot.run(args.token)