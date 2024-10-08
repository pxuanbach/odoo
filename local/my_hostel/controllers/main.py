from odoo import http
from odoo.http import request


class Main(http.Controller):

    @http.route('/my-hostel/students', type='http', auth='none')
    def all_students(self):
        students = request.env['hostel.student'].sudo().search([])
        html_result = '<html><body><ul>'
        for student in students:
            html_result += "<li> %s </li>" % student.name
        html_result += '</ul></body></html>'
        return html_result
