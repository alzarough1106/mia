from odoo import models, fields, api, _
from datetime import datetime

class transaction_check_reciept(models.Model):
    _name = "transaction.check.reciept"
    _order = "check_id desc"
    _rec_name = "check_id"

    kabad_id = fields.Many2one('loza.reciept.approval', string='Kabad Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Kabad Document of this attachment")

    check_id = fields.Char(string='Check ID', copy=False, readonly=1)
    description = fields.Char(string='Statement', copy=False)
    debit_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Debit Account',
        store=True, readonly=False)
    credit_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Credit Account',
        store=True, readonly=False)

    @api.model
    def _get_default_currency(self):
#        return self.bank_account.company_id.currency_id
        return self.env.company.currency_id


    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='القيمة',currency_field='currency_id')
    check_no = fields.Char(string='رقم الصك')
    check_date = fields.Date(string="تاريخ الصك", default=datetime.today())

    @api.model
    def create(self, vals):
        vals['check_id'] = self.env['ir.sequence'].next_by_code('transaction.check.reciept') or 'CKBD'
        result = super(transaction_check_reciept, self).create(vals)
        return result
