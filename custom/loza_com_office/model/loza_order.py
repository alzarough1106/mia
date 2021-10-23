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
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import pytz


class loza_order(models.Model):
    _name = "loza.order"
    _inherit = 'mail.thread'
    # _inherit = 'loza_media_office.loza.event'
    _order = 'date desc'
    _rec_name = 'sequence'
    _description = 'An Order for execution'

    sequence = fields.Char(string="Order ID", readonly=True, copy=True)
    title = fields.Char(string="Title", )
    date = fields.Datetime(string='Order Date', default=datetime.now())
    before_date = fields.Datetime(string='Deadline At')
    summary = fields.Text(string="Order Summary", )

    # The User who originated the Order and it is automatic
    order_user = fields.Many2one('res.users', 'Order Originator')
    order_user_mobile = fields.Char('Order Originator Mobile Number', related="order_user.partner_id.mobile")

    # The User Accountable for executing the order
    order_executive = fields.Many2one('res.users', 'Order Co-ordinator')
    order_executive_mobile = fields.Char('Order Co-ordinator Mobile Number',
                                         related="order_executive.partner_id.mobile")

    # A flag to know if the order is still active
    is_active = fields.Boolean(string='Active?', default=False)

    desgnated_office = fields.Many2one('loza.office', string='Desgnated Office')
    originating_office = fields.Many2one('loza.office', string='Originating Office', related="order_user.office_id",
                                         store=True, index=True)

    offices = fields.Many2many('loza.office', string='offices')
    quests = fields.Many2many('loza.order.quest', string='Quests')
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
    ], string='Type', readonly=True, index=True, copy=False, default='service', tracking=True)

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('loza.order')
        result = super(loza_order, self).create(vals)
        return result

    def action_send_order(self):
        self.write({'state': 'sent'})
        self.order_user = self.env.user
        return {}

    def action_set_execution(self):
        self.order_executive = self.env.user
        self.write({'state': 'inprogress'})
        return

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
        # offices = self.env['loza.office'].search([('id','in',list)])
        # return offices

    def action_open_my_orders(self):
        return {
            'name': _('My Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('order_user', '=', self.env.user.id)],
            'res_model': 'loza.order',
        }

    def action_open_all_orders(self):
        return {
            'name': _('All Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'res_model': 'loza.order',
        }

    def action_open_my_team_orders(self):
        office_id = self.env.user.office_id
        users = self.env['res.users'].search([('office_id', '=', office_id.id)])
        return {
            'name': _('My Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('order_user', 'in', users.ids)],
            'res_model': 'loza.order',
        }

    def action_open_orders(self):
        return {
            'name': _('Work Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('offices', 'in', self._get_total_offices())],
            'res_model': 'loza.order',
        }

    def action_open_desgnated_orders(self):
        return {
            'name': _('Desgnated Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('desgnated_office', '=', self.env.user.office_id.id)],
            'res_model': 'loza.order',
        }

    def action_open_my_owned_orders(self):
        return {
            'name': _('Desgnated Orders'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'binding_view_types': 'tree',
            'domain': [('order_executive', '=', self.env.user.id)],
            'res_model': 'loza.order',
        }

    def loza_order_responses(self):
        return {
            'name': _('Order Responses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,graph,pivot',
            'binding_view_types': 'tree',
            'domain': [('order_id', '=', self.id), ('office_id', 'in', self._get_total_offices())],
            'res_model': 'loza.order.response',
            'context': {
                'order_id': self.id,
            }
        }

    def loza_order_stats(self):
        return {
            'name': _('Order Quest Responses'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,graph,pivot',
            'binding_view_types': 'tree',
            'domain': [('order_id', '=', self.id), ('office_id', 'in', self._get_total_offices())],
            'res_model': 'loza.order.quest.response',
            'context': {
                'order_id': self.id,
            }
        }

    response_count = fields.Integer(compute='get_response_count')

    def get_response_count(self):
        count = self.env['loza.order.response'].search_count(
            [('order_id', '=', self.id), ('office_id', 'in', self._get_total_offices())])
        self.response_count = count

    # TODO Write the function
    def action_create_order_response(self):

        response = self.env['loza.order.response'].create({
            'office_id': self.env.user.office_id.id,
            'order_id': self.id,
            'quest_response_ids': [],
            'title': 'Response For Order ID: ' + self.sequence,
            #            'office_id': self.env.user.office_id,
        })
        for quest in self.quests:
            quest_response = self.env['loza.order.quest.response'].create({
                'quest_id': quest.id,
                'order_response': response.id,
            })
            response.quest_response_ids += quest_response

        return {
            'name': 'Order Response',
            'type': 'ir.actions.act_window',
            'res_model': 'loza.order.response',
            'view_mode': 'form',
            'target': 'current',
            'res_id': response.id,
        }

    def action_open_media_event(self):
        return {
            'name': _('Media Events'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('event_id', '=', self.id)],
            'binding_view_types': 'tree',
            'res_model': 'loza_media_office.loza.event',
        }