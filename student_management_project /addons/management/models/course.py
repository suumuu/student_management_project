from odoo import models, fields

class Course(models.Model):
    _name = 'student.course'
    _description = 'Course'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    credit = fields.Integer(string='Credit', default=2)

    student_ids = fields.Many2many(
        'student.student',
        'student_course_rel',
        'course_id',
        'student_id',
        string='Students',
        readonly=True
    )

    student_count = fields.Integer(string='Students Enrolled', compute='_compute_student_count')

    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'student.student',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.student_ids.ids)],
            'target': 'current',
        }
