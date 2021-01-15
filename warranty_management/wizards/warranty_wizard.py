from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WarrantyWizard(models.TransientModel):
    _name = 'warranty.wizard'

    wm_sale_order_id_w = fields.Many2one('sale.order', string="Related Sale order")
    wm_start_date_w = fields.Datetime("Start Date")
    wm_end_date_w = fields.Datetime("End Date")
    wm_partner_id_w = fields.Many2one('res.partner', string="Customer")
    wm_product_id_w = fields.Many2one('product.product', string="Product")
    wm_assigned_by_w = fields.Many2one('res.users', string="Awarded by")
    wm_comments_w = fields.Text("Note")

    def add_warranty(self):
        try:
            IrConfigParameter = self.env['ir.config_parameter'].sudo()
            auto_confirm = IrConfigParameter.get_param('warranty_management.wm_is_auto_confirm')
            warranty = self.env['warranty.management'].search([('wm_sale_order_id', '=', self.wm_sale_order_id_w.id),
                                                    ('wm_product_id', '=', self.env.context['default_product_id'])])
            if not warranty:
                self.env['warranty.management'].create({
                    "wm_sale_order_id": self.wm_sale_order_id_w.id,
                    "wm_start_date": self.wm_start_date_w if self.wm_start_date_w else None,
                    "wm_end_date": self.wm_end_date_w if self.wm_end_date_w else None,
                    "wm_partner_id": self.env.context['default_customer_id'],
                    "wm_product_id": self.env.context['default_product_id'],
                    "wm_status": 'warranty' if auto_confirm == 'True' else 'draft',
                    "wm_assigned_by": self.env.user.id,
                    "wm_comments": self.wm_comments_w if self.wm_comments_w else None,
                })
                self.env.cr.commit()

        except Exception as e:
            raise ValidationError(str(e))
