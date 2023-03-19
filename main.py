import discord, os, datetime, time
import discordlog

databasePath = "data/objects.db"
mediaPath = "data/media"
os.makedirs(mediaPath, exist_ok = True)
os.makedirs(os.path.dirname(databasePath), exist_ok = True)

token = open("token.txt", "r").read()
bot = discord.Client()
logger = discordlog.logger(databasePath, mediaPath, 0, datetime.timedelta(days = 1))

async def fetchMessage(messageID, channelID):
    channel = await bot.fetch_channel(channelID)
    return await channel.fetch_message(messageID)

@bot.event
async def on_ready():
    print("Connected.")
    for guild in bot.guilds:
        await logger.saveObjectSnapshot(guild)

# Events to be logged
@bot.event
async def on_message(message):
    eventUUID = await logger.logEvent("Message", [message.id])
    await logger.saveObjectSnapshot(message, eventUUID)

@bot.event
async def on_raw_message_edit(event):
    eventUUID = await logger.logEvent("MessageEdit", [event.message_id])
    await logger.saveObjectSnapshot(await fetchMessage(event.message_id, event.channel_id), eventUUID)

@bot.event
async def on_raw_message_delete(event):
    eventUUID = await logger.logEvent("MessageDelete", [event.message_id])
    await logger.deleteObject(event.message_id, "Message", eventUUID)

@bot.event
async def on_raw_bulk_message_delete(event):
    eventUUID = await logger.logEvent("BulkMessageDelete", [",".join(map(str, event.message_ids))])
    for id in event.message_ids: await logger.deleteObject(id, "Message", eventUUID)

@bot.event
async def on_raw_reaction_add(event):
    eventUUID = await logger.logEvent("ReactionAdd", [event.emoji.id, event.message_id, event.user_id])
    await logger.saveObjectSnapshot(await fetchMessage(event.message_id, event.channel_id), eventUUID)

@bot.event
async def on_raw_reaction_remove(event):
    eventUUID = await logger.logEvent("ReactionRemove", [event.emoji.id, event.message_id, event.user_id])
    await logger.saveObjectSnapshot(await fetchMessage(event.message_id, event.channel_id), eventUUID)

@bot.event
async def on_raw_reaction_clear(event):
    eventUUID = await logger.logEvent("ReactionClear", [event.message_id])
    await logger.saveObjectSnapshot(await fetchMessage(event.message_id, event.channel_id), eventUUID)

@bot.event
async def on_raw_reaction_clear_emoji(event):
    eventUUID = await logger.logEvent("ReactionClear", [event.emoji_id, event.message_id])
    await logger.saveObjectSnapshot(await fetchMessage(event.message_id, event.channel_id), eventUUID)

@bot.event
async def on_guild_channel_delete(channel):
    eventUUID = await logger.logEvent("GuildChannelDelete", [channel.id])
    await logger.deleteObject(channel.id, type(channel).__name__, eventUUID)

@bot.event
async def on_guild_channel_create(channel):
    eventUUID = await logger.logEvent("GuildChannelCreate", [channel.id])
    await logger.saveObjectSnapshot(channel, eventUUID)

@bot.event
async def on_guild_channel_update(before, channel):
    eventUUID = await logger.logEvent("GuildChannelUpdate", [channel.id])
    await logger.saveObjectSnapshot(channel, eventUUID)

@bot.event
async def on_typing(channel, user, when):
    eventUUID = await logger.logEvent("Typing", [user.id, channel.id, time.mktime(when.timetuple())])

bot.run(token)

