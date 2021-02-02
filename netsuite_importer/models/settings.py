from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools


class Integration(models.TransientModel):
    _inherit = 'res.config.settings'

    nsAccountID = fields.Char('Account ID')
    consumerKey = fields.Char('Consumer Key')
    consumerSecret = fields.Char('Consumer Secret')
    token = fields.Char('Token Id')
    tokenSecret = fields.Char('Token Secret')

    def set_values(self):
        res = super(Integration,self).set_values()
        self.env['ir.config_parameter'].set_param('netsuite_importer.nsAccountID', self.nsAccountID)
        self.env['ir.config_parameter'].set_param('netsuite_importer.consumerKey', self.consumerKey)
        self.env['ir.config_parameter'].set_param('netsuite_importer.consumerSecret', self.consumerSecret)
        self.env['ir.config_parameter'].set_param('netsuite_importer.token', self.token)
        self.env['ir.config_parameter'].set_param('netsuite_importer.tokenSecret', self.tokenSecret)
        return res

    @api.model
    def get_values(self):
        res = super(Integration,self).get_values()
        icpsudo = self.env['ir.config_parameter'].sudo()
        nsAccountID = icpsudo.get_param('netsuite_importer.nsAccountID')
        consumerKey = icpsudo.get_param('netsuite_importer.consumerKey')
        consumerSecret = icpsudo.get_param('netsuite_importer.consumerSecret')
        token = icpsudo.get_param('netsuite_importer.token')
        tokenSecret = icpsudo.get_param('netsuite_importer.tokenSecret')
        res.update(
            nsAccountID=nsAccountID,
            consumerKey=consumerKey,
            consumerSecret=consumerSecret,
            token=token,
            tokenSecret=tokenSecret,
        )
        return res