import os, argparse, sqlite3, json, time, uuid, discord, globalVars
from downloadAssets import downloadAssets

# Parse CLI arguments
parser = argparse.ArgumentParser(description = "Discord logger aiming to log as much as possible.")
parser.add_argument("-t", "--token", help = "Discord token", required = True)
parser.add_argument("-d", "--database-file", help = "Database file", default = "database.db")
parser.add_argument("-m", "--media-dir", help = "Media directory", default = "media/")
args = parser.parse_args()

# Create database
globalVars.mediaPath = args.media_dir
os.makedirs(args.media_dir, exist_ok = True)
if os.path.dirname(args.database_file): os.makedirs(os.path.dirname(args.database_file), exist_ok = True)
globalVars.database = sqlite3.connect(args.database_file, isolation_level = None)
globalVars.cursor = globalVars.database.cursor()
globalVars.cursor.execute("CREATE TABLE IF NOT EXISTS socket_recv(uuid PRIMARY KEY, timestamp, json)")

# Discord client
class discordClient(discord.Client):
    async def on_ready(self):
        print("Connected to Discord.")

    # Receiving data directly from the socket as it's more "raw" than discord.py-self's premade events
    async def on_socket_raw_receive(self, data):
        # Set timestamp immediately to get as accurate of a time as possible
        timestamp = time.time()
        dataJSON = json.loads(data)

        # Save raw socket data to the socket_recv table in the database
        socketRecvUUID = str(uuid.uuid4())
        globalVars.cursor.execute("INSERT INTO socket_recv VALUES (?, ?, ?)", [socketRecvUUID, timestamp, data])

        # Process event
        if dataJSON["op"] == 0:
            downloadAssets(socketRecvUUID, timestamp, dataJSON)

# Start bot
bot = discordClient(enable_debug_events = True)
bot.run(args.token)

