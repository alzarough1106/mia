from odoo import models, fields, api, _
from datetime import datetime, timedelta

class loza_loan(models.Model):
    _name = "loza.loan"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'image.mixin']

    _order = "loan_id desc"
    _rec_name = "loan_id"
    _sql_constraints = [
        ('name_uniq', 'unique (loan_id)', 'The ID of the Loan')
    ]

    @api.model
    def _get_default_currency(self):
        return self.env.company.currency_id

    name = fields.Char(string='الإسم المعروض')
    loan_id = fields.Char(string='سلفة', copy=False,  readonly=True)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    journal_id = fields.Many2one('account.journal', string="Journal")
    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='Amount',currency_field='currency_id')
    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Loan Account',
        store=True)


    @api.model
    def create(self, vals):
        vals['loan_id'] = self.env['ir.sequence'].next_by_code('loza.loan') or 'LLN'
        result = super(loza_loan, self).create(vals)
        msg_body = 'تم إنشاء السلفة'
        for msg in self:
            msg.message_post(body=msg_body)
        return result



