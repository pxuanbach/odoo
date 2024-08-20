from odoo import api, fields, models, _


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('m2m_group', 'M2m Group')])
