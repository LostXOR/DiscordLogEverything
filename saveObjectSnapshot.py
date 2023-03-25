import time, uuid, globalVars

# Save a snapshot of the object and all its properties to the database
# Currently just has a few skeleton properties for each object, more to be filled in
async def saveObjectSnapshot(object, eventUUID = None):
    objectType = type(object).__name__
    # Array representing row to be added to database with variables common to all objects
    newRow = [str(uuid.uuid4()), time.time(), 0, eventUUID, object.id]

    if objectType == "Guild":
        newRow += [
            object.name,
            object.owner_id,
            time.mktime(object.joined_at.timetuple()) if object.joined_at else None,
            time.mktime(object.created_at.timetuple()),
            object.description,
            object.member_count,
            object.online_count,
            ",".join([str(channel.id) for channel in object.channels]),
            ",".join([str(member.id) for member in object.members]),
            ",".join([str(category.id) for category in object.categories])]
        for channel in object.channels: await saveObjectSnapshot(channel, eventUUID)
        for member in object.members: await saveObjectSnapshot(member, eventUUID)
        for category in object.categories: await saveObjectSnapshot(category, eventUUID)

    elif objectType == "TextChannel":
        newRow += [
            object.name,
            object.guild.id,
            object.category_id,
            object.topic,
            object.position]

    elif objectType == "DMChannel":
        newRow += [
            object.recipient.id]

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

    elif objectType == "Thread":
        newRow += [
            object.name,
            object.member_count,
            object.owner_id,
            object.parent_id]


    elif objectType == "ThreadMember":
        newRow += [
            object.thread_id,
            time.mktime(object.joined_at.timetuple())
        ]

    elif objectType == "Member":
        newRow += [
            object.name,
            object.discriminator]

    elif objectType == "User":
        newRow += [
            object.name,
            object.discriminator]

    elif objectType == "ClientUser":
        newRow += [
            object.name,
            object.discriminator]

    elif objectType == "Message":
        newRow += [
            object.content,
            object.channel.id,
            object.author.id,
            ",".join([str(attachment.id) for attachment in object.attachments])]
        for attachment in object.attachments: await saveObjectSnapshot(attachment, eventUUID)
        await saveObjectSnapshot(object.author, eventUUID)

    elif objectType == "Emoji":
        newRow += [
            object.name,
            object.guild_id,
            object.url]
        await object.save(f"{globalVars.mediaPath}/{object.id}")

    elif objectType == "Role":
        newRow += [
            object.name,
            object.position,
            object.guild.id]

    elif objectType == "Asset":
        newRow += [
            object.key,
            object.url]
        await object.save(f"{globalVars.mediaPath}/{object.id}")

    elif objectType == "Attachment":
        newRow += [
            object.url,
            object.proxy_url,
            object.size,
            object.filename]
        # Sometimes the cache server doesn't have the file, so download from the non-cache server
        try:
            await object.save(f"{globalVars.mediaPath}/{object.id}", use_cached = True)
        except:
            await object.save(f"{globalVars.mediaPath}/{object.id}")

    elif objectType == "UserSettings":
        newRow += [
            str(object.locale)]

    elif objectType == "Relationship":
        newRow += [
            object.user.id,
            object.nick]

    elif objectType == "ScheduledEvent":
        newRow += [
            object.name,
            object.description,
            time.mktime(object.start_time.timetuple()),
            time.mktime(object.end_time.timetuple())]

    elif objectType == "Payment":
        newRow += [
            object.currency,
            object.sku_price]

    elif objectType == "Invite":
        newRow += [
            object.uses,
            object.guild.id]

    elif objectType == "Gift":
        newRow += [
            object.max_uses,
            object.redeemed]

    elif objectType == "Interaction":
        newRow += [
            object.message.id]

    elif objectType == "StageInstance":
        newRow += [
            object.channel.id]

    elif objectType == "Achievement":
        newRow += [
            object.name]

    elif objectType == "Entitlement":
        newRow += [
            object.parent_id]

    elif objectType == "Modal":
        newRow += [
            object.title]

    elif objectType == "Integration":
        newRow += [
            object.name]

    elif objectType == "StreamIntegration":
        newRow += [
            object.name]

    else:
        print(f"{objectType} unknown")
        return

    # Fetch latest existing snapshot of object with ID
    response = globalVars.cursor.execute(f"SELECT * FROM {objectType} WHERE id = ? ORDER BY timestamp DESC LIMIT 1", [object.id]).fetchone()
    # Save new snapshot if latest snapshot is different or does not exist
    if not response or list(response[5:]) != newRow[5:]:
        parameters = ", ".join("?" * len(newRow))
        globalVars.cursor.execute(f"INSERT INTO {objectType} VALUES ({parameters})", newRow)