# -*- coding: utf-8 -*-
############################################################################
#
# Abr Afrikia LTD CONFIDENTIAL
# __________________
#
#  [2020] - [2021] Abr Afrikia Limited - Tripoli Libya
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Abr Afrikia Limited and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to Abr Afrikia Limited
# and its suppliers and may be covered by International Laws and Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Abr Afrikia Limited
#
#############################################################################
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import Warning,UserError

class loza_employee_transfer(models.Model):
    _name = "loza.employee.transfer"
    _rec_name = 'employee_id'
    _order = 'date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'a transfer of an employee'
    '''
    '''
    company_id = fields.Many2one('res.company', string='Company',readonly=True, required=True,
                                 default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department', string='Department',
                           index=True, auto_join=True, ondelete="cascade",
                           check_company=True,
                           help="The department which employee has moved to")
    job_id = fields.Many2one('hr.job', string='Job Position',
                           index=True, auto_join=True, ondelete="cascade",
                           check_company=True,
                           help="The new position which employee has moved to")
    employee_id = fields.Many2one('hr.employee', string='Employee',
                           index=True, auto_join=True, ondelete="cascade",
                           check_company=True,
                           help="The Employee who did the penalty")


    date = fields.Date(string="Transfer Date", default=date.today())

    state = fields.Selection([
        ('draft', 'مسودة'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, default='draft',
        tracking=True)

    def action_transfer_button(self):
           #close the last one
            resume_lines_values = []
            line_type = self.env.ref('hr_skills.resume_type_experience', raise_if_not_found=True)
            for resume_line in self.employee_id.resume_line_ids:
                    if not resume_line.date_end:
                        resume_line.date_end = self.date

            resume_lines_values.append({
                    'employee_id': self.employee_id.id,
                    'name': self.employee_id.company_id.name or '',
                    'date_start': self.date,
                    'description': self.job_id.name or '',
                    'line_type_id': line_type and line_type.id,
                })
            self.env['hr.resume.line'].create(resume_lines_values)

            #change real values for employee
            self.employee_id.job_id = self.job_id
            self.employee_id.department_id = self.department_id
            self.write({'state': "done"})
