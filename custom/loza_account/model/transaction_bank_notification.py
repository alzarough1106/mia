from odoo import models, fields, api, _


class transaction_bank_notification(models.Model):
    _name = "transaction.bank.notification"
    _order = "transaction_id desc"
    _rec_name = "transaction_id"

    internal_id = fields.Many2one('loza.bank.notification', string='internal Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Internal Document of this attachment")

    transaction_id = fields.Char(string='Transaction ID', copy=False, readonly=1)
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
    amount = fields.Monetary(string='Amount',currency_field='currency_id')

    @api.model
    def create(self, vals):
        vals['transaction_id'] = self.env['ir.sequence'].next_by_code('transaction.bank.notification') or 'TXD'
        result = super(transaction_bank_notification, self).create(vals)
        return result