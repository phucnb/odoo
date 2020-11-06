from odoo import _, api, fields, models

class CustomState(models.Model):
    _inherit = 'res.country.state'

    def name_get(self):
        result = []
        for rewrite in self:
            if rewrite.country_id.name in['United States', 'Canada']:
                name = "%s" % rewrite.name
            else:
                name = "{0} ({1})".format(rewrite.name, rewrite.country_id.code)
            result.append((rewrite.id, name))
        return result
