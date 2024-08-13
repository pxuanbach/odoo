import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'
   
   group_hostel_user = fields.Boolean(string="Hostel User", implied_group='my_hostel.group_hostel_user')
