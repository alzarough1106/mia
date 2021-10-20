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

class loza_order_response(models.Model):
    _name = "loza.order.response"
    _order = 'title desc'
    _description = 'An Order for execution'
    _rec_name = 'title'


    title = fields.Char(string="Title")
    notes = fields.Text(string="Notes")
    quest_response_ids = fields.Many2many('loza.order.quest.response',string="Responses")
    office_id = fields.Many2one('loza.office',string="Office")
    election_point = fields.Many2one('loza.election.point',string="Election Point")
    order_id = fields.Many2one('loza.order')
    notes = fields.Text(string="Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def action_submit(self):
        self.write({'state': 'done'})
        return

    @api.onchange('election_point')
    def _onchange_election_point(self):
        self.title = 'Results for Election Point ' + self.election_point.name
