from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'

  
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    roll_no = fields.Char(string='Roll No', required=True, copy=False, index=True)

    department = fields.Selection([
        ('cse', 'CSE'),
        ('iit', 'IIT'),
        ('english', 'English'),
        ('math', 'Math'),
        ('bangla', 'Bangla')
    ], string='Department', required=True)

    course_ids = fields.Many2many(
        'student.course',
        'student_course_rel',
        'student_id',
        'course_id',
        string='Courses'
    )

  
    @api.constrains('roll_no', 'department', 'email')
    def _check_unique_constraints(self):
        for rec in self:
           
            duplicate_roll = self.env['student.student'].search([
                ('roll_no', '=', rec.roll_no),
                ('department', '=', rec.department),
                ('id', '!=', rec.id)
            ], limit=1)
            if duplicate_roll:
                raise ValidationError(
                    f"Roll No '{rec.roll_no}' already exists in department {rec.department}!"
                )

           
            duplicate_email = self.env['student.student'].search([
                ('email', '=', rec.email),
                ('id', '!=', rec.id)
            ], limit=1)
            if duplicate_email:
                raise ValidationError(
                    f"Email '{rec.email}' is already used by another student!"
                )

            
            if rec.email and "@gmail.com" not in rec.email:
                raise ValidationError("Please enter a valid email address!")

  
    def action_submit_student(self):
        """ Custom Submit button - save student and show success notification """
        for rec in self:
            if not rec.name or not rec.roll_no or not rec.email:
                raise ValidationError("Name, Roll No and Email are required!")

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': f'Student {rec.name} submitted successfully!',
                    'sticky': False,
                }
            }

    def action_show_enrolled_courses(self):
        """ Show all courses enrolled by this student """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Courses for {self.name}',
            'res_model': 'student.course',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.course_ids.ids)],
            'target': 'current',
        }