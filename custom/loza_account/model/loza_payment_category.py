from odoo import models, fields, api, _


class loza_payment_category(models.Model):
    _name = "loza.payment.category"
    _order = "name desc"

    name = fields.Char(string='الإسم', copy=False, required=True)
