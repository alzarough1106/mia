from odoo import models, fields, api, _
from datetime import datetime

class transaction_check_payment(models.Model):
    _name = "transaction.check.payment"
    _order = "check_id desc"
    _rec_name = "check_id"

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

    check_id = fields.Char(string='Check ID', copy=False, readonly=1)
    description = fields.Char(string='Statement', copy=False)

    @api.model
    def _get_default_currency(self):
#        return self.bank_account.company_id.currency_id
        return self.env.company.currency_id


    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='القيمة',currency_field='currency_id')
    check_no = fields.Char(string='رقم الصك')
#    pay_to = fields.Many2one('res.partner', string="أسم المستفيد")
    check_date = fields.Date(string="تاريخ الصك", default=datetime.today())

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

    @api.model
    def create(self, vals):
        vals['check_id'] = self.env['ir.sequence'].next_by_code('transaction.check.payment') or 'CHK'
        result = super(transaction_check_payment, self).create(vals)
        return result
