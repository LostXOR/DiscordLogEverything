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
    # TODO: Use event.data instead of fetching message
    async def on_raw_message_edit(self, event):
        eventUUID = logEvent("MessageEdit", [event.message_id])
        await saveObjectSnapshot(await self.fetchMessage(event.message_id, event.channel_id), eventUUID)

    async def on_raw_message_delete(self, event):
        eventUUID = logEvent("MessageDelete", [event.message_id])
        deleteObject(event.message_id, "Message", eventUUID)

    async def on_raw_bulk_message_delete(self, event):
        eventUUID = logEvent("BulkMessageDelete", event.message_ids + [None] * (100 - len(event.message_ids)))
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
        logEvent("Typing", [user.id, channel.id, time.mktime(when.timetuple())])

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
        # member can sometimes be a Relationship instead of a Member for some reason, it's a bug but we need to correct for it
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
    # TODO: figure out how to log this
    async def on_connections_update(self):
        eventUUID = logEvent("ConnectionsUpdate")

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

    async def on_invite_create(self, invite):
        eventUUID = logEvent("InviteCreate", [invite.id, invite.guild.id])
        await saveObjectSnapshot(invite, eventUUID)

    async def on_invite_delete(self, invite):
        eventUUID = logEvent("InviteDelete", [invite.id, invite.guild.id])
        deleteObject(invite.id, "Invite", eventUUID)

    async def on_gift_create(self, gift):
        eventUUID = logEvent("GiftCreate", [gift.id])
        await saveObjectSnapshot(gift, eventUUID)

    async def on_gift_update(self, gift):
        eventUUID = logEvent("GiftUpdate", [gift.id])
        await saveObjectSnapshot(gift, eventUUID)

    async def on_call_create(self, call):
        eventUUID = logEvent("CallCreate", [call.channel.id])

    async def on_call_delete(self, call):
        eventUUID = logEvent("CallDelete", [call.channel.id])

    async def on_call_update(self, before, call):
        eventUUID = logEvent("CallUpdate", [call.channel.id])

    async def on_interaction(self, interaction):
        eventUUID = logEvent("Interaction", [interaction.id])
        saveObjectSnapshot(interaction, eventUUID)

    async def on_interaction_finish(self, interaction):
        eventUUID = logEvent("InteractionFinish", [interaction.id])
        saveObjectSnapshot(interaction, eventUUID)

    async def on_stage_instance_create(self, stage):
        eventUUID = logEvent("StageInstanceCreate", [stage.id])
        await saveObjectSnapshot(stage, eventUUID)

    async def on_stage_instance_delete(self, stage):
        eventUUID = logEvent("StageInstanceDelete", [stage.id])
        await deleteObject(stage.id, "StageInstance", eventUUID)

    async def on_stage_instance_update(self, stage):
        eventUUID = logEvent("StageInstanceUpdate", [stage.id])
        await saveObjectSnapshot(stage, eventUUID)

    async def on_premium_guild_subscription_slot_create(self, slot):
        eventUUID = logEvent("PremiumGuildSubscriptionSlotCreate", [slot.id])
        await saveObjectSnapshot(slot, eventUUID)

    async def on_premium_guild_subscription_slot_update(self, slot):
        eventUUID = logEvent("PremiumGuildSubscriptionSlotUpdate", [slot.id])
        await saveObjectSnapshot(slot, eventUUID)

    async def on_achievement_update(self, achievement, percent_complete):
        eventUUID = logEvent("AchievementUpdate", [achievement.id, percent_complete])
        await saveObjectSnapshot(achievement, eventUUID)

    async def on_entitlement_create(self, entitlement):
        eventUUID = logEvent("EntitlementCreate", [entitlement.id])
        await saveObjectSnapshot(entitlement, eventUUID)

    async def on_entitlement_update(self, entitlement):
        eventUUID = logEvent("EntitlementUpdate", [entitlement.id])
        await saveObjectSnapshot(entitlement, eventUUID)

    async def on_entitlement_delete(self, entitlement):
        eventUUID = logEvent("EntitlementDelete", [entitlement.id])
        await deleteObjectSnapshot(entitlement.id, "Entitlement", eventUUID)

    async def on_modal(self, modal):
        eventUUID = logEvent("Modal", [modal.id])
        await saveObjectSnapshot(modal, eventUUID)

    async def on_integration_create(self, integration):
        eventUUID = logEvent("IntegrationCreate", [integration.id])
        await saveObjectSnapshot(integration, eventUUID)

    async def on_integration_update(self, integration):
        eventUUID = logEvent("IntegrationUpdate", [integration.id])
        await saveObjectSnapshot(integration, eventUUID)

    async def on_raw_integration_delete(self, event):
        eventUUID = logEvent("IntegrationDelete", [event.integration_id])
        await deleteObject(event.integration_id, "Integration", eventUUID)

    async def on_guild_integrations_update(self, guild):
        eventUUID = logEvent("GuildIntegrationsUpdate", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

    async def on_webhooks_update(self, channel):
        eventUUID = logEvent("WebhooksUpdate", [channel.id])
        await saveObjectSnapshot(channel, eventUUID)
    # TODO: Save before state in event?
    async def on_voice_state_update(self, member, before, voiceState):
        eventUUID = logEvent("VoiceStateUpdate", [member.id])
        await saveObjectSnapshot(member, eventUUID)

    async def on_billing_popup_bridge_callback(self, paymentSourceType, path, query, state):
        eventUUID = logEvent("BillingPopupBridgeCallback", [str(paymentSourceType), path, query, state])

    async def on_guild_stickers_update(guild, before, stickers):
        eventUUID = logEvent("GuildStickersUpdate", [guild.id])
        await saveObjectSnapshot(guild, eventUUID)

# on_library_application_update may be added in the future