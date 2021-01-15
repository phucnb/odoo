from odoo import models, fields, api


class WarrantySettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_stock_warranty = fields.Boolean('Warranty', default=False,
                                          implied_group='warranty_management.group_stock_warranty')
    wm_is_auto_confirm = fields.Boolean('Auto Confirm', default=False)

    def set_values(self):
        res = super(WarrantySettings, self).set_values()
        self.env['ir.config_parameter'].set_param('warranty_management.group_stock_warranty', self.group_stock_warranty)
        self.env['ir.config_parameter'].set_param('warranty_management.wm_is_auto_confirm', self.wm_is_auto_confirm)

        return res

    @api.model
    def get_values(self):
        res = super(WarrantySettings, self).get_values()
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        is_warranty = IrConfigParameter.get_param('warranty_management.group_stock_warranty')
        auto_confirm = IrConfigParameter.get_param('warranty_management.wm_is_auto_confirm')

        res.update(
            group_stock_warranty=True if is_warranty == 'True' else False,
            wm_is_auto_confirm=True if auto_confirm == 'True' else False,
        )

        return res
