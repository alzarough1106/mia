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

class io_certification(models.Model):
    _name = "io.certification"
    _order = 'name desc'
    _record = 'name'
    _description = 'The history of an employment degree for an employee'
    '''
    We add to the resource the fields that we require for our system
    '''
    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)


