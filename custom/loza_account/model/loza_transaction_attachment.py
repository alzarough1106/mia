from odoo import models, fields, api, _


class loza_transaction_attachment(models.Model):
    _name = "loza.transaction.attachment"
    _order = "attachment_id desc"
    _rec_name = "attachment_id"


    attachment_id = fields.Char(string='Attachment ID', copy=False, readonly=1)
    description = fields.Char(string='Attachment Description', copy=False)
    file = fields.Binary("Attachment", copy=False)
    saraf_id = fields.Many2one('loza.payment.approval', string='Saraf Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Saraf Document of this attachment")
    kabad_id = fields.Many2one('loza.reciept.approval', string='kabad Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The kabad Document of this attachment")

    internal_id = fields.Many2one('loza.bank.notification', string='internal Document',
        index=True, readonly=True, auto_join=True, ondelete="cascade",
        check_company=True,
        help="The Internal Document of this attachment")

    @api.model
    def create(self, vals):
        vals['attachment_id'] = self.env['ir.sequence'].next_by_code('loza.transaction.attachment') or 'ATT'
        result = super(loza_transaction_attachment, self).create(vals)
        return result