"""
#@bot.event
#async def on_guild_channel_delete(channel):

#@bot.event
#async def on_guild_channel_create(channel):

#@bot.event
#async def on_guild_channel_update(channel):

@bot.event
async def on_guild_channel_pins_update(channel, last_pin):

@bot.event
async def on_private_channel_delete(channel):

@bot.event
async def on_private_channel_create(channel):

@bot.event
async def on_private_channel_update(before, after):

@bot.event
async def on_private_channel_pins_update(channel, last_pin):

@bot.event
async def on_group_join(channel, user):

@bot.event
async def on_group_remove(channel, user):

#@bot.event
#async def on_typing(channel, user, when):

@bot.event
async def on_settings_update():

@bot.event
async def on_guild_settings_update():

@bot.event
async def on_required_action_update():

@bot.event
async def on_payment_sources_update():

@bot.event
async def on_subscriptions_update():

@bot.event
async def on_payment_client_add():

@bot.event
async def on_payment_update():

@bot.event
async def on_premium_guild_subscription_slot_create():

@bot.event
async def on_premium_guild_subscription_slot_update():

@bot.event
async def on_billing_popup_bridge_callback():

@bot.event
async def on_library_application_update():

@bot.event
async def on_achievement_update():

@bot.event
async def on_entitlement_create():

@bot.event
async def on_entitlement_update():

@bot.event
async def on_entitlement_delete():

@bot.event
async def on_gift_create():

@bot.event
async def on_gift_update():

@bot.event
async def on_connections_update():

@bot.event
async def on_connections_create():

@bot.event
async def on_connections_delete():

@bot.event
async def on_connections_link_callback():

@bot.event
async def on_relationship_add():

@bot.event
async def on_relationship_remove():

@bot.event
async def on_relationship_update():

@bot.event
async def on_call_create():

@bot.event
async def on_call_delete():

@bot.event
async def on_call_update():

@bot.event
async def on_guild_available():

@bot.event
async def on_guild_unavailable():

@bot.event
async def on_guild_join():

@bot.event
async def on_guild_remove():

@bot.event
async def on_guild_update():

@bot.event
async def on_guild_emojis_update():

@bot.event
async def on_guild_stickers_update():

@bot.event
async def on_invite_create():

@bot.event
async def on_invite_delete():

@bot.event
async def on_integration_create():

@bot.event
async def on_integration_update():

@bot.event
async def on_guild_integrations_update():

@bot.event
async def on_webhooks_update():

@bot.event
async def on_raw_integration_delete():

@bot.event
async def on_interaction():

@bot.event
async def on_interaction_finish():

@bot.event
async def on_modal():

@bot.event
async def on_member_join():

@bot.event
async def on_member_remove():

@bot.event
async def on_member_update():

@bot.event
async def on_user_update():

@bot.event
async def on_member_ban():

@bot.event
async def on_member_unban():

@bot.event
async def on_presence_update():

@bot.event
async def on_raw_member_list_update():

#@bot.event
#async def on_message():

#@bot.event
#async def on_raw_message_edit():

#@bot.event
#async def on_raw_message_delete():

#@bot.event
#async def on_raw_bulk_message_delete():

#@bot.event
#async def on_raw_reaction_add():

#@bot.event
#async def on_raw_reaction_remove():

#@bot.event
#async def on_raw_reaction_clear():

#@bot.event
#async def on_raw_reaction_clear_emoji():

@bot.event
async def on_guild_role_create():

@bot.event
async def on_guild_role_delete():

@bot.event
async def on_guild_role_update():

@bot.event
async def on_scheduled_event_create():

@bot.event
async def on_scheduled_event_delete():

@bot.event
async def on_scheduled_event_update():

@bot.event
async def on_scheduled_event_user_add():

@bot.event
async def on_scheduled_event_user_remove():

@bot.event
async def on_stage_instance_create():

@bot.event
async def on_stage_instance_delete():

@bot.event
async def on_stage_instance_update():

@bot.event
async def on_thread_create():

@bot.event
async def on_thread_join():

@bot.event
async def on_thread_update():

@bot.event
async def on_thread_remove():

@bot.event
async def on_thread_delete():

@bot.event
async def on_thread_member_join():

@bot.event
async def on_thread_member_remove():

@bot.event
async def on_voice_state_update():
"""