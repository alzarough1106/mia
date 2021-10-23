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

class loza_election_point(models.Model):
    _name = "loza.election.point"
    _inherit = 'mail.thread'
    _order = 'name desc'
    _description = 'An election point where people go and vote'
    _rec_name = 'name'

    sequence = fields.Char(string="Sequence")
    name = fields.Char(string="Election Point Name")
    voters = fields.Integer(string='Voters')
    longitude = fields.Char('Longitude')
    latitude = fields.Char('Latitude')
    office_id = fields.Many2one('loza.office',string="Under Office")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('loza.election.point')
        result = super(loza_election_point, self).create(vals)
        return result
