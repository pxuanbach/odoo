from odoo import models, fields, api


class HostelCategory(models.Model):
    _name = "hostel.category"

    name = fields.Char('Category')
    parent_id = fields.Many2one(
        'hostel.category',
        string='Parent Category',
        ondelete='restrict',
        index=True)
    _parent_store = True
    _parent_name = "parent_id" # optional if field is 'parent_id'
    parent_path = fields.Char(index=True, unaccent=False)
    child_ids = fields.One2many(
        'hostel.category', 'parent_id',
        string='Child Categories')
    
    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive categories.')
