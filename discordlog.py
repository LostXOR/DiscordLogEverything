import datetime, time, json, uuid, sqlite3

class logger:
    def __init__(self, databasePath, mediaPath, maxMessages, maxTime):
        # Make variables accessible to entire class
        self.db = sqlite3.connect(f"{databasePath}")
        self.cursor = self.db.cursor()
        self.mediaPath = mediaPath
        self.maxMessages = maxMessages
        self.maxTime = maxTime

        # Create tables for data types if they don't exist already
        self.db.execute("CREATE TABLE IF NOT EXISTS Guild(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, owner_id, created_at, joined_at, description, member_count, online_count, channels, members, categories)")
        self.db.execute("CREATE TABLE IF NOT EXISTS TextChannel(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, guild_id, category_id, topic, position)")
        self.db.execute("CREATE TABLE IF NOT EXISTS VoiceChannel(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, guild_id, category_id, bitrate, position)")
        self.db.execute("CREATE TABLE IF NOT EXISTS StageChannel(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, guild_id, category_id, bitrate, position)")
        self.db.execute("CREATE TABLE IF NOT EXISTS ForumChannel(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, guild_id, category_id, position)")
        self.db.execute("CREATE TABLE IF NOT EXISTS CategoryChannel(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, guild_id, position, channels)")
        self.db.execute("CREATE TABLE IF NOT EXISTS Member(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, discriminator)")
        self.db.execute("CREATE TABLE IF NOT EXISTS User(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, discriminator)")
        self.db.execute("CREATE TABLE IF NOT EXISTS ClientUser(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, name, discriminator)")
        self.db.execute("CREATE TABLE IF NOT EXISTS Message(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, content, channel_id, author_id, attachments)")
        self.db.execute("CREATE TABLE IF NOT EXISTS Asset(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, key, url)")
        self.db.execute("CREATE TABLE IF NOT EXISTS Attachment(uuid PRIMARY KEY, timestamp, deleted, event_uuid, id, url, proxy_url, size, filename)")

        # Create tables for events if they don't exist already
        self.db.execute("CREATE TABLE IF NOT EXISTS EventMessage(uuid PRIMARY KEY, timestamp, message_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventMessageEdit(uuid PRIMARY KEY, timestamp, message_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventMessageDelete(uuid PRIMARY KEY, timestamp, message_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventBulkMessageDelete(uuid PRIMARY KEY, timestamp, message_ids)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventReactionAdd(uuid PRIMARY KEY, timestamp, emoji_id, message_id, user_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventReactionRemove(uuid PRIMARY KEY, timestamp, emoji_id, message_id, user_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventReactionClear(uuid PRIMARY KEY, timestamp, message_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventReactionClearEmoji(uuid PRIMARY KEY, timestamp, emoji_id, message_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventGuildChannelDelete(uuid PRIMARY KEY, timestamp, channel_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventGuildChannelCreate(uuid PRIMARY KEY, timestamp, channel_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventGuildChannelUpdate(uuid PRIMARY KEY, timestamp, channel_id)")
        self.db.execute("CREATE TABLE IF NOT EXISTS EventTyping(uuid PRIMARY KEY, timestamp, user_id, channel_id, time)")

    # Save a snapshot of a Discord object to the database
    async def saveObjectSnapshot(self, object, eventUUID = None):
        objectType = type(object).__name__
        # Array representing row to be added to database with variables common to all objects
        newRow = [str(uuid.uuid4()), time.time(), 0, eventUUID, object.id]

        if objectType == "Guild":
            newRow += [
                object.name,
                object.owner_id,
                time.mktime(object.joined_at.timetuple()),
                time.mktime(object.created_at.timetuple()),
                object.description,
                object.member_count,
                object.online_count,
                ",".join([str(channel.id) for channel in object.channels]),
                ",".join([str(member.id) for member in object.members]),
                ",".join([str(category.id) for category in object.categories])]
            for channel in object.channels: await self.saveObjectSnapshot(channel)
            for member in object.members: await self.saveObjectSnapshot(member)
            for category in object.categories: await self.saveObjectSnapshot(category)

        elif objectType == "TextChannel":
            newRow += [
                object.name,
                object.guild.id,
                object.category_id,
                object.topic,
                object.position]
            await self.saveMessagesSnapshot(object)

        elif objectType == "VoiceChannel":
            newRow += [
                object.name,
                object.guild.id,
                object.category_id,
                object.bitrate,
                object.position]

        elif objectType == "StageChannel":
            newRow += [
                object.name,
                object.guild.id,
                object.category_id,
                object.bitrate,
                object.position]

        elif objectType == "ForumChannel":
            newRow += [
                object.name,
                object.guild.id,
                object.category_id,
                object.position]

        elif objectType == "CategoryChannel":
            newRow += [
                object.name,
                object.guild.id,
                object.position,
                ",".join([str(channel.id) for channel in object.channels])]

        elif objectType == "Member":
            newRow += [
                object.name,
                object.discriminator]

        elif objectType == "User" or objectType == "ClientUser":
            newRow += [
                object.name,
                object.discriminator]

        elif objectType == "Message":
            newRow += [
                object.content,
                object.channel.id,
                object.author.id,
                ",".join([str(attachment.id) for attachment in object.attachments])]
            for attachment in object.attachments: await self.saveObjectSnapshot(attachment)
            await self.saveObjectSnapshot(object.author)

        elif objectType == "Asset":
            newRow += [
                object.key,
                object.url]
            await object.save(f"{self.mediaPath}/{object.id}")

        elif objectType == "Attachment":
            newRow += [
                object.url,
                object.proxy_url,
                object.size,
                object.filename]
            try:
                await object.save(f"{self.mediaPath}/{object.id}", use_cached = True)
            except:
                print(newRow)

        else:
            print(f"{objectType} unknown")

        # Fetch latest existing snapshot of object with ID
        response = self.cursor.execute(f"SELECT * FROM {objectType} WHERE id = ? ORDER BY timestamp DESC LIMIT 1", [object.id]).fetchone()
        # Save new snapshot if latest snapshot is different or does not exist
        if not response or list(response[5:]) != newRow[5:]:
            parameters = ", ".join("?" * len(newRow))
            self.cursor.execute(f"INSERT INTO {objectType} VALUES ({parameters})", newRow)
            self.db.commit()

    # Used to update deleted objects to represent that they are deleted
    async def deleteObject(self, objectID, objectType, eventUUID):
        self.cursor.execute(f"INSERT INTO {objectType} (uuid, timestamp, deleted, event_uuid, id) VALUES (?, ?, ?, ?, ?)", [str(uuid.uuid4()), time.time(), 1, eventUUID, objectID])
        self.db.commit()

    async def logEvent(self, eventType, eventData):
        rowUUID = str(uuid.uuid4())
        newRow = [rowUUID, time.time()] + eventData
        parameters = ", ".join("?" * len(newRow))
        self.cursor.execute(f"INSERT INTO Event{eventType} VALUES ({parameters})", newRow)
        return rowUUID

    # Take snapshots of messages in a channel going back maxMessages or to maxTime (datetime.timedelta)
    async def saveMessagesSnapshot(self, channel):
        try:
            async for message in channel.history(limit = self.maxMessages, after = datetime.datetime.now() - self.maxTime):
                await self.saveObjectSnapshot(message)
        except:
            pass