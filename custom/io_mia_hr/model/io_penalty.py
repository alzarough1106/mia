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

class io_penalty(models.Model):
    _name = "io.penalty"
    _order = 'date desc'
    _description = 'a penalty on an employee'
    '''
    We add to the resource the fields that we require for our system
    '''
    name = fields.Char(string='Name')
    notes = fields.Char(string='Notes')
    points = fields.Integer(string='Points')
    employee_id = fields.Many2one('hr.employee', string='Employee',
                           index=True, readonly=True, auto_join=True, ondelete="cascade",
                           check_company=True,
                           help="The Employee who did the penalty")


    date = fields.Date(string="Penalty Date", default=date.today())
