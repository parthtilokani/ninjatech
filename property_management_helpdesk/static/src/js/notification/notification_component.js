
import { Component, useState, onMounted, useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";


//export class NotificationIcon extends Component {
//    static template = "property_management_helpdesk.NotificationIconTemplate";
//
//    setup() {
//        this.chatterService = useState(useService("helpdesk.core.common"));
//        this.store = useState(useService("mail.store"));
//
//        console.log("............. this component loaded????????///",this.store.chatHub.thread, this.store.Thread.records,this.store.Thread.records.selfMember?.message_unread_counter);
////        useEffect(
////            () => {
//////                this.state.bouncing = this.thread.importantCounter ? true : this.state.bouncing;
////                const channel = this.store.Thread.getOrFetch({
////                    model: "helpdesk.ticket",
////                }).then(function(res){
////                    console.log("result............", res);
////                });
////                console.log("something////////////////", this.store.Thread.records, this.store.Thread);
////            },
////            () => [this.store.Thread.records]
////        );
//
//        this.state = useState({ unreadCount: 0 });
//
//        onMounted(async () => {
//            await this.fetchUnreadCount();
//        });
//    }
//
//
//
//    async fetchUnreadCount() {
//        console.log("fetch Unread count/?//////");
//        const { resModel, resId } = this.chatterService;
//        if (!resModel || !resId) return;
//
////        this.state.unreadCount = await this.rpc("/your_module/get_unread_message_count", {
////            model: resModel,
////            res_id: resId,
////        });
//    }
//
//    async onClick() {
//        await this.markMessagesAsRead();
//        this.state.unreadCount = 0;
//        // Scroll to chatter section (adjust selector as needed)
//        document.querySelector(".o_portal_chatter")?.scrollIntoView({ behavior: "smooth" });
//    }
//
//    async markMessagesAsRead() {
//        const { resModel, resId } = this.chatterService;
////        await this.rpc("/your_module/mark_messages_as_read", {
////            model: resModel,
////            res_id: resId,
////        });
//    }
//}
//
//
//registry.category("public_components").add("NotificationIcon", NotificationIcon);