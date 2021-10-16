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
from datetime import timedelta

class hr_employee(models.Model):
    _inherit = ['hr.employee']
    '''
    We add to the resource the fields that we require for our system
    '''
    transferred = fields.Boolean(String="Transferred")
    employee_no = fields.Char(string="Employee No")
    national_id = fields.Char(string="National ID")
    date_work_start = fields.Date(string="Date Start of Work")
    has_dependents = fields.Boolean(string="Has Dependants?")
    contractor = fields.Boolean(string="Contractor?")
    transferred = fields.Boolean(string="Transferred??")
    no_of_wives = fields.Integer(string="No of Wives")
    person_id = fields.Char(string='Person ID')
    employment_degree_update_date = fields.Date(string="Next Degree Date")
    employment_degree_yearly_update_date = fields.Date(string="Next Yearly Bounus Date")
    current_emp_degree_years = fields.Selection([
        ('0','0'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ], string="Current Degree Years", default="0")
    employment_degree = fields.Selection([
        ('1', 'First Degree'),
        ('2', 'Second Degree'),
        ('3', 'Third Degree'),
        ('4', 'Fourth Degree'),
        ('5', 'Fifth Degree'),
        ('6', 'Sixth Degree'),
        ('7', 'Seventh Degree'),
        ('8', 'Eight Degree'),
        ('9', 'Ninth Degree'),
        ('10', 'Tenth Degree'),
        ('11', 'Eleventh Degree'),
        ('12', 'Twelfth Degree'),
        ('13', 'Thirteenth Degree'),
        ('14', 'Fourteenth Degree'),
        ('15', 'Fifteenth Degree'),
        ('16', 'Sixteenth Degree'),
        ('17', 'Seventeenth Degree'),
        ('18', 'Eighteenth Degree'),
        ('19', 'Nineteenth Degree'),
        ('20', 'Twentieth Degree'),
    ], 'Employment Degree', default="1")

    certification = fields.Many2one('io.certification', string='Certificate',
                           index=True, auto_join=True, ondelete="cascade",
                           check_company=True,
                           help="The certificate of an employee")

    employment_degree_history = fields.One2many('io.employment.degree', 'employee_id',string="Employment Degrees History", copy=False)
    hr_penalties = fields.One2many('io.penalty', 'employee_id',string="Penalties", copy=False)


    # def write(self, values):
    #     res = super(hr_employee, self).write(values)
    #     return res

    @api.model
    # kron job every month
    def update_holiday_allocations(self):
        print("Updating Values of Holiday Allocations")
        msg = '<div>The Following Employees have passed age 45 and require your attention to add Holidays allocation</div>'
        Y45 = timedelta(days=(45 * 365.24))
        D31 = timedelta(days=30)
        morethan = fields.date.today() - Y45
        lessthan = fields.date.today() - Y45 + D31
        search_obj = self.env['hr.employee'].search([('birthday', '>=', morethan), ('birthday', '<=', lessthan)])
        notification_ids = []
        if search_obj:
            for employee in search_obj:
                    notification_ids.append((0, 0, {
                                'res_partner_id': employee.user_id.partner_id.id,
                                'notification_type': 'inbox'}))
                    employee.sudo().message_post(body=msg, subtype_xmlid="mail.mt_comment")  # Message from Odoo Bot

                    activity_type = self.env['mail.activity.type'].search([('name', '=', 'activity_type_holiday_allocation')], limit=1)
                    deadline_date = fields.Date.today() + timedelta(days=5)

                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': 'إضافة 15 يوما لمستحقات الإجازة لأن الموظف قد تجاوز ال 45 سنة',
                        'note': 'urgent in 5 days',
                        'date_deadline': deadline_date,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')], limit=1).id,
                        'res_id': employee.id,
                        'user_id': activity_type.default_user_id.id
                    }
                    self.env['mail.activity'].create(create_vals)

    @api.onchange('employment_degree')
    def onchange_employment_degree(self):
        # Do the Math Only.
        delta = timedelta(days=1461)
        if int(self.employment_degree) > 9:
            delta= timedelta(days=1821)
        createIT = True
        degreePromotionDate = fields.date.today() + delta
        self.employment_degree_update_date = degreePromotionDate
        self.employment_degree_yearly_update_date = fields.date.today() + timedelta(days=365)
        self.current_emp_degree_years = '0'
        # # degree = self.employment_degree_history.browse([('employment_degree','=',self.employment_degree)])
        # self.employment_degree_update_date = fields.date.today() + delta

        for degree in self.employment_degree_history:
            if not degree.degree_end_date:
                degree.degree_end_date = fields.date.today()
            if degree.employment_degree == self.employment_degree:
                    createIT = False


        if createIT:
        #     #create it
            current_degree = self.env['io.employment.degree'].create({
                'employment_degree': self.employment_degree,
                'employee_id': self.id,
                'degree_start_date':  fields.date.today(),
                'degree_end_date': fields.date.today() + delta,
            })
        # last thing update zero the yearly experience bounus
        self.current_emp_degree_years = '0'



    @api.model
    # kron job every month
    def update_current_emp_degree_years(self):
        print("Updating Values of Employment Degree Years")
        msg = '<div>You have reached your employment degree update date and will be proceessed soon</div>'

        less_than = fields.date.today() + timedelta(days=1)
        more_than = fields.date.today() - timedelta(days=1)
        degrees_obj = self.env['hr.employee'].search([('employment_degree_update_date', '>=', more_than), ('employment_degree_update_date', '<=', less_than)])
        activity_type = self.env['mail.activity.type'].search([('name', '=', 'activity_type_employment_degree_update')],
                                                              limit=1)



        for employee in degrees_obj:
                    employee.sudo().message_post(body=msg, subtype_xmlid="mail.mt_comment")  # Message from Odoo Bot
                    deadline_date = fields.Date.today() + timedelta(days=5)
                    summary = "The employee name" + employee.name + " Should get an employment degreee update"
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary,
                        'note': 'urgent in 3 days',
                        'date_deadline': deadline_date,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')], limit=1).id,
                        'res_id': employee.id,
                        'user_id': activity_type.default_user_id.id
                    }
                    self.env['mail.activity'].create(create_vals)

        yearly_obj = self.env['hr.employee'].search([('employment_degree_yearly_update_date', '>=', more_than), ('employment_degree_yearly_update_date', '<=', less_than)])
        for employee in yearly_obj:
                    employee.sudo().message_post(body=msg, subtype_xmlid="mail.mt_comment")  # Message from Odoo Bot
                    deadline_date = fields.Date.today() + timedelta(days=5)
                    summary = "The employee name" + employee.name + " Should get a bounus update on his employment degree years"
                    create_vals = {
                        'activity_type_id': activity_type.id,
                        'summary': summary,
                        'note': 'urgent in 3 days',
                        'date_deadline': deadline_date,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.employee')], limit=1).id,
                        'res_id': employee.id,
                        'user_id': activity_type.default_user_id.id
                    }
                    self.env['mail.activity'].create(create_vals)
