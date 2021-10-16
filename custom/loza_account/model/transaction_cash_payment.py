from odoo import models, fields, api, _


class transaction_cash_payment(models.Model):
    _name = "transaction.cash.payment"
    _order = "transaction_id desc"
    _rec_name = "transaction_id"

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

    transaction_id = fields.Char(string='Transaction ID', copy=False, readonly=1)
    description = fields.Char(string='Statement', copy=False)
#    partner_id = fields.Many2one('res.partner', string="أسم الجهة")

    @api.model
    def _get_default_currency(self):
#        return self.bank_account.company_id.currency_id
        return self.env.company.currency_id


    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='Amount',currency_field='currency_id')

    state = fields.Selection([
        ('open', 'Open'),
        ('half_lock', 'Half-Locked'),
        ('locked', 'Locked'),
    ], string='State', readonly=True, default='open')

    debit_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Debit Account',
        store=True, readonly=False)
    credit_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Credit Account',
        store=True, readonly=False)

    @api.model
    def create(self, vals):
        vals['transaction_id'] = self.env['ir.sequence'].next_by_code('transaction.cash.payment') or 'TXD'
        result = super(transaction_cash_payment, self).create(vals)
        return result