odoo.define('pn_mail/static/src/js/log_schedule.js', function(require) {
    "use strict";

    //const components = require('mail/static/src/components/chatter_topbar/chatter_topbar.js');
    //const ChatterTopbar = component;

    const components = {
        ChatterTopbar: require('mail/static/src/components/chatter_topbar/chatter_topbar.js'),
    };

    const { str_to_datetime } = require('web.time');
    const { patch } = require('web.utils');

    patch(components.ChatterTopbar, 'pn_mail/static/src/js/log_schedule.js', {
        _onClickLogScheduleActivity(ev) {
            const action = {
                type: 'ir.actions.act_window',
                name: this.env._t("Log"),
                res_model: 'mail.activity',
                view_mode: 'form',
                views: [[false, 'form']],
                target: 'new',
                context: {
                    default_res_id: this.chatter.thread.id,
                    default_res_model: this.chatter.thread.model,
                    default_is_log_schedule: true,
                    is_log_schedule: true
                },
                res_id: false,
            };
            return this.env.bus.trigger('do-action', {
                action,
                options: {
                    on_close: () => {
                        this.chatter.thread.refreshActivities();
                        this.chatter.thread.refresh();
                    },
                },
            });
        },
    });

    /*ChatterTopbar('mail.user', 'hr/static/src/models/user/user.js', {
        *//**
         * Employee related to this user.
         *//*
        employee: one2one('hr.employee', {
            inverse: 'user',
        }),
    });*/

    /*ChatterTopbar.include({


    });*/
});