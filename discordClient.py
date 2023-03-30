import discord, json, time, uuid, globalVars
from saveObject import saveObject

# Basic Discord client
class discordClient(discord.Client):
    async def on_ready(self):
        print("Connected to Discord.")

    # Receiving data directly from the socket as it's more "raw" than discord.py-self's premade events
    async def on_socket_raw_receive(self, msg):
        # Set timestamp immediately to get as accurate of a time as possible
        timestamp = time.time()
        data = json.loads(msg)
        #print(msg) forgot to comment this out, probably a good idea to avoid spamming people's consoles

        # Save raw socket data to the socket_recv table in the database
        recvUUID = str(uuid.uuid4())
        globalVars.cursor.execute("INSERT INTO socket_recv VALUES (?, ?, ?, ?, ?, ?)", [recvUUID, timestamp, data["op"], data["s"], data["t"], msg])

        # Process events
        if data["op"] == 0:

            # READY event - sent on first connection, contains lots of data the client needs to display guilds, channels, users, etc.
            if data["t"] == "READY":
                pass

            # READY_SUPPLEMENTAL event - sent right after READY with what seems to be some additional user data
            elif data["t"] == "READY_SUPPLEMENTAL":
                pass

            # Message events
            elif data["t"] == "TYPING_START": pass  # Typing only provides a user ID and channel ID, so no objects to log
            elif data["t"] == "MESSAGE_CREATE" or data["t"] == "MESSAGE_UPDATE": saveObject(data["d"], "message", recvUUID, timestamp, False)
            elif data["t"] == "MESSAGE_DELETE": saveObject(data["d"], "message", recvUUID, timestamp, True)
            elif data["t"] == "MESSAGE_DELETE_BULK": [saveObject({**data["d"], "id": id}, "message", recvUUID, timestamp, True) for id in data["d"].pop("ids")]