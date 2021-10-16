from odoo import models, fields, api, _
from datetime import datetime, timedelta

class loza_pitty_cash(models.Model):
    _name = "loza.pitty.cash"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'image.mixin']

    _order = "pittycash_id desc"
    _rec_name = "pittycash_id"
    _sql_constraints = [
        ('name_uniq', 'unique (pittycash_id)', 'The ID of the Pitty Cash")')
    ]

    @api.model
    def _get_default_currency(self):
        return self.env.company.currency_id

    pittycash_id = fields.Char(string='عهدة', copy=False,  readonly=True)
    name = fields.Char(string='الإسم المعروض')
    employee_id = fields.Many2one('hr.employee', string="Employee")
    partner_id = fields.Many2one('res.partner', string="Employee")
    journal_id = fields.Many2one('account.journal', string="Journal")
    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    balance = fields.Monetary(string='Balance',currency_field='currency_id',readonly=True, compute="_compute_balance")
    max_limit = fields.Monetary(string='Max Limit',currency_field='currency_id')
    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Pitty Cash Account',
        store=True)

    @api.model
    def create(self, vals):
        vals['pittycash_id'] = self.env['ir.sequence'].next_by_code('loza.pitty.cash') or 'LPC'
        result = super(loza_pitty_cash, self).create(vals)
        msg_body = 'تم إنشاء العهدة'
        for msg in self:
            msg.message_post(body=msg_body)
        return result



    def _compute_balance(self):
        payments = self.env['account.move'].search([('journal_id.name', '=', 'العهد المالية')])
        for doc in self:
            total = 0.0
            payment_p = payments.search([('partner_id','=', doc.partner_id.id)])
            for p in payment_p:
                total += p.amount_total
            doc.balance = total

    @api.onchange('employee_id')
    def onchange_transaction_ids(self):
            self.partner_id = self.employee_id.address_id.id
