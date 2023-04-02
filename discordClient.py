import discord, json, time, uuid, globalVars
from parseEvent import parseEvent

# Basic Discord client
class discordClient(discord.Client):
    async def on_ready(self):
        print("Connected to Discord.")

    # Receiving data directly from the socket as it's more "raw" than discord.py-self's premade events
    async def on_socket_raw_receive(self, data):
        # Set timestamp immediately to get as accurate of a time as possible
        timestamp = time.time()
        dataJSON = json.loads(data)
        #print(msg)

        # Save raw socket data to the socket_recv table in the database
        socketRecvUUID = str(uuid.uuid4())
        globalVars.cursor.execute("INSERT INTO socket_recv VALUES (?, ?, ?)", [socketRecvUUID, timestamp, data])

        # Process event
        if dataJSON["op"] == 0:
            parseEvent(socketRecvUUID, timestamp, dataJSON)