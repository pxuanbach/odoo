import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)


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
    remarks = fields.Text('Remarks')

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

    def log_all_room_members(self):
        # This is an empty recordset of model hostel.student
        hostel_room_obj = self.env['hostel.student']
        all_members = hostel_room_obj.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be created in hostel.room.category model
        record = self.env['hostel.room.category'].create(parent_category_val)
        return True

    def update_room_no(self):
        self.ensure_one()
        self.room_no = "RM002"

    # Filter recordset
    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        _logger.info('Filtered Rooms: %s', filtered_rooms)

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
        return all_rooms.filtered(predicate)
    
    def get_members_name(self):
        all_rooms = self.search([])
        filtered_rooms = self.get_members_names(all_rooms)
        _logger.info('Members Name: %s', filtered_rooms)

    @api.model
    def get_members_names(self, rooms):
        return rooms.mapped('student_ids.name')

    @api.model
    def create(self, values):
        if not self.user_has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'remarks'
                )
        return super(HostelRoom, self).create(values)
    
    def write(self, values):
        if not self.user_has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )
        return super(HostelRoom, self).write(values)
