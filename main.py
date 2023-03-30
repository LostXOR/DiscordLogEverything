import os, sqlite3, argparse, globalVars
from discordClient import discordClient

# Parse CLI arguments
parser = argparse.ArgumentParser(description = "Discord logger aiming to log as much as possible.")
parser.add_argument("-t", "--token", help = "Discord token", required = True)
parser.add_argument("-d", "--database-file", help = "Database file", default = "database.db")
parser.add_argument("-m", "--media-dir", help = "Media directory", default = "media/")
args = parser.parse_args()

# Create database
os.makedirs(args.media_dir, exist_ok = True)
if os.path.dirname(args.database_file): os.makedirs(os.path.dirname(args.database_file), exist_ok = True)
globalVars.database = sqlite3.connect(args.database_file, isolation_level = None)
globalVars.cursor = globalVars.database.cursor()
globalVars.cursor.execute("CREATE TABLE IF NOT EXISTS socket_recv(uuid PRIMARY KEY, timestamp, op, s, t, json)")
globalVars.database.commit()

# Start bot
bot = discordClient(enable_debug_events = True)
bot.run(args.token)