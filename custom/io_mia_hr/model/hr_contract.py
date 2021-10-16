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
from datetime import timedelta

class hr_contract(models.Model):
    _inherit = 'hr.contract'
    '''i
    We add to the resource the fields that we require for our system
    '''

    contract_type = fields.Selection([
        ('service', 'Service Contract'),
        ('classified', 'Classified Contract'),
        ('transfer', 'Transfer Contract'),
        ('contractor', 'Contractor Contract'),
        ('marketing', 'Marketing Contract'),
    ], 'Contract Type', default="classified")


    @api.model
    # kron job every month
    def update_state(self):
        print("Updating Values of Contracts Allocations")
        msg = 'There is a contract that will expire very soon and requires a renewal or any other action'
        D31 = timedelta(days=31)
        morethan = fields.date.today() + D31
        lessthan = fields.date.today()
        search_obj = self.env['hr.contract'].search([('state', '=', 'open'), ('date_end', '<=', morethan), ('date_end', '>=', lessthan)])

        notification_ids = []
        for contract in search_obj:

                notification_ids.append((0, 0, {
                    'res_partner_id': contract.employee_id.user_id.partner_id.id,
                    'notification_type': 'inbox'}))
                contract.sudo().message_post(body=msg, subtype_xmlid="mail.mt_comment")  # Message from Odoo Bot
                # activity_type = self.env.ref('activity_type_loza_contract_expire_soon')
                activity_type = self.env['mail.activity.type'].search([('name', '=', 'activity_type_contract_update')], limit=1)
                deadline_date = fields.Date.today() + timedelta(days=5)

                create_vals = {
                    'activity_type_id': activity_type.id,
                    'summary': 'عقد سينتهي قريبا ويحتاج إلى تجديد',
                    'note': 'urgent in 5 days',
                    'date_deadline': deadline_date,
                    'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.contract')], limit=1).id,
                    'res_id': contract.id,
                    'user_id': activity_type.default_user_id.id
                }
                self.env['mail.activity'].create(create_vals)
