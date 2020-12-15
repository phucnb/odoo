from odoo import models, fields, api

class ResPartnerField(models.Model):

     _inherit = 'res.partner'

     x_field = fields.Char('X Field')
     hs_analytics_num_event_completions = fields.Integer('Number of event completions')
     num_notes = fields.Integer("Number of Sales Activities")
     hs_email_bounce = fields.Integer("Marketing emails bounced")
     hs_email_click = fields.Integer("Marketing emails clicked")
     hs_email_delivered = fields.Integer("Marketing emails delivered")
     hs_email_open = fields.Integer("Marketing emails opened")
     hs_email_last_send_date = fields.Date('Last marketing email send date')
     hs_email_last_open_date = fields.Date('Last marketing email open date')
     hs_email_last_click_date = fields.Date('Last marketing email click date')
     hs_email_last_email_name = fields.Text("Last marketing email name")
     hs_marketable_until_renewal = fields.Boolean('Marketing Until Next Update')
     hs_email_optout = fields.Boolean('Unsubscribed from all email')
     # 1hs_deal_companies = fields.Many2one('res.partner', 'Company')

  


    # sale_order_count1 = fields.Integer(compute='_compute_sale_order_count1', string='Sale Order Count')
   
    # def _compute_sale_order_count1(self):
    #     # retrieve all children partners and prefetch 'parent_id' on them
    #     all_partners = self.with_context(active_test=False).search([('id', 'child_of', self.ids)])
    #     all_partners.read(['parent_id'])

    #     sale_order_groups = self.env['sale.order'].read_group(
    #         domain=[('partner_id', 'in', all_partners.ids)],
    #         fields=['partner_id'], groupby=['partner_id']
    #     )
    #     partners = self.browse()
    #     for group in sale_order_groups:
    #         partner = self.browse(group['partner_id'][0])
    #         while partner:
    #             if partner in self:
    #                 partner.sale_order_count1 += group['partner_id_count']
    #                 partners |= partner
    #             partner = partner.parent_id
    #     (self - partners).sale_order_count1 = 0
