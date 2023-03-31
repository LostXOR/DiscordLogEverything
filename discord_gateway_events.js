// This file contains some code ripped from Discord that seems to be part of the inital processing of gateway events.
// It gives a list of all the events and roughly their parameters, so it'll be useful when writing event handling code.
// This code never actually gets ran when running DiscordLogEverything.

switch () {
    case "READY_SUPPLEMENTAL":
        O.Z.readySupplemental.measure((function() {
            i.ZP.Emitter.batched((function() {
                t = O.Z.hydrateReadySupplemental.measure((function() {
                    return function(e) {
                        var t = e.guilds,
                            n = e.merged_members,
                            r = e.merged_presences,
                            o = Ze(e, ["guilds", "merged_members", "merged_presences"]),
                            i = ze(We, null == r ? void 0 : r.friends),
                            a = null == t ? void 0 : t.map((function(e, t) {
                                var o = ze(We, null == r ? void 0 : r.guilds[t]),
                                    i = ze(We, null == n ? void 0 : n[t]);
                                return Ye(Fe({}, e), {
                                    unavailable: void 0 === e.voice_states,
                                    presences: o,
                                    members: i
                                })
                            }));
                        We = {};
                        return Ye(Fe({}, o), {
                            presences: i,
                            guilds: null != a ? a : []
                        })
                    }(t)
                }));
                var e = function(e) {
                        return e.map((function(e) {
                            return {
                                user: e.user,
                                status: e.status,
                                clientStatus: e.client_status,
                                activities: e.activities
                            }
                        }))
                    },
                    n = t.guilds.filter((function(e) {
                        return !0 !== e.unavailable
                    }));
                n.forEach((function(t) {
                    t.presences = e(t.presences || [])
                }));
                var r, o = t.presences ? e(t.presences) : [],
                    i = (null !== (r = t.lazy_private_channels) && void 0 !== r ? r : []).map((function(e) {
                        return (0, Le.q_)(e)
                    }));
                O.Z.dispatchReadySupplemental.measure((function() {
                    Vt({
                        type: "CONNECTION_OPEN_SUPPLEMENTAL",
                        guilds: n,
                        presences: o,
                        lazyPrivateChannels: i
                    })
                }));
                var a = [];
                n.forEach((function(e) {
                    e.voice_states.forEach((function(t) {
                        var n;
                        a.push({
                            userId: t.user_id,
                            guildId: e.id,
                            sessionId: t.session_id,
                            channelId: t.channel_id,
                            mute: t.mute,
                            deaf: t.deaf,
                            selfMute: t.self_mute,
                            selfDeaf: t.self_deaf,
                            selfVideo: t.self_video || !1,
                            suppress: t.suppress,
                            selfStream: t.self_stream || !1,
                            requestToSpeakTimestamp: null !== (n = t.request_to_speak_timestamp) && void 0 !== n ? n : null
                        })
                    }))
                }));
                Vt({
                    type: "VOICE_STATE_UPDATES",
                    voiceStates: a,
                    initial: !0
                });
                Gt.update();
                kt.update({}, !0);
                null != t.disclose && t.disclose.includes("pomelo") && Vt({
                    type: "DISCLOSE_UPDATE",
                    disclose: t.disclose
                })
            }))
        }));
        setTimeout((function() {
            return Vt({
                type: "POST_CONNECTION_OPEN"
            })
        }), 2e3);
        break;
    case "READY":
        if (t.user.bot) {
            Vt({
                type: "LOGOUT"
            });
            return
        }
        O.Z.ready.measure((function() {
            i.ZP.Emitter.batched((function() {
                var e = (t = O.Z.hydrateReady.measure((function() {
                        return Ke(t)
                    }))).private_channels.map((function(e) {
                        return (0, Le.q_)(e)
                    })),
                    n = t.guilds.filter((function(e) {
                        return e.unavailable
                    })).map((function(e) {
                        return e.id
                    })),
                    r = t.guilds.filter((function(e) {
                        return !0 !== e.unavailable
                    }));
                r.forEach((function(e) {
                    e.presences = []
                }));
                var o = null == t.user_settings_proto ? void 0 : (0, Ce.ac)(t.user_settings_proto);
                0;
                O.Z.dispatchReady.measure((function() {
                    var i;
                    Vt({
                        type: "CONNECTION_OPEN",
                        sessionId: t.session_id,
                        authSessionIdHash: t.auth_session_id_hash,
                        user: t.user,
                        users: t.users,
                        guilds: r,
                        initialPrivateChannels: e,
                        unavailableGuilds: n,
                        readState: t.read_state,
                        userGuildSettings: t.user_guild_settings,
                        tutorial: t.tutorial,
                        relationships: t.relationships,
                        friendSuggestionCount: t.friend_suggestion_count,
                        presences: t.presences,
                        analyticsToken: t.analytics_token,
                        experiments: t.experiments,
                        connectedAccounts: t.connected_accounts,
                        guildExperiments: t.guild_experiments,
                        requiredAction: t.required_action,
                        consents: t.consents,
                        sessions: Bt(t.sessions || []),
                        pendingPayments: t.pending_payments,
                        countryCode: null !== (i = t.country_code) && void 0 !== i ? i : void 0,
                        guildJoinRequests: t.guild_join_requests || [],
                        userSettingsProto: o,
                        apiCodeVersion: t.api_code_version
                    })
                }));
                null != t.auth_token && Vt({
                    type: "UPDATE_TOKEN",
                    token: t.auth_token,
                    userId: t.user.id
                });
                Ut.update();
                Gt.update();
                kt.update();
                jt()
            }))
        }));
        break;
    case "RESUMED":
        Ut.forceUpdate();
        Gt.forceUpdate();
        kt.forceUpdate();
        jt();
        Vt({
            type: "CONNECTION_RESUMED"
        });
        break;
    case "TYPING_START": // Done
        null != t.member && Rt(t.guild_id, t.member.user, t.member);
        Vt({
            type: "TYPING_START",
            channelId: t.channel_id,
            userId: t.user_id
        });
        break;
    case "ACTIVITY_START":
        Vt({
            type: "ACTIVITY_START",
            userId: t.user_id,
            activity: t.activity
        });
        break;
    case "ACTIVITY_USER_ACTION":
        Vt({
            type: "ACTIVITY_USER_ACTION",
            actionType: t.action_type,
            user: t.user,
            applicationId: t.application_id,
            channelId: t.channel_id,
            messageId: t.message_id
        });
        break;
    case "MESSAGE_CREATE": // Done
        Ct(t);
        null != t.author && Vt({
            type: "MESSAGE_CREATE",
            guildId: t.guild_id,
            channelId: t.channel_id,
            message: t,
            optimistic: !1,
            isPushNotification: !1
        });
        break;
    case "MESSAGE_UPDATE": // Done
        Ct(t);
        Vt({
            type: "MESSAGE_UPDATE",
            guildId: t.guild_id,
            message: t
        });
        break;
    case "MESSAGE_DELETE": // Done
        Vt({
            type: "MESSAGE_DELETE",
            guildId: t.guild_id,
            id: t.id,
            channelId: t.channel_id
        });
        break;
    case "MESSAGE_DELETE_BULK": // Done
        Vt({
            type: "MESSAGE_DELETE_BULK",
            guildId: t.guild_id,
            ids: t.ids,
            channelId: t.channel_id
        });
        break;
    case "MESSAGE_ACK":
        Vt({
            type: "MESSAGE_ACK",
            channelId: t.channel_id,
            messageId: t.message_id,
            manual: t.manual,
            newMentionCount: t.mention_count,
            version: t.version
        });
        break;
    case "GUILD_FEATURE_ACK":
        Vt({
            type: "GUILD_FEATURE_ACK",
            id: t.resource_id,
            ackType: t.ack_type,
            ackedId: t.entity_id
        });
        break;
    case "USER_NON_CHANNEL_ACK":
        Vt({
            type: "USER_NON_CHANNEL_ACK",
            ackType: t.ack_type,
            ackedId: t.entity_id
        });
        break;
    case "CHANNEL_PINS_ACK":
        Vt({
            type: "CHANNEL_PINS_ACK",
            channelId: t.channel_id,
            timestamp: t.timestamp,
            version: t.version
        });
        break;
    case "CHANNEL_PINS_UPDATE":
        Vt({
            type: "CHANNEL_PINS_UPDATE",
            channelId: t.channel_id,
            lastPinTimestamp: t.last_pin_timestamp
        });
        break;
    case "CHANNEL_CREATE": // Done
    case "CHANNEL_DELETE": // Done
        Vt({
            type: e,
            channel: (0, Le.q_)(t)
        });
        break;
    case "CHANNEL_UPDATE": // Done
        Ft.add(t);
        break;
    case "THREAD_CREATE":
    case "THREAD_UPDATE":
    case "THREAD_DELETE":
        var r = t.newly_created,
            a = vt(t, ["newly_created"]);
        Vt({
            type: e,
            isNewlyCreated: r,
            channel: (0, Le.q_)(a)
        });
        break;
    case "THREAD_LIST_SYNC":
        Vt({
            type: "THREAD_LIST_SYNC",
            guildId: t.guild_id,
            threads: t.threads.map((function(e) {
                var t = ke.Z.getChannel(e.parent_id);
                if (null != t) {
                    e.nsfw = t.nsfw;
                    e.parentChannelThreadType = t.type
                }
                return (0, Le.q_)(e)
            })),
            mostRecentMessages: t.most_recent_messages,
            members: t.members ? o().map(t.members, Re.Z) : void 0,
            channelIds: t.channel_ids
        });
        break;
    case "THREAD_MEMBER_UPDATE":
        Vt({
            type: "THREAD_MEMBER_UPDATE",
            id: t.id,
            guildId: t.guild_id,
            userId: t.user_id,
            flags: t.flags,
            muted: t.muted,
            muteConfig: t.mute_config,
            joinTimestamp: t.join_timestamp
        });
        break;
    case "THREAD_MEMBERS_UPDATE":
        var l;
        Vt({
            type: "THREAD_MEMBERS_UPDATE",
            id: t.id,
            guildId: t.guild_id,
            memberCount: t.member_count,
            addedMembers: null === (l = t.added_members) || void 0 === l ? void 0 : l.map((function(e) {
                return {
                    id: e.id,
                    guildId: t.guild_id,
                    userId: e.user_id,
                    flags: e.flags,
                    joinTimestamp: e.join_timestamp
                }
            })),
            removedMemberIds: t.removed_member_ids,
            memberIdsPreview: t.member_ids_preview
        });
        break;
    case "FORUM_UNREADS":
        if (t.permission_denied) break;
        Vt({
            type: "FORUM_UNREADS",
            channelId: t.channel_id,
            threads: t.threads.map((function(e) {
                return {
                    threadId: e.thread_id,
                    missing: e.missing,
                    count: e.count
                }
            }))
        });
        break;
    case "CHANNEL_RECIPIENT_ADD":
    case "CHANNEL_RECIPIENT_REMOVE":
        Vt({
            type: e,
            channelId: t.channel_id,
            user: t.user,
            nick: t.nick
        });
        break;
    case "GUILD_CREATE":
        if (t.unavailable) Vt({
            type: "GUILD_UNAVAILABLE",
            guildId: t.id
        });
        else {
            var f, d = function(e) {
                var t, n, r, o, i, a, s, u = Xe(e.id);
                if ("partial" !== e.data_mode) {
                    var c, l;
                    return {
                        id: e.id,
                        application_command_counts: e.application_command_counts,
                        emojis: e.emojis,
                        guild_scheduled_events: e.guild_scheduled_events,
                        joined_at: e.joined_at,
                        member_count: e.member_count,
                        members: e.members,
                        premium_subscription_count: e.premium_subscription_count,
                        properties: e.properties,
                        roles: e.roles,
                        stage_instances: e.stage_instances,
                        stickers: e.stickers,
                        threads: null !== (l = null === (c = e.threads) || void 0 === c ? void 0 : c.map((function(t) {
                            return (0, Le.q_)(t, e.id)
                        }))) && void 0 !== l ? l : [],
                        channels: e.channels.map((function(t) {
                            t.guild_id = e.id;
                            return (0, Le.q_)(t, e.id)
                        })),
                        presences: e.presences,
                        embedded_activities: e.embedded_activities,
                        voice_states: e.voice_states,
                        version: e.version
                    }
                }
                if (null == u) throw Error("Guild data was missing from store, but hash was still available.");
                return {
                    id: e.id,
                    application_command_counts: e.application_command_counts,
                    channels: Je(u, e),
                    embedded_activities: e.embedded_activities,
                    emojis: null == u.emojis ? null : $e(u.emojis, e.partial_updates.emojis, e.partial_updates.deleted_emoji_ids),
                    emojiUpdates: {
                        writes: null !== (n = e.partial_updates.emojis) && void 0 !== n ? n : [],
                        deletes: null !== (r = e.partial_updates.deleted_emoji_ids) && void 0 !== r ? r : []
                    },
                    guild_scheduled_events: e.guild_scheduled_events,
                    joined_at: e.joined_at,
                    member_count: e.member_count,
                    members: e.members,
                    premium_subscription_count: e.premium_subscription_count,
                    presences: e.presences,
                    properties: null !== (o = e.properties) && void 0 !== o ? o : u.properties,
                    roles: et(e.id, u.roles, e.partial_updates.roles, e.partial_updates.deleted_role_ids),
                    stage_instances: e.stage_instances,
                    stickers: null == u.stickers ? null : $e(u.stickers, e.partial_updates.stickers, e.partial_updates.deleted_sticker_ids),
                    stickerUpdates: {
                        writes: null !== (i = e.partial_updates.stickers) && void 0 !== i ? i : [],
                        deletes: null !== (a = e.partial_updates.deleted_sticker_ids) && void 0 !== a ? a : []
                    },
                    unableToSyncDeletes: e.unable_to_sync_deletes,
                    threads: null !== (s = null === (t = e.threads) || void 0 === t ? void 0 : t.map((function(t) {
                        return (0, Le.q_)(t, e.id)
                    }))) && void 0 !== s ? s : [],
                    voice_states: e.voice_states,
                    version: e.version
                }
            }(t);
            s.Z.createGuild(d);
            Vt({
                type: "VOICE_STATE_UPDATES",
                voiceStates: d.voice_states.map((function(e) {
                    return {
                        userId: e.user_id,
                        guildId: d.id,
                        sessionId: e.session_id,
                        channelId: e.channel_id,
                        mute: e.mute,
                        deaf: e.deaf,
                        selfMute: e.self_mute,
                        selfDeaf: e.self_deaf,
                        selfVideo: e.self_video || !1,
                        suppress: e.suppress,
                        selfStream: e.self_stream || !1,
                        requestToSpeakTimestamp: null !== (f = e.request_to_speak_timestamp) && void 0 !== f ? f : null
                    }
                }))
            })
        }
        break;
    case "GUILD_UPDATE":
        Vt({
            type: "GUILD_UPDATE",
            guild: t
        });
        t.unavailable && Vt({
            type: "GUILD_UNAVAILABLE",
            guildId: t.id
        });
        break;
    case "GUILD_DELETE":
        Vt({
            type: "GUILD_DELETE",
            guild: t
        });
        t.unavailable && Vt({
            type: "GUILD_UNAVAILABLE",
            guildId: t.id
        });
        break;
    case "GUILD_MEMBERS_CHUNK":
        i.ZP.Emitter.batched((function() {
            Vt({
                type: "GUILD_MEMBERS_CHUNK",
                guildId: t.guild_id,
                members: t.members,
                notFound: t.not_found
            });
            null != t.presences && t.presences.forEach((function(e) {
                var n = e.user,
                    r = e.status,
                    o = e.client_status,
                    i = e.activities;
                return Zt(t.guild_id, n, r, i, o)
            }));
            Ht.flush()
        }));
        break;
    case "THREAD_MEMBER_LIST_UPDATE":
        i.ZP.Emitter.batched((function() {
            Vt({
                type: "THREAD_MEMBER_LIST_UPDATE",
                guildId: t.guild_id,
                threadId: t.thread_id,
                members: t.members
            });
            null != t.presences && t.presences.forEach((function(e) {
                var n = e.user,
                    r = e.status,
                    o = e.client_status,
                    i = e.activities;
                return Zt(t.guild_id, n, r, i, o)
            }));
            Ht.flush()
        }));
        break;
    case "GUILD_BAN_ADD":
    case "GUILD_BAN_REMOVE":
    case "GUILD_MEMBER_ADD":
    case "GUILD_MEMBER_UPDATE":
    case "GUILD_MEMBER_REMOVE":
        Vt({
            type: e,
            guildId: t.guild_id,
            user: t.user,
            avatar: t.avatar,
            roles: t.roles,
            nick: t.nick,
            premiumSince: t.premium_since,
            isPending: t.pending,
            joinedAt: t.joined_at,
            communicationDisabledUntil: t.communication_disabled_until,
            flags: t.flags
        });
        break;
    case "GUILD_ROLE_CREATE":
    case "GUILD_ROLE_UPDATE":
        Vt({
            type: e,
            guildId: t.guild_id,
            role: t.role
        });
        break;
    case "GUILD_ROLE_DELETE":
        Vt({
            type: "GUILD_ROLE_DELETE",
            guildId: t.guild_id,
            roleId: t.role_id,
            version: t.version
        });
        break;
    case "GUILD_EMOJIS_UPDATE":
        Vt({
            type: "GUILD_EMOJIS_UPDATE",
            guildId: t.guild_id,
            emojis: t.emojis
        });
        break;
    case "GUILD_STICKERS_UPDATE":
        Vt({
            type: "GUILD_STICKERS_UPDATE",
            guildId: t.guild_id,
            stickers: t.stickers
        });
        break;
    case "GUILD_INTEGRATIONS_UPDATE":
        Vt({
            type: "GUILD_INTEGRATIONS_UPDATE",
            guildId: t.guild_id
        });
        break;
    case "INTEGRATION_CREATE":
        Vt({
            type: "INTEGRATION_CREATE",
            application: t.application,
            guildId: t.guild_id
        });
        break;
    case "INTEGRATION_DELETE":
        Vt({
            type: "INTEGRATION_DELETE",
            applicationId: t.application_id,
            guildId: t.guild_id
        });
        break;
    case "USER_UPDATE":
        Vt({
            type: "CURRENT_USER_UPDATE",
            user: t
        });
        break;
    case "USER_SETTINGS_PROTO_UPDATE":
        var _ = (0, Ce.kI)(t.settings.type, t.settings.proto);
        if (null == _) break;
        if ("string" == typeof _) {
            console.error("Invalid proto: |".concat(_, "| |").concat(t.settings.proto, "|"));
            console.error({
                parsed: _,
                wire: t.settings.proto,
                type: t.settings.type
            });
            throw Error("UserSettingsProto must not be a string")
        }
        Vt({
            type: "USER_SETTINGS_PROTO_UPDATE",
            settings: {
                proto: _,
                type: t.settings.type
            },
            partial: t.partial
        });
        break;
    case "USER_GUILD_SETTINGS_UPDATE":
        Vt({
            type: "USER_GUILD_SETTINGS_FULL_UPDATE",
            userGuildSettings: [t]
        });
        break;
    case "USER_CONNECTIONS_UPDATE":
        Vt({
            type: "USER_CONNECTIONS_UPDATE"
        });
        break;
    case "USER_REQUIRED_ACTION_UPDATE":
        Vt({
            type: "USER_REQUIRED_ACTION_UPDATE",
            requiredAction: t.required_action
        });
        break;
    case "USER_NOTE_UPDATE":
        Vt(Tt({
            type: "USER_NOTE_UPDATE"
        }, t));
        break;
    case "RELATIONSHIP_ADD":
        Vt({
            type: "RELATIONSHIP_ADD",
            relationship: {
                id: t.id,
                type: t.type,
                user: t.user,
                since: t.since,
                nickname: t.nickname
            },
            shouldNotify: !0 === t.should_notify
        });
        break;
    case "RELATIONSHIP_REMOVE":
        Vt({
            type: "RELATIONSHIP_REMOVE",
            relationship: t
        });
        break;
    case "RELATIONSHIP_UPDATE":
        Vt({
            type: "RELATIONSHIP_UPDATE",
            relationship: t
        });
        break;
    case "PRESENCE_UPDATE":
        Zt(t.guild_id, t.user, t.status, t.activities, t.client_status);
        break;
    case "PRESENCES_REPLACE":
        Vt({
            type: "PRESENCES_REPLACE",
            presences: t
        });
        break;
    case "SESSIONS_REPLACE":
        Vt({
            type: "SESSIONS_REPLACE",
            sessions: Bt(t)
        });
        break;
    case "VOICE_STATE_UPDATE":
        null != t.member && Rt(t.guild_id, t.member.user, t.member);
        var p;
        Vt({
            type: "VOICE_STATE_UPDATES",
            voiceStates: [{
                userId: t.user_id,
                guildId: t.guild_id,
                sessionId: t.session_id,
                channelId: t.channel_id,
                mute: t.mute,
                deaf: t.deaf,
                selfMute: t.self_mute,
                selfDeaf: t.self_deaf,
                selfVideo: t.self_video || !1,
                suppress: t.suppress,
                selfStream: t.self_stream || !1,
                requestToSpeakTimestamp: null !== (p = t.request_to_speak_timestamp) && void 0 !== p ? p : null,
                oldChannelId: lt.Z.getUserVoiceChannelId(t.guild_id, t.user_id)
            }]
        });
        break;
    case "LOBBY_VOICE_STATE_UPDATE":
        Vt({
            type: "LOBBY_VOICE_STATE_UPDATE",
            userId: t.user_id,
            lobbyId: t.lobby_id,
            sessionId: t.session_id,
            channelId: t.channel_id,
            mute: t.mute,
            deaf: t.deaf,
            selfMute: t.self_mute,
            selfDeaf: t.self_deaf
        });
        break;
    case "VOICE_SERVER_UPDATE":
        Vt({
            type: "VOICE_SERVER_UPDATE",
            guildId: t.guild_id,
            channelId: t.channel_id,
            endpoint: t.endpoint,
            token: t.token
        });
        break;
    case "LOBBY_VOICE_SERVER_UPDATE":
        Vt({
            type: "LOBBY_VOICE_SERVER_UPDATE",
            lobbyId: t.lobby_id,
            endpoint: t.endpoint,
            token: t.token
        });
        break;
    case "CALL_CREATE":
        Vt({
            type: "CALL_CREATE",
            channelId: t.channel_id,
            messageId: t.message_id,
            embeddedActivities: t.embedded_activities,
            region: t.region,
            ringing: t.ringing
        });
        var E = t.voice_states;
        if (null != E) {
            var h;
            Vt({
                type: "VOICE_STATE_UPDATES",
                voiceStates: E.map((function(e) {
                    return {
                        userId: e.user_id,
                        guildId: null,
                        sessionId: e.session_id,
                        channelId: e.channel_id,
                        mute: e.mute,
                        deaf: e.deaf,
                        selfMute: e.self_mute,
                        selfDeaf: e.self_deaf,
                        selfVideo: e.self_video || !1,
                        suppress: e.suppress,
                        selfStream: e.self_stream || !1,
                        requestToSpeakTimestamp: null !== (h = e.request_to_speak_timestamp) && void 0 !== h ? h : null
                    }
                }))
            })
        }
        break;
    case "CALL_UPDATE":
        Vt({
            type: "CALL_UPDATE",
            channelId: t.channel_id,
            messageId: t.message_id,
            region: t.region,
            ringing: t.ringing
        });
        break;
    case "CALL_DELETE":
        Vt({
            type: "CALL_DELETE",
            channelId: t.channel_id,
            unavailable: t.unavailable
        });
        break;
    case "OAUTH2_TOKEN_REVOKE":
        Vt({
            type: "OAUTH2_TOKEN_REVOKE",
            accessToken: t.access_token
        });
        break;
    case "RECENT_MENTION_DELETE":
        Vt({
            type: "RECENT_MENTION_DELETE",
            id: t.message_id
        });
        break;
    case "FRIEND_SUGGESTION_CREATE":
        Vt({
            type: "FRIEND_SUGGESTION_CREATE",
            suggestion: t
        });
        break;
    case "FRIEND_SUGGESTION_DELETE":
        Vt({
            type: "FRIEND_SUGGESTION_DELETE",
            suggestedUserId: t.suggested_user_id
        });
        break;
    case "WEBHOOKS_UPDATE":
        Vt({
            type: "WEBHOOKS_UPDATE",
            guildId: t.guild_id,
            channelId: t.channel_id
        });
        break;
    case "BURST_CREDIT_BALANCE_UPDATE":
        Vt({
            type: "BURST_CREDITS_SET",
            amount: t.amount,
            wasReplenishedToday: t.replenished_today
        });
        break;
    case "MESSAGE_REACTION_ADD":
    case "MESSAGE_REACTION_REMOVE":
        Vt({
            type: e,
            channelId: t.channel_id,
            messageId: t.message_id,
            userId: t.user_id,
            emoji: t.emoji,
            burst: t.burst,
            colors: t.burst_colors
        });
        break;
    case "MESSAGE_REACTION_REMOVE_ALL":
        Vt({
            type: "MESSAGE_REACTION_REMOVE_ALL",
            channelId: t.channel_id,
            messageId: t.message_id
        });
        break;
    case "MESSAGE_REACTION_REMOVE_EMOJI":
        Vt({
            type: "MESSAGE_REACTION_REMOVE_EMOJI",
            channelId: t.channel_id,
            messageId: t.message_id,
            emoji: t.emoji
        });
        break;
    case "PAYMENT_UPDATE":
        Vt({
            type: "PAYMENT_UPDATE",
            payment: t
        });
        break;
    case "ENTITLEMENT_CREATE":
    case "ENTITLEMENT_UPDATE":
    case "ENTITLEMENT_DELETE":
        Vt({
            type: e,
            entitlement: t
        });
        break;
    case "USER_PAYMENT_SOURCES_UPDATE":
        if (ot.Z.hasLayers()) {
            n(673679).tZ();
            u.Gn(ft.Z.getFetchedSKUIDs())
        }
        break;
    case "USER_SUBSCRIPTIONS_UPDATE":
        c.k();
        ot.Z.hasLayers() && n(673679).jg();
        break;
    case "USER_PREMIUM_GUILD_SUBSCRIPTION_SLOT_CREATE":
        Vt({
            type: "GUILD_BOOST_SLOT_CREATE",
            guildBoostSlot: De.Z.createFromServer(t)
        });
        break;
    case "USER_PREMIUM_GUILD_SUBSCRIPTION_SLOT_UPDATE":
        Vt({
            type: "GUILD_BOOST_SLOT_UPDATE",
            guildBoostSlot: De.Z.createFromServer(t)
        });
        break;
    case "BILLING_POPUP_BRIDGE_CALLBACK":
        Vt({
            type: "BILLING_POPUP_BRIDGE_CALLBACK",
            paymentSourceType: t.payment_source_type,
            state: t.state,
            path: t.path,
            query: t.query
        });
        break;
    case "USER_PAYMENT_CLIENT_ADD":
        (0, we.L)().then((function(e) {
            var n = t.purchase_token_hash;
            n === e && Vt({
                type: "USER_PAYMENT_CLIENT_ADD",
                purchaseTokenHash: n,
                expiresAt: t.expires_at
            })
        }));
        break;
    case "GUILD_MEMBER_LIST_UPDATE":
        i.ZP.Emitter.batched((function() {
            var e = function(e) {
                if (null != e.member) {
                    var n = e.member;
                    Rt(t.guild_id, n.user, n);
                    if (null != n.presence) {
                        var r = n.presence;
                        Zt(t.guild_id, r.user, r.status, r.activities, r.client_status)
                    }
                }
            };
            t.ops.forEach((function(t) {
                var n = t.op,
                    r = t.items,
                    o = t.item;
                switch (n) {
                    case "SYNC":
                        r.forEach(e);
                        break;
                    case "UPDATE":
                    case "INSERT":
                        e(o)
                }
            }));
            Ht.flush();
            Vt({
                type: "GUILD_MEMBER_LIST_UPDATE",
                guildId: t.guild_id,
                id: t.id,
                ops: t.ops,
                groups: t.groups,
                memberCount: t.member_count
            })
        }));
        break;
    case "LOBBY_CREATE":
        Vt({
            type: "LOBBY_CREATE",
            lobby: t
        });
        t.voice_states.forEach((function(e) {
            Vt({
                type: "LOBBY_VOICE_STATE_UPDATE",
                lobbyId: t.id,
                userId: e.user_id,
                sessionId: e.session_id,
                channelId: e.channel_id,
                mute: e.mute,
                deaf: e.deaf,
                selfMute: e.self_mute,
                selfDeaf: e.self_deaf
            })
        }));
        break;
    case "LOBBY_UPDATE":
        Vt({
            type: "LOBBY_UPDATE",
            lobby: t
        });
        break;
    case "LOBBY_DELETE":
        Vt({
            type: "LOBBY_DELETE",
            lobbyId: t.id,
            reason: t.reason
        });
        break;
    case "LOBBY_MEMBER_CONNECT":
    case "LOBBY_MEMBER_UPDATE":
    case "LOBBY_MEMBER_DISCONNECT":
        Vt({
            type: e,
            lobbyId: t.lobby_id,
            member: t.member
        });
        break;
    case "LOBBY_MESSAGE":
        Vt({
            type: "LOBBY_MESSAGE",
            lobbyId: t.lobby_id,
            senderId: t.sender_id,
            data: t.data
        });
        break;
    case "GIFT_CODE_UPDATE":
        Vt({
            type: "GIFT_CODE_UPDATE",
            uses: t.uses,
            code: t.code
        });
        break;
    case "GIFT_CODE_CREATE":
        Vt({
            type: "GIFT_CODE_CREATE",
            giftCode: t
        });
        break;
    case "USER_ACHIEVEMENT_UPDATE":
        Vt({
            type: "USER_ACHIEVEMENT_UPDATE",
            userAchievement: t
        });
        break;
    case "LIBRARY_APPLICATION_UPDATE":
        Vt({
            type: "LIBRARY_APPLICATION_UPDATE",
            libraryApplication: t
        });
        break;
    case "STREAM_CREATE":
        Vt({
            type: "STREAM_CREATE",
            streamKey: t.stream_key,
            region: t.region,
            viewerIds: t.viewer_ids,
            rtcServerId: t.rtc_server_id,
            paused: t.paused
        });
        break;
    case "STREAM_SERVER_UPDATE":
        Vt({
            type: "STREAM_SERVER_UPDATE",
            streamKey: t.stream_key,
            endpoint: t.endpoint,
            token: t.token
        });
        break;
    case "STREAM_UPDATE":
        Vt({
            type: "STREAM_UPDATE",
            streamKey: t.stream_key,
            region: t.region,
            viewerIds: t.viewer_ids,
            paused: t.paused
        });
        break;
    case "STREAM_DELETE":
        Vt({
            type: "STREAM_DELETE",
            streamKey: t.stream_key,
            unavailable: t.unavailable,
            reason: t.reason
        });
        break;
    case "GENERIC_PUSH_NOTIFICATION_SENT":
        Vt({
            type: "GENERIC_PUSH_NOTIFICATION_SENT",
            title: t.title,
            body: t.body,
            trackingType: t.tracking_type,
            icon: t.icon,
            route: t.route,
            tag: t.tag
        });
        break;
    case "NOTIFICATION_CENTER_ITEM_CREATE":
        Vt({
            type: "NOTIFICATION_CENTER_ITEM_CREATE",
            item: t
        });
        break;
    case "NOTIFICATION_CENTER_ITEM_DELETE":
        Vt({
            type: "NOTIFICATION_CENTER_ITEM_DELETE",
            id: t.id
        });
        break;
    case "NOTIFICATION_CENTER_ITEMS_ACK":
        Vt({
            type: "NOTIFICATION_CENTER_ITEMS_ACK",
            id: t.id,
            optimistic: !1
        });
        break;
    case "NOTIFICATION_CENTER_ITEM_COMPLETED":
        Vt({
            type: "NOTIFICATION_CENTER_ITEM_COMPLETED",
            item_enum: t.item_enum
        });
        break;
    case "APPLICATION_COMMAND_PERMISSIONS_UPDATE":
        Vt({
            type: e,
            guildId: t.guild_id
        });
        break;
    case "GUILD_APPLICATION_COMMAND_INDEX_UPDATE":
        Vt({
            type: "GUILD_APPLICATION_COMMAND_INDEX_UPDATE",
            guildId: t.guild_id,
            applicationCommandCounts: t.application_command_counts
        });
        break;
    case "GUILD_JOIN_REQUEST_CREATE":
        Vt({
            type: "GUILD_JOIN_REQUEST_CREATE",
            request: t.request,
            status: t.status,
            guildId: t.guild_id
        });
        break;
    case "GUILD_JOIN_REQUEST_UPDATE":
        Vt({
            type: "GUILD_JOIN_REQUEST_UPDATE",
            request: t.request,
            status: t.status,
            guildId: t.guild_id
        });
        break;
    case "GUILD_JOIN_REQUEST_DELETE":
        Vt({
            type: "GUILD_JOIN_REQUEST_DELETE",
            id: t.id,
            userId: t.user_id,
            guildId: t.guild_id
        });
        break;
    case "INTERACTION_CREATE":
        Vt({
            type: "INTERACTION_CREATE",
            interactionId: t.id,
            nonce: t.nonce
        });
        break;
    case "INTERACTION_SUCCESS":
        Vt({
            type: "INTERACTION_SUCCESS",
            interactionId: t.id,
            nonce: t.nonce
        });
        break;
    case "INTERACTION_FAILURE":
        Vt({
            type: "INTERACTION_FAILURE",
            nonce: t.nonce
        });
        break;
    case "APPLICATION_COMMAND_AUTOCOMPLETE_RESPONSE":
        Vt({
            type: "APPLICATION_COMMAND_AUTOCOMPLETE_RESPONSE",
            choices: t.choices,
            nonce: t.nonce
        });
        break;
    case "INTERACTION_MODAL_CREATE":
        Vt({
            type: "INTERACTION_MODAL_CREATE",
            id: t.id,
            channelId: t.channel_id,
            customId: t.custom_id,
            application: t.application,
            title: t.title,
            components: t.components,
            nonce: t.nonce
        });
        break;
    case "STAGE_INSTANCE_CREATE":
        Vt({
            type: "STAGE_INSTANCE_CREATE",
            instance: t
        });
        break;
    case "STAGE_INSTANCE_UPDATE":
        Vt({
            type: "STAGE_INSTANCE_UPDATE",
            instance: t
        });
        break;
    case "STAGE_INSTANCE_DELETE":
        Vt({
            type: "STAGE_INSTANCE_DELETE",
            instance: t
        });
        break;
    case "GUILD_SCHEDULED_EVENT_CREATE":
        Vt({
            type: "GUILD_SCHEDULED_EVENT_CREATE",
            guildScheduledEvent: t
        });
        break;
    case "GUILD_SCHEDULED_EVENT_UPDATE":
        Vt({
            type: "GUILD_SCHEDULED_EVENT_UPDATE",
            guildScheduledEvent: t
        });
        break;
    case "GUILD_SCHEDULED_EVENT_DELETE":
        Vt({
            type: "GUILD_SCHEDULED_EVENT_DELETE",
            guildScheduledEvent: t
        });
        break;
    case "GUILD_SCHEDULED_EVENT_USER_ADD":
        Vt({
            type: "GUILD_SCHEDULED_EVENT_USER_ADD",
            userId: t.user_id,
            guildId: t.guild_id,
            guildEventId: t.guild_scheduled_event_id
        });
        break;
    case "GUILD_SCHEDULED_EVENT_USER_REMOVE":
        Vt({
            type: "GUILD_SCHEDULED_EVENT_USER_REMOVE",
            userId: t.user_id,
            guildId: t.guild_id,
            guildEventId: t.guild_scheduled_event_id
        });
        break;
    case "GUILD_DIRECTORY_ENTRY_CREATE":
        Vt({
            type: "GUILD_DIRECTORY_ENTRY_CREATE",
            channelId: t.directory_channel_id,
            entry: t
        });
        break;
    case "GUILD_DIRECTORY_ENTRY_UPDATE":
        Vt({
            type: "GUILD_DIRECTORY_ENTRY_UPDATE",
            channelId: t.directory_channel_id,
            entry: t
        });
        break;
    case "GUILD_DIRECTORY_ENTRY_DELETE":
        Vt({
            type: "GUILD_DIRECTORY_ENTRY_DELETE",
            channelId: t.directory_channel_id,
            guildId: t.entity_id
        });
        break;
    case "AUTO_MODERATION_MENTION_RAID_DETECTION":
        Vt({
            type: "AUTO_MODERATION_MENTION_RAID_DETECTION",
            guildId: t.guild_id,
            decisionId: t.decision_id,
            suspiciousMentionActivityUntil: t.suspicious_mention_activity_until
        });
        break;
    case "VOICE_CHANNEL_EFFECT_SEND":
        Vt({
            type: "VOICE_CHANNEL_EFFECT_SEND",
            emoji: t.emoji,
            channelId: t.channel_id,
            userId: t.user_id,
            animationType: t.animation_type,
            animationId: t.animation_id,
            soundId: t.sound_id,
            soundVolume: t.sound_volume,
            soundOverridePath: t.sound_override_path,
            points: t.points,
            streamerId: t.streamer_id,
            lineId: t.line_id,
            emojiHose: t.emoji_hose
        });
        break;
    case "GUILD_SOUNDBOARD_SOUND_CREATE":
        Vt({
            type: "GUILD_SOUNDBOARD_SOUND_CREATE",
            sound: {
                guildId: t.guild_id,
                name: t.name,
                soundId: t.sound_id,
                user: new Pe.Z(t.user),
                volume: t.volume,
                emojiId: t.emoji_id,
                emojiName: t.emoji_name,
                overridePath: t.override_path
            }
        });
        break;
    case "GUILD_SOUNDBOARD_SOUND_UPDATE":
        Vt({
            type: "GUILD_SOUNDBOARD_SOUND_UPDATE",
            sound: {
                guildId: t.guild_id,
                name: t.name,
                soundId: t.sound_id,
                user: new Pe.Z(t.user),
                volume: t.volume,
                emojiId: t.emoji_id,
                emojiName: t.emoji_name,
                overridePath: t.override_path
            }
        });
        break;
    case "GUILD_SOUNDBOARD_SOUND_DELETE":
        Vt({
            type: "GUILD_SOUNDBOARD_SOUND_DELETE",
            guildId: t.guild_id,
            soundId: t.sound_id
        });
        break;
    case "EMBEDDED_ACTIVITY_UPDATE":
        Vt({
            type: "EMBEDDED_ACTIVITY_INBOUND_UPDATE",
            guildId: t.guild_id,
            channelId: t.channel_id,
            embeddedActivity: t.embedded_activity,
            connections: t.connections,
            updateCode: t.update_code
        });
        break;
    case "AUTH_SESSION_CHANGE":
        Vt({
            type: "AUTH_SESSION_CHANGE",
            authSessionIdHash: t.auth_session_id_hash
        });
        break;
    case "USER_CONNECTIONS_LINK_CALLBACK":
        Vt({
            type: "USER_CONNECTIONS_LINK_CALLBACK",
            provider: t.provider,
            callbackCode: t.callback_code,
            callbackState: t.callback_state
        });
        break;
    case "DELETED_ENTITY_IDS":
        Vt(Tt({
            type: "DELETED_ENTITY_IDS"
        }, t));
        break;
    case "CONSOLE_COMMAND_UPDATE":
        Vt({
            type: "CONSOLE_COMMAND_UPDATE",
            id: t.id,
            result: t.result,
            error: t.error
        });
        break;
    case "PASSIVE_UPDATE_V1":
        var I, m, T;
        Vt({
            type: "PASSIVE_UPDATE_V1",
            guildId: t.guild_id,
            members: t.members,
            channels: null === (I = t.channels) || void 0 === I ? void 0 : I.map((function(e) {
                return {
                    id: e.id,
                    lastMessageId: e.last_message_id,
                    lastPinTimestamp: e.last_pin_timestamp
                }
            })),
            voiceStates: null === (m = t.voice_states) || void 0 === m ? void 0 : m.map((function(e) {
                return {
                    channelId: e.channel_id,
                    deaf: e.deaf || !1,
                    mute: e.mute || !1,
                    requestToSpeakTimestamp: null !== (T = e.request_to_speak_timestamp) && void 0 !== T ? T : null,
                    selfDeaf: e.self_deaf || !1,
                    selfMute: e.self_mute || !1,
                    selfStream: e.self_stream || !1,
                    selfVideo: e.self_video || !1,
                    sessionId: e.session_id,
                    suppress: e.suppress,
                    userId: e.user_id
                }
            }))
        });
        break;
    case "PRIVATE_CHANNEL_INTEGRATION_CREATE":
        Vt({
            type: "PRIVATE_CHANNEL_INTEGRATION_CREATE",
            integration: t
        });
        break;
    case "PRIVATE_CHANNEL_INTEGRATION_UPDATE":
        Vt({
            type: "PRIVATE_CHANNEL_INTEGRATION_UPDATE",
            integration: t
        });
        break;
    case "PRIVATE_CHANNEL_INTEGRATION_DELETE":
        Vt({
            type: "PRIVATE_CHANNEL_INTEGRATION_DELETE",
            channelId: t.channel_id,
            applicationId: t.application_id
        });
        break;
    case "CREATOR_MONETIZATION_RESTRICTIONS_UPDATE":
        Vt({
            type: "GUILD_ROLE_SUBSCRIPTIONS_FETCH_RESTRICTIONS_SUCCESS",
            guildId: t.guild_id,
            restrictions: t.restrictions
        })
}