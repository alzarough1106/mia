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
from datetime import date, datetime
from datetime import timedelta
from odoo.exceptions import Warning,UserError

class io_exit_permissions(models.Model):
    _name = "io.exit.permissions"
    _order = 'exit_dt desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'The exit permission of an employee'
    _rec_name = "exit_id"

    '''
    The exit permission for an employee
    '''
    exit_id = fields.Char(string='أذن الخروج', copy=False,  readonly=True)
    exit_dt  = fields.Date(string="Date", default=date.today())
    employee_id = fields.Many2one('hr.employee', string='Employee',
                           index=True,  auto_join=True, ondelete="cascade",
                           help="The Employee who has exit permissions")
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, default='draft')
    sorted = fields.Boolean(string='Is Sorted?',default=False)

    @api.model
    def create(self, vals):
        vals['exit_id'] = self.env['ir.sequence'].next_by_code('io.exit.permissions') or 'EXT'
        result = super(io_exit_permissions, self).create(vals)
        msg_body = 'تم إنشاء إذن الخروج'
        for msg in self:
            msg.message_post(body=msg_body)
        return result

    def action_accept_exit_permission(self):
        # mark the entry as exited and exist
        outer_dt = self.exit_dt + timedelta(days=1)
        attendance_record = self.env['hr.attendance'].search([
                      ('check_in', '>=', self.exit_dt),
                      ('employee_id', '=', self.employee_id.id),
                      ('check_in', '<=', outer_dt),
                        ])

        if not attendance_record:
                raise  UserError('There is no record checkin for this employee')
        #otherwise just update the record
        attendance_record.status = 'late'
        attendance_record.check_out = outer_dt
        # mytime = attendance_record.check_in.time()
        #
        # if mytime.hour <= 9:
        #         attendance_record.status = 'present'
        # elif mytime.minute > 0:
        #         attendance_record.status = 'absense'
        self.write({'state': "done"})


    def update_status(self):
        #first get attendance
        attendance_to_sort = self.env['hr.attendance'].search([('sorted','=',False)])
        for ar in attendance_to_sort:
            ci_date = ar.check_in
            nine_oclock = datetime(ci_date.year, ci_date.month, ci_date.day, 7, 0)
            nine_thirty = datetime(ci_date.year, ci_date.month, ci_date.day, 7, 30)
            if ar.check_in > nine_thirty:
                    ar.status = 'absent'
            elif ar.check_in > nine_oclock:
                    ar.status = 'late'
            else:
                    ar.status = 'present'
            if not ar.check_out:
                ar.check_out = datetime(ci_date.year, ci_date.month, ci_date.day, 15, 0)
            ar.sorted = True


        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('Done!'),
                'message': 'Sorted %s Entries' % len(attendance_to_sort),
                'type': 'success',  # types: success,warning,danger,info
                'sticky': False,  # True/False will display for few seconds if false
            },
        }
        return notification
        # return {
        #     'name': _('Attendance'),
        #     'view_mode': 'tree',
        #     'res_model': 'hr.attendance',
        #     'type': 'ir.actions.act_window',
        # }
