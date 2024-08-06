from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    is_hostel_rector = fields.Boolean("Hostel Rector", help="Activate if the following person is hostel rector")

