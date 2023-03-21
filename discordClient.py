import discord, time
from saveObjectSnapshot import saveObjectSnapshot
from deleteObject import deleteObject
from logEvent import logEvent

class discordClient(discord.Client):

    # Helper function to make it easier to fetch a message from message and channel IDs
    async def fetchMessage(self, messageID, channelID):
        channel = await self.fetch_channel(channelID)
        return await channel.fetch_message(messageID)

    async def on_ready(self):
        print("Connected to Discord.")
        # Snapshot guilds (also snapshots channels and members by recursion)
        for guild in self.guilds:
            await saveObjectSnapshot(guild)

    # Events to be logged
    # Each function is very similar, but slightly too different to wrap as one function.
    # If you think you can do better, go ahead and make a pull request. :)
    async def on_message(self, message):
        eventUUID = logEvent("Message", [message.id])
        await saveObjectSnapshot(message, eventUUID)

    async def on_raw_message_edit(self, event):
        eventUUID = logEvent("MessageEdit", [event.message_id])
        await saveObjectSnapshot(await self.fetchMessage(event.message_id, event.channel_id), eventUUID)

    async def on_raw_message_delete(self, event):
        eventUUID = logEvent("MessageDelete", [event.message_id])
        deleteObject(event.message_id, "Message", eventUUID)

    async def on_raw_bulk_message_delete(self, event):
        eventUUID = logEvent("BulkMessageDelete", [",".join(map(str, event.message_ids))])
        for id in event.message_ids: deleteObject(id, "Message", eventUUID)

    async def on_raw_reaction_add(self, event):
        eventUUID = logEvent("ReactionAdd", [event.emoji.id, event.message_id, event.user_id])
        await saveObjectSnapshot(await self.fetchMessage(event.message_id, event.channel_id), eventUUID)

    async def on_raw_reaction_remove(self, event):
        eventUUID = logEvent("ReactionRemove", [event.emoji.id, event.message_id, event.user_id])
        await saveObjectSnapshot(await self.fetchMessage(event.message_id, event.channel_id), eventUUID)

    async def on_raw_reaction_clear(self, event):
        eventUUID = logEvent("ReactionClear", [event.message_id])
        await saveObjectSnapshot(await self.fetchMessage(event.message_id, event.channel_id), eventUUID)

    async def on_raw_reaction_clear_emoji(self, event):
        eventUUID = logEvent("ReactionClear", [event.emoji_id, event.message_id])
        await saveObjectSnapshot(await self.fetchMessage(event.message_id, event.channel_id), eventUUID)

    async def on_guild_channel_delete(self, channel):
        eventUUID = logEvent("GuildChannelDelete", [channel.id])
        deleteObject(channel.id, type(channel).__name__, eventUUID)

    async def on_guild_channel_create(self, channel):
        eventUUID = logEvent("GuildChannelCreate", [channel.id])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_guild_channel_update(self, before, channel):
        eventUUID = logEvent("GuildChannelUpdate", [channel.id])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_private_channel_delete(self, channel):
        eventUUID = logEvent("PrivateChannelDelete", [channel.id])
        deleteObject(channel.id, type(channel).__name__, eventUUID)

    async def on_private_channel_create(self, channel):
        eventUUID = logEvent("PrivateChannelCreate", [channel.id])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_private_channel_update(self, before, channel):
        eventUUID = logEvent("PrivateChannelUpdate", [channel.id])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_guild_channel_pins_update(self, channel, last_pin):
        lastPin = time.mktime(last_pin.timetuple()) if last_pin else None
        eventUUID = logEvent("GuildChannelPinsUpdate", [channel.id, lastPin])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_private_channel_pins_update(self, channel, last_pin):
        lastPin = time.mktime(last_pin.timetuple()) if last_pin else None
        eventUUID = logEvent("PrivateChannelPinsUpdate", [channel.id, lastPin])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_typing(self, channel, user, when):
        eventUUID = logEvent("Typing", [user.id, channel.id, time.mktime(when.timetuple())])

    async def on_group_join(self, channel, user):
        eventUUID = logEvent("GroupJoin", [user.id, channel.id])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_group_remove(self, channel, user):
        eventUUID = logEvent("GroupRemove", [user.id, channel.id])
        await saveObjectSnapshot(channel, eventUUID)

    async def on_guild_join(self, guild):
        eventUUID = logEvent("GuildJoin", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_guild_remove(self, guild):
        eventUUID = logEvent("GuildRemove", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_guild_update(self, before, guild):
        eventUUID = logEvent("GuildUpdate", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_presence_update(self, before, member):
        # member can sometimes be a Relationship instead of a Member for some reason, idk why but we need to correct for it
        if type(member).__name__ == "Relationship":
            member = member.user
        eventUUID = logEvent("PresenceUpdate", [member.id])
        await saveObjectSnapshot(member, eventUUID)

    async def on_settings_update(self, before, settings):
        eventUUID = logEvent("SettingsUpdate")
        # saveObjectSnapshot needs an ID, so make a dummy one
        settings.id = None
        await saveObjectSnapshot(settings, eventUUID)

    async def on_guild_settings_update(self, before, settings):
        eventUUID = logEvent("GuildSettingsUpdate", [settings.guild.id])
        await saveObjectSnapshot(settings.guild, eventUUID)

    async def on_guild_available(self, guild):
        eventUUID = logEvent("GuildAvailable", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_guild_unavailable(self, guild):
        eventUUID = logEvent("GuildUnavailable", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_guild_emojis_update(self, guild, before, after):
        eventUUID = logEvent("GuildEmojisUpdate", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_member_join(self, member):
        eventUUID = logEvent("MemberJoin", [member.id, member.guild.id])
        await saveObjectSnapshot(member, eventUUID)

    async def on_member_remove(self, member):
        eventUUID = logEvent("MemberRemove", [member.id, member.guild.id])
        await saveObjectSnapshot(member, eventUUID)

    async def on_member_update(self, before, member):
        eventUUID = logEvent("MemberUpdate", [member.id, member.guild.id])
        await saveObjectSnapshot(member, eventUUID)

    async def on_user_update(self, before, user):
        eventUUID = logEvent("UserUpdate", [user.id])
        await saveObjectSnapshot(user, eventUUID)

    async def on_guild_role_create(self, role):
        eventUUID = logEvent("GuildRoleCreate", [role.id])
        await saveObjectSnapshot(role, eventUUID)

    async def on_guild_role_delete(self, role):
        eventUUID = logEvent("GuildRoleDelete", [role.id])
        deleteObject(role.id, "Role", eventUUID)

    async def on_guild_role_update(self, before, role):
        eventUUID = logEvent("GuildRoleUpdate", [role.id])
        await saveObjectSnapshot(role, eventUUID)

    async def on_thread_create(self, thread):
        eventUUID = logEvent("ThreadCreate", [thread.id])
        await saveObjectSnapshot(thread, eventUUID)

    async def on_thread_join(self, thread):
        eventUUID = logEvent("ThreadJoin", [thread.id])
        await saveObjectSnapshot(thread, eventUUID)

    async def on_thread_update(self, before, thread):
        eventUUID = logEvent("ThreadUpdate", [thread.id])
        await saveObjectSnapshot(thread, eventUUID)

    async def on_thread_remove(self, thread):
        eventUUID = logEvent("ThreadRemove", [thread.id])
        await saveObjectSnapshot(thread, eventUUID)

    async def on_thread_delete(self, thread):
        eventUUID = logEvent("ThreadDelete", [thread.id])
        deleteObjectSnapshot(thread.id, "Thread", eventUUID)

    async def on_thread_member_join(self, threadMember):
        eventUUID = logEvent("ThreadMemberJoin", [threadMember.id, threadMember.thread_id])
        await saveObjectSnapshot(threadMember, eventUUID)

    async def on_thread_member_remove(self, threadMember):
        eventUUID = logEvent("ThreadMemberRemove", [threadMember.id, threadMember.thread_id])
        await saveObjectSnapshot(threadMember, eventUUID)

    async def on_relationship_add(self, relationship):
        eventUUID = logEvent("RelationshipAdd", [relationship.id, relationship.user.id])
        await saveObjectSnapshot(relationship, eventUUID)

    async def on_relationship_remove(self, relationship):
        eventUUID = logEvent("RelationshipRemove", [relationship.id, relationship.user.id])
        await saveObjectSnapshot(relationship, eventUUID)

    async def on_relationship_update(self, before, relationship):
        eventUUID = logEvent("RelationshipUpdate", [relationship.id, relationship.user.id])
        await saveObjectSnapshot(relationship, eventUUID)

    async def on_connections_update(self):
        eventUUID = logEvent("ConnectionsUpdate")
        # Not sure how to log this...

    async def on_connection_update(self, before, connection):
        eventUUID = logEvent("ConnectionUpdate", [connection.url, connection.show_activity, connection.revoked])

    async def on_connection_create(self, connection):
        eventUUID = logEvent("ConnectionCreate", [connection.url, connection.show_activity, connection.revoked])

    async def on_connections_link_callback(self, provider, code, state):
        eventUUID = logEvent("ConnectionsLinkCallback", [provider, code, state])

    async def on_scheduled_event_create(self, event):
        eventUUID = logEvent("ScheduledEventCreate", [event.id])
        await saveObjectSnapshot(event, eventUUID)

    async def on_scheduled_event_delete(self, event):
        eventUUID = logEvent("ScheduledEventDelete", [event.id])
        deleteObject(event.id, "ScheduledEvent", eventUUID)

    async def on_scheduled_event_update(self, before, event):
        eventUUID = logEvent("ScheduledEventUpdate", [event.id])
        await saveObjectSnapshot(event, eventUUID)

    async def on_scheduled_event_user_add(self, event, user):
        eventUUID = logEvent("ScheduledEventUserAdd", [user.id, event.id])
        await saveObjectSnapshot(event, eventUUID)

    async def on_scheduled_event_user_remove(self, event, user):
        eventUUID = logEvent("ScheduledEventUserRemove", [user.id, event.id])
        await saveObjectSnapshot(event, eventUUID)

    async def on_member_ban(self, guild, user):
        eventUUID = logEvent("MemberBan", [user.id, guild.id])
        await saveObjectSnapshot(user, eventUUID)

    async def on_member_unban(self, guild, user):
        eventUUID = logEvent("MemberUnban", [user.id, guild.id])
        await saveObjectSnapshot(user, eventUUID)

    # These are difficult or impossible to test
    async def on_required_action_update(self, action):
        eventUUID = logEvent("RequiredActionUpdate", [str(action)])

    async def on_payment_sources_update(self):
        eventUUID = logEvent("PaymentSourcesUpdate")

    async def on_subscriptions_update(self):
        eventUUID = logEvent("SubscriptionsUpdate")

    async def on_payment_client_add(self, tokenHash, expires):
        eventUUID = logEvent("PaymentClientAdd", [tokenHash, time.mktime(expires.timetuple())])

    async def on_payment_update(self, payment):
        eventUUID = logEvent("PaymentUpdate", [payment.id])
        await saveObjectSnapshot(payment, eventUUID)
    # End of difficult or impossible to test

"""
To be added
async def on_premium_guild_subscription_slot_create():
async def on_premium_guild_subscription_slot_update():
async def on_billing_popup_bridge_callback():
async def on_library_application_update():
async def on_achievement_update():
async def on_entitlement_create():
async def on_entitlement_update():
async def on_entitlement_delete():
async def on_gift_create():
async def on_gift_update():
async def on_call_create():
async def on_call_delete():
async def on_call_update():
async def on_guild_stickers_update():
async def on_invite_create():
async def on_invite_delete():
async def on_integration_create():
async def on_integration_update():
async def on_guild_integrations_update():
async def on_webhooks_update():
async def on_raw_integration_delete():
async def on_interaction():
async def on_interaction_finish():
async def on_modal():
async def on_raw_member_list_update():
async def on_stage_instance_create():
async def on_stage_instance_delete():
async def on_stage_instance_update():
async def on_voice_state_update():
Not much left, yay!
"""