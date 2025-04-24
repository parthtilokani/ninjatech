import { reactive } from "@odoo/owl";

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

export class HelpdeskCoreCommon {
    /**
     * @param {import("@web/env").OdooEnv} env
     * @param {Partial<import("services").Services>} services
     */
    constructor(env, services) {
        this.busService = services.bus_service;
        this.env = env;
        this.notificationService = services.notification;
        this.orm = services.orm;
        this.presence = services.presence;
//        this.store = services["mail.store"];
    }

    setup() {

        this.busService.addChannel("helpdesk.ticket/new_message");

        this.busService.subscribe("helpdesk.ticket/new_message", (payload, metadata) => {
            // Insert should always be done before any async operation. Indeed,
            // awaiting before the insertion could lead to overwritting newer
            // state coming from more recent `mail.record/insert` notifications.
            this.store.insert(payload.data, { html: true });
            this._handleNotificationNewMessage(payload, metadata);
        });

    }


    async _handleNotificationNewMessage(payload, { id: notifId }) {
        const { data, id: channelId, silent, temporary_id } = payload;

        const channel = await this.store.Thread.getOrFetch({
            model: "helpdesk.ticket",
            id: channelId,
        });

        if (!channel) {
            return;
        }
        const message = this.store.Message.get(data["mail.message"][0]);
        console.log("channe;.................", channel, message);
        if (!message) {
            return;
        }
        if (message.notIn(channel.messages)) {
            if (!channel.loadNewer) {
                channel.addOrReplaceMessage(message, this.store.Message.get(temporary_id));
            } else if (channel.status === "loading") {
                channel.pendingNewMessages.push(message);
            }
            if (message.isSelfAuthored && channel.selfMember) {
                channel.selfMember.seen_message_id = message;
            } else {
                if (!channel.isDisplayed && channel.selfMember) {
                    channel.selfMember.syncUnread = true;
                    channel.scrollUnread = true;
                }
                if (notifId > channel.selfMember?.message_unread_counter_bus_id) {
                    channel.selfMember.message_unread_counter++;
                }
            }
        }
        if (
            !channel.isCorrespondentOdooBot &&
            channel.channel_type !== "channel" &&
            this.store.self.type === "partner" &&
            channel.selfMember
        ) {
            // disabled on non-channel threads and
            // on "channel" channels for performance reasons
            channel.markAsFetched();
        }
        if (
            !channel.loadNewer &&
            !message.isSelfAuthored &&
            channel.composer.isFocused &&
            this.store.self.type === "partner" &&
            channel.newestPersistentMessage?.eq(channel.newestMessage)
        ) {
            channel.markAsRead();
        }
        console.log("................ this................");
        this.env.bus.trigger("helpdesk.ticket/new_message", { channel, message, silent });
        const authorMember = channel.channelMembers.find(({ persona }) =>
            persona?.eq(message.author)
        );
        if (authorMember) {
            authorMember.seen_message_id = message;
        }
    }
}

export const helpdeskCoreCommon = {
    dependencies: [
        "bus_service",
//        "mail.out_of_focus",
//        "mail.store",
        "notification",
        "orm",
        "presence",
    ],
    /**
     * @param {import("@web/env").OdooEnv} env
     * @param {Partial<import("services").Services>} services
     */
    start(env, services) {
        const helpdeskCoreCommon = reactive(new HelpdeskCoreCommon(env, services));
        helpdeskCoreCommon.setup(env, services);
        return helpdeskCoreCommon;
    },
};

registry.category("services").add("helpdesk.core.common", helpdeskCoreCommon);
