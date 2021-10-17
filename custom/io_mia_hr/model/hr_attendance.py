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
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'
    person_id = fields.Char(string='Person ID')
    status = fields.Selection([
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ], 'Status', default="present")

    sorted = fields.Boolean(string='Is Sorted?',default=False)

    @api.model
    def create(self, vals):
        res = super(HrAttendance,self).create(vals)
        self.write({'person_id': self.employee_id.person_id})
        return res

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.write({'person_id': self.employee_id.person_id})
        self.person_id = self.employee_id.person_id

    @api.onchange('check_in')
    def onchange_check_in(self):

        if self.check_in:
            d1 = self.check_in
            hour = d1.hour
            minute = d1.minute
            if hour == 9:
                if minute <= 11:
                    self.status = 'present'
                else:
                    self.status = 'late'
            if hour <= 9:
                self.status = 'present'
            if hour > 9:
                if minute > 30:
                    self.status = 'absent'
                else:
                    self.status = 'absent'

            self.write({'status': self.status})


    @api.model
    def update_todays_attendance(self):
        print("Updating todays attendance")
