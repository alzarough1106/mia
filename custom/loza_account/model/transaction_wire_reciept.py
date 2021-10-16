from odoo import models, fields, api, _
from datetime import datetime


class transaction_wire_reciept(models.Model):
    _name = "transaction.wire.reciept"
    _order = "kabad_id desc"
    _rec_name = "wire_id"

    saraf_id = fields.Many2one('loza.payment.approval', string='Saraf Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Saraf Document of this attachment")
    kabad_id = fields.Many2one('loza.reciept.approval', string='Kabad Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Kabad Document of this attachment")
    internal_id = fields.Many2one('loza.bank.notification', string='internal Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Internal Document of this attachment")

    wire_id = fields.Char(string='Wire ID', copy=False, readonly=1)
    description = fields.Char(string='Statement', copy=False)

    @api.model
    def _get_default_currency(self):
        return self.env.company.currency_id


    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='القيمة',currency_field='currency_id')
    bank_account = fields.Many2one('res.partner.bank',string='رقم الحساب')
    bank_name = fields.Char(string="أسم المصرف")
    type = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Cheaque'),
    ], string='Type', default='cash')

    @api.onchange('bank_account')
    def onchange_bank_account(self):
        amount_tmp = 0
        for rec in self:
            if rec.bank_account:
                self.bank_name = rec.bank_account.bank_id.name
        return {}


    @api.model
    def create(self, vals):
        vals['wire_id'] = self.env['ir.sequence'].next_by_code('transaction.wire.reciept') or 'WIRE'
        result = super(transaction_wire_reciept, self).create(vals)
        return result
