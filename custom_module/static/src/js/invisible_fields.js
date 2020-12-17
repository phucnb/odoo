odoo.define('sale_customer.invisible_fields', function(require) {
    "use strict";

    var FormController = require('web.FormController');

    FormController.include({
        _onEdit: function () {
            // wait for potential pending changes to be saved (done with widgets
            // allowing to edit in readonly)
            // this.mutex.getUnlockedDef().then(this._setMode.bind(this, 'edit'));
            this._super.apply(this, arguments);
        },
    });
});
