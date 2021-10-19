# -*- coding: utf-8 -*-
############################################################################
#
# LOZA LTD CONFIDENTIAL
# __________________
#
#  [2020] - [2021] Loza Limited - Tripoli Libya
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Loza Limited and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to Loza Limited
# and its suppliers and may be covered by International Laws and Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Loza Limited
#
#############################################################################

from odoo import api, fields, models, _
from datetime import date, datetime
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import pytz

class loza_office(models.Model):
    _name = "loza.office"
    _inherit = 'mail.thread'
    _order = 'name desc'
    _description = 'An Order for execution'

    name = fields.Char(string="Office Name")
    parent = fields.Many2one('loza.office',string="Parent")
    election_points = fields.One2many('loza.election.point','office_id',string="Election Points")
    sequence = fields.Char(string="Sequence")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('loza.office')
        result = super(loza_office, self).create(vals)
        return result
