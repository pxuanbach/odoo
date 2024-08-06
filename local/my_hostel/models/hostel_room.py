from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class BaseArchive(models.AbstractModel):
	_name = 'base.archive'
	active = fields.Boolean(default=True)
	
	def do_archive(self):
		for record in self:
			record.active = not record.active


class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = "Hostel Room Information"
    _rec_name = "room_no"
    _inherit = ['base.archive']
    _sql_constraints = [
        ("room_no_unique", "unique(room_no)", "Room number must be unique!")]

    name = fields.Char(string="Room Name", required=True)
    hostel_id = fields.Many2one("hostel.hostel", "hostel", help="Name of hostel")
    room_no = fields.Char("Room No.", required=True)
    floor_no = fields.Integer("Floor No.", default=1, help="Floor Number")
    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month")
    student_ids = fields.One2many("hostel.student", "room_id",
        string="Students", help="Enter students")
    hostel_amenities_ids = fields.Many2many("hostel.amenities",
        string="Amenities", domain="[('active', '=', True)]",
        help="Select hostel room amenities")
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'closed'),
                   ('closed', 'draft')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(msg)
        
    def make_available(self):
        self.change_state('available')
        
    def make_closed(self):
        self.change_state('closed')
