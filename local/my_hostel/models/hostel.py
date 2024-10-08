import logging
from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "Information about hostel"
    _rec_names_search = ['name', 'hostel_code']
    _order = "id desc, name"
    _rec_name = 'hostel_code'

    name = fields.Char(string="hostel Name", required=True)
    hostel_code = fields.Char(string="Code", required=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    phone = fields.Char('Phone', required=True)
    mobile = fields.Char('Mobile', required=True)
    email = fields.Char('Email')
    hostel_floors = fields.Integer(string="Total Floors")
    image = fields.Binary('Hostel Image')
    active = fields.Boolean("Active", default=True,
        help="Activate/Deactivate hostel record")
    type = fields.Selection([("individual", "Individual Host"), ("business", "Business Host")], "Type", help="Type of Hostel",
        required=True, default="common")
    other_info = fields.Text("Other Information",
        help="Enter more information")
    description = fields.Html('Description')
    hostel_rating = fields.Float('Hostel Average Rating', 
        # digits=(14, 4),
        digits='Rating Value')
    category_id = fields.Many2one('hostel.category')
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')
    rector = fields.Many2one("res.partner", "Rector",
        help="Select hostel rector")

    @api.depends('hostel_code')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.hostel_code:
                name = f'{name} ({record.hostel_code})'
            record.display_name = name
    
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
            ('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    def find_room(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Berloga Capsule JBR'),
                    ('category_id.name', 'ilike', 'VIP'),
                '&', ('name', 'ilike', 'Michael'),
                    ('category_id.name', 'ilike', 'VIP')
        ]
        rooms = self.search(domain)
        _logger.info('Room found: %s', rooms)
        return True

    def find_partner(self):
        PartnerObj = self.env['res.partner']
        domain = [
            ('name', 'ilike', 'Azure'),
        ]
        partner = PartnerObj.search(domain)
        _logger.info('Partner found: %s', partner)
        return True

    def sort_hostels_by_rating(self):
        all_hostels = self.search([])
        sorted_hostels = self.sort_rooms_by_rating(all_hostels)
        _logger.info("Sorted Hostels %s %s", sorted_hostels.mapped('name'), sorted_hostels.mapped('hostel_rating'))

    @api.model
    def sort_rooms_by_rating(self, hostels):
        return hostels.sorted(key='hostel_rating', reverse=True)
