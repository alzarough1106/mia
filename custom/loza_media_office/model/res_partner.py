from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    office_id = fields.Many2one('loza.office', string='Campaign Office')
