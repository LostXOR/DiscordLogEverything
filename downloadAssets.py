import requests, shutil, globalVars

# Helper function to download a Discord asset
def downloadAsset(key, url, proxy_url = None):
    # Attempt download from proxy url if it exists
    if proxy_url:
        response = requests.get(proxy_url, stream = True)

    # If download from proxy url fails download from normal url
    if not proxy_url or response.status_code != 200:
        response = requests.get(url, stream = True)

    # If download was successful, save file
    if response.status_code == 200:
        with open(f"{globalVars.mediaPath}/{key}", "wb") as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)

    # if download failed, print an error
    else:
        print(f"Download failed: {url}")

# Scans the event data for assets and downloads them
def downloadAssets(socketRecvUUID, timestamp, eventJSON):
    # Makes the saveObject calls shorter
    a = socketRecvUUID
    b = timestamp
    d = eventJSON["d"]

    # Big ol' switch case for each type of event
    match eventJSON["t"]:
        case "MESSAGE_CREATE":
            for attachment in d["attachments"]:
                downloadAsset(attachment["id"], attachment["url"], attachment["proxy_url"])
        case "MESSAGE_UPDATE":
            for attachment in d["attachments"]:
                downloadAsset(attachment["id"], attachment["url"], attachment["proxy_url"])
        case "READY": pass
        case "READY_SUPPLEMENTAL": pass
        case "MESSAGE_DELETE": pass
        case "MESSAGE_DELETE_BULK": pass
        case "CHANNEL_CREATE": pass
        case "CHANNEL_DELETE": pass
        case "CHANNEL_UPDATE": pass
        case "THREAD_CREATE": pass
        case "THREAD_UPDATE": pass
        case "THREAD_DELETE": pass
        case "GUILD_CREATE": pass
        case "GUILD_UPDATE": pass
        case "GUILD_DELETE": pass
        case "GUILD_MEMBER_UPDATE": pass
        case "PRESENCE_UPDATE": pass
        case "RESUMED": pass
        case "TYPING_START": pass
        case "ACTIVITY_START": pass
        case "ACTIVITY_USER_ACTION": pass
        case "MESSAGE_ACK": pass
        case "GUILD_FEATURE_ACK": pass
        case "USER_NON_CHANNEL_ACK": pass
        case "CHANNEL_PINS_ACK": pass
        case "CHANNEL_PINS_UPDATE": pass
        case "THREAD_LIST_SYNC": pass
        case "THREAD_MEMBER_UPDATE": pass
        case "THREAD_MEMBERS_UPDATE": pass
        case "FORUM_UNREADS": pass
        case "CHANNEL_RECIPIENT_ADD": pass
        case "CHANNEL_RECIPIENT_REMOVE": pass
        case "GUILD_MEMBERS_CHUNK": pass
        case "THREAD_MEMBER_LIST_UPDATE": pass
        case "GUILD_BAN_ADD": pass
        case "GUILD_BAN_REMOVE": pass
        case "GUILD_MEMBER_ADD": pass
        case "GUILD_MEMBER_REMOVE": pass
        case "GUILD_ROLE_CREATE": pass
        case "GUILD_ROLE_UPDATE": pass
        case "GUILD_ROLE_DELETE": pass
        case "GUILD_EMOJIS_UPDATE": pass
        case "GUILD_STICKERS_UPDATE": pass
        case "GUILD_INTEGRATIONS_UPDATE": pass
        case "INTEGRATION_CREATE": pass
        case "INTEGRATION_DELETE": pass
        case "USER_UPDATE": pass
        case "USER_SETTINGS_PROTO_UPDATE": pass
        case "USER_GUILD_SETTINGS_UPDATE": pass
        case "USER_CONNECTIONS_UPDATE": pass
        case "USER_REQUIRED_ACTION_UPDATE": pass
        case "USER_NOTE_UPDATE": pass
        case "RELATIONSHIP_ADD": pass
        case "RELATIONSHIP_REMOVE": pass
        case "RELATIONSHIP_UPDATE": pass
        case "PRESENCES_REPLACE": pass
        case "SESSIONS_REPLACE": pass
        case "VOICE_STATE_UPDATE": pass
        case "LOBBY_VOICE_STATE_UPDATE": pass
        case "VOICE_SERVER_UPDATE": pass
        case "LOBBY_VOICE_SERVER_UPDATE": pass
        case "CALL_CREATE": pass
        case "CALL_UPDATE": pass
        case "CALL_DELETE": pass
        case "OAUTH2_TOKEN_REVOKE": pass
        case "RECENT_MENTION_DELETE": pass
        case "FRIEND_SUGGESTION_CREATE": pass
        case "FRIEND_SUGGESTION_DELETE": pass
        case "WEBHOOKS_UPDATE": pass
        case "BURST_CREDIT_BALANCE_UPDATE": pass
        case "MESSAGE_REACTION_ADD": pass
        case "MESSAGE_REACTION_REMOVE": pass
        case "MESSAGE_REACTION_REMOVE_ALL": pass
        case "MESSAGE_REACTION_REMOVE_EMOJI": pass
        case "PAYMENT_UPDATE": pass
        case "ENTITLEMENT_CREATE": pass
        case "ENTITLEMENT_UPDATE": pass
        case "ENTITLEMENT_DELETE": pass
        case "USER_PAYMENT_SOURCES_UPDATE": pass
        case "USER_SUBSCRIPTIONS_UPDATE": pass
        case "USER_PREMIUM_GUILD_SUBSCRIPTION_SLOT_CREATE": pass
        case "USER_PREMIUM_GUILD_SUBSCRIPTION_SLOT_UPDATE": pass
        case "BILLING_POPUP_BRIDGE_CALLBACK": pass
        case "USER_PAYMENT_CLIENT_ADD": pass
        case "GUILD_MEMBER_LIST_UPDATE": pass
        case "LOBBY_CREATE": pass
        case "LOBBY_UPDATE": pass
        case "LOBBY_DELETE": pass
        case "LOBBY_MEMBER_CONNECT": pass
        case "LOBBY_MEMBER_UPDATE": pass
        case "LOBBY_MEMBER_DISCONNECT": pass
        case "LOBBY_MESSAGE": pass
        case "GIFT_CODE_UPDATE": pass
        case "GIFT_CODE_CREATE": pass
        case "USER_ACHIEVEMENT_UPDATE": pass
        case "LIBRARY_APPLICATION_UPDATE": pass
        case "STREAM_CREATE": pass
        case "STREAM_SERVER_UPDATE": pass
        case "STREAM_UPDATE": pass
        case "STREAM_DELETE": pass
        case "GENERIC_PUSH_NOTIFICATION_SENT": pass
        case "NOTIFICATION_CENTER_ITEM_CREATE": pass
        case "NOTIFICATION_CENTER_ITEM_DELETE": pass
        case "NOTIFICATION_CENTER_ITEMS_ACK": pass
        case "NOTIFICATION_CENTER_ITEM_COMPLETED": pass
        case "APPLICATION_COMMAND_PERMISSIONS_UPDATE": pass
        case "GUILD_APPLICATION_COMMAND_INDEX_UPDATE": pass
        case "GUILD_JOIN_REQUEST_CREATE": pass
        case "GUILD_JOIN_REQUEST_UPDATE": pass
        case "GUILD_JOIN_REQUEST_DELETE": pass
        case "INTERACTION_CREATE": pass
        case "INTERACTION_SUCCESS": pass
        case "INTERACTION_FAILURE": pass
        case "APPLICATION_COMMAND_AUTOCOMPLETE_RESPONSE": pass
        case "INTERACTION_MODAL_CREATE": pass
        case "STAGE_INSTANCE_CREATE": pass
        case "STAGE_INSTANCE_UPDATE": pass
        case "STAGE_INSTANCE_DELETE": pass
        case "GUILD_SCHEDULED_EVENT_CREATE": pass
        case "GUILD_SCHEDULED_EVENT_UPDATE": pass
        case "GUILD_SCHEDULED_EVENT_DELETE": pass
        case "GUILD_SCHEDULED_EVENT_USER_ADD": pass
        case "GUILD_SCHEDULED_EVENT_USER_REMOVE": pass
        case "GUILD_DIRECTORY_ENTRY_CREATE": pass
        case "GUILD_DIRECTORY_ENTRY_UPDATE": pass
        case "GUILD_DIRECTORY_ENTRY_DELETE": pass
        case "AUTO_MODERATION_MENTION_RAID_DETECTION": pass
        case "VOICE_CHANNEL_EFFECT_SEND": pass
        case "GUILD_SOUNDBOARD_SOUND_CREATE": pass
        case "GUILD_SOUNDBOARD_SOUND_UPDATE": pass
        case "GUILD_SOUNDBOARD_SOUND_DELETE": pass
        case "EMBEDDED_ACTIVITY_UPDATE": pass
        case "AUTH_SESSION_CHANGE": pass
        case "USER_CONNECTIONS_LINK_CALLBACK": pass
        case "DELETED_ENTITY_IDS": pass
        case "CONSOLE_COMMAND_UPDATE": pass
        case "PASSIVE_UPDATE_V1": pass
        case "PRIVATE_CHANNEL_INTEGRATION_CREATE": pass
        case "PRIVATE_CHANNEL_INTEGRATION_UPDATE": pass
        case "PRIVATE_CHANNEL_INTEGRATION_DELETE": pass
        case "CREATOR_MONETIZATION_RESTRICTIONS_UPDATE": pass
        case "GUILD_AUDIT_LOG_ENTRY_CREATE": pass
        case "INTEGRATION_UPDATE": pass
        case "INVITE_CREATE": pass
        case "AUDIO_SETTINGS_UPDATE": pass
        case _:
            print(f"Event {eventJSON['t']} unknown.")
            print("Please create a bug report and include the below data. It will help to improve DiscordLogEverything.")
            print(eventJSON)