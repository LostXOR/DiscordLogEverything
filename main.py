import discord, os, datetime, argparse, signal, globalVars
from createDatabase import createDatabase
from discordClient import discordClient

# Parse CLI arguments
parser = argparse.ArgumentParser(description = "Discord logger aiming to log as much as possible.")
parser.add_argument("-t", "--token", help = "Discord token", required = True)
parser.add_argument("-d", "--database-file", help = "Database file", default = "database.db")
parser.add_argument("-m", "--media-dir", help = "Media directory", default = "media/")
args = parser.parse_args()

# Set global variables
globalVars.cursor = createDatabase(args.database_file)
os.makedirs(args.media_dir, exist_ok = True)
globalVars.mediaPath = args.media_dir

# Start bot
bot = discordClient()
bot.run(args.token)