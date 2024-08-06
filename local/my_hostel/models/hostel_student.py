from odoo import api, fields, models


class HostelStudent(models.Model):
    _name = "hostel.student"
    _description = "Hostel Student Information"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    
    name = fields.Char("Student Name")
    gender = fields.Selection([("male", "Male"),
        ("female", "Female"), ("other", "Other")],
        string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True,
        help="Activate/Deactivate hostel record")
    room_id = fields.Many2one("hostel.room", "Room",
        help="Select hostel room")
    hostel_id = fields.Many2one("hostel.hostel", related='room_id.hostel_id')
    status = fields.Selection([("draft", "Draft"),
        ("reservation", "Reservation"), ("pending", "Pending"),
        ("paid", "Done"),("discharge", "Discharge"), ("cancel", "Cancel")],
        string="Status", copy=False, default="draft",
        help="State of the student hostel")
