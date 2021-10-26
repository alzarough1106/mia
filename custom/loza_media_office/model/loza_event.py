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


class loza_event(models.Model):
    _name = "loza.event"
    _inherit = 'mail.thread'
    _event = 'date desc'
    _rec_name = 'sequence'
    _description = 'An Event for execution'

    sequence = fields.Char(string="Event ID", readonly=True, copy=True)
    title = fields.Char(string="Title of the Event", )
    date = fields.Datetime(string='Event Date')
    summary = fields.Text(string="Event Summary", )
    place = fields.Many2many('loza.office', string='Places')
    designated_office = fields.Many2one('loza.office', string='Designated Office')
    quests = fields.Many2many('loza.event.quest', string='Quests')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('inprogress', 'In progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    type = fields.Selection([
        ('resolution', 'Resolution'),
        ('event', 'Event'),
        ('poll', 'Poll'),
        ('service', 'Service'),
    ], string='Type', readonly=True, index=True, copy=False, default='event', tracking=True)

    # The User who originated the Event and it is automatic
    event_user = fields.Many2one('res.users', 'Event Originator')
    event_executive = fields.Many2one('res.users', 'Event Co-ordinator')
    event_user_mobile = fields.Char('Event Originator Mobile Number', related="event_user.partner_id.mobile")

    # designated_office = fields.Many2one('loza.office', string='Designated Office')
    # originating_office = fields.Many2one('loza.office', string='Originating Office', related="event_user.office_id", store=True, index=True)

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('loza.event')
        result = super(loza_event, self).create(vals)
        return result
    def action_draft(self):
        self.state='draft'
    def action_cancel(self):
        self.state='cancel'
        vals['sequence'] = self.env['ir.sequence'].next_by_code('loza.event')
        result = super(loza_event, self).create(vals)
        return result

    def _get_sub_offices(self, office_id, list):
        list.append(office_id.id)
        children = self.env['loza.office'].search([('parent', '=', office_id.id)])
        for office in children:
            self._get_sub_offices(office, list)

    def _get_total_offices(self):
            office_id = self.env.user.office_id
            list = []
            self._get_sub_offices(office_id, list)
            the_offices = self.env['loza.office'].search([('id', 'in', list)])
            return the_offices.ids

    def action_open_events(self):
        return {
            'name': _('Event Created'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('designated_office', 'in', self._get_total_offices())],
            'res_model': 'loza.event',
        }
    def action_open_my_events(self):
        return {
            'name': _('My Events'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('event_user', '=', self.env.user.id)],
            'res_model': 'loza.event',
        }
    def action_send_event(self):
        self.write({'state': 'sent'})
        self.event_user = self.env.user
        return {}

    def action_accept_event(self):
        self.event_user = self.env.user
        self.write({'state': 'inprogress'})
        return

    def action_open_designated_events(self):
        return {
            'name': _('Events_Assigned'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('designated_office', '=', self.env.user.office_id.id)],
            'res_model': 'loza.event',
        }