from odoo import models, fields, api, _
from datetime import datetime


class transaction_wire(models.Model):
    _name = "transaction.wire"
    _order = "wire_id desc"
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
    from_bank_account = fields.Many2one('res.partner.bank',string='رقم الحساب')
    from_bank_name = fields.Char(string="الصادرة عن مصرف")
    to_bank_account = fields.Many2one('res.partner.bank',string='رقم الحساب')
    to_bank_name = fields.Char(string="مرسلة إلى مصرف")
#    partner_id = fields.Many2one('res.partner', string="أسم المستفيد")
    debit_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Debit Account',
        store=True, readonly=False)
    credit_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Credit Account',
        store=True, readonly=False)
    state = fields.Selection([
        ('open', 'Open'),
        ('half_lock', 'Half-Locked'),
        ('locked', 'Locked'),
    ], string='State', readonly=True, default='open')

    @api.onchange('from_bank_account')
    def onchange_from_bank_account(self):
        amount_tmp = 0
        for rec in self:
            if rec.from_bank_account:
                self.from_bank_name = rec.from_bank_account.bank_id.name
        return {}


    @api.onchange('to_bank_account')
    def onchange_to_bank_account(self):
        amount_tmp = 0
        for rec in self:
            if rec.to_bank_account:
                self.to_bank_name = rec.to_bank_account.bank_id.name
        return {}

    @api.model
    def create(self, vals):
        vals['wire_id'] = self.env['ir.sequence'].next_by_code('transaction.wire') or 'WIRE'
        vals['to_bank_name'] = self.to_bank_account.bank_id.name
        vals['from_bank_name'] = self.from_bank_account.bank_id.name
        result = super(transaction_wire, self).create(vals)
        return result
