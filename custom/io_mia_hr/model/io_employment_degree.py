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

class io_employment_degree(models.Model):
    _name = "io.employment.degree"
    _order = 'employment_degree desc'
    _description = 'The history of an employment degree for an employee'
    '''
    We add to the resource the fields that we require for our system
    '''
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

    employee_id = fields.Many2one('hr.employee', string='Employee',
                           index=True, readonly=True, auto_join=True, ondelete="cascade",
                           check_company=True,
                           help="The Employee with the current history")


    degree_start_date = fields.Date(string="Degree Start Date", default=date.today())
    degree_end_date = fields.Date(string="Degree End Date")
