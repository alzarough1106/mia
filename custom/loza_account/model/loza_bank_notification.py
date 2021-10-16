from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class loza_bank_notification(models.Model):
    _name = "loza.bank.notification"
    _inherit = ['mail.thread']
    _order = "internal_id desc"
    _rec_name = "internal_id"
    _sql_constraints = [
        ('name_uniq', 'unique (internal_id)', 'The name of the Ish3aar Document')
    ]

    internal_id = fields.Char(string='الأشعار', copy=False, readonly=True)

    partner_id = fields.Many2one('res.partner', string="أسم الجهة")

    internal_type = fields.Selection([
        ('negative', 'خصم'),
        ('positive', 'إضافة'),
    ], string='نوع الأشعار', default='negative')

    #   department_id = fields.Many2one('hr.department',string='مركز التكلفة')
    bank_id = fields.Many2one('res.partner.bank', string="أسم المصرف")

    payment_date = fields.Date(string="تاريخ المعاملة", default=datetime.today())
    addition_date = fields.Date(string="تاريخ الإضافة", default=datetime.today())

    @api.model
    def _get_default_currency(self):
        return self.env.company.currency_id

    #        return self.journal_id.company_id.currency_id

    recepient_id = fields.Many2one('res.partner', string="أسم المستلم")
    #    recepient_id_no = fields.Char(string='رقم الهوية')

    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', compute="_compute_amount", readonly=True)
    #    debit_account_id = fields.Many2one('account.account', string="Debit Account")
    #    credit_account_id = fields.Many2one('account.account', string="Credit Account")
    total = fields.Float(string="Total")
    total_string = fields.Char(string="Total in letters")
    transaction_ids = fields.One2many('transaction.bank.notification', 'internal_id', string="Transactions Details",
                                      copy=False)
    attachment_ids = fields.One2many('loza.transaction.attachment', 'internal_id', string="Attachments", copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('accounts', 'Accounts'),
        ('posted', 'Posted'),
    ], string='State', readonly=True, default='draft')

    prepare_id = fields.Many2one('hr.employee', string="أسم المستلم")
    prepare_id_jobtitle = fields.Char(string="الصفة الوظيفية")

    @api.model
    def create(self, vals):
        vals['internal_id'] = self.env['ir.sequence'].next_by_code('loza.bank.notification') or 'SRF'
        result = super(loza_bank_notification, self).create(vals)

        msg_body = 'تم إنشاء الأشعار'
        for msg in self:
            msg.message_post(body=msg_body)

        return result

    def action_confirm_internal(self):

        msg_body = 'تم أعتماده من المراجعة'
        for msg in self:
            msg.message_post(body=msg_body)

        self.write({'state': "accounts"})
        return

    def _compute_amount(self):
        for doc in self:
            total_untaxed = 0.0
            for line in doc.transaction_ids:
                total_untaxed += line.amount
            doc.amount = total_untaxed
            doc.total_string = self._generate_total_in_string()

    one_digit = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]

    two_digits = ["عشرة", "أحد عشر", "اثنا عشر", "ثلاثة عشر", "أربعة عشر", "خمسة عشر", "ستة عشر", "سبعة عشر",
                  "ثمانية عشر", "تسعة عشر"]

    tens_multiple = ["", "عشرة", "عشرين", "ثلاثون", "أربعون", "خمسون", "ستون", "سبعون", "ثمانون", "تسعين"]

    tens_power = ["مائة", "ألف", "مليون", "مليار"]

    hundreds = ["", "مائة", "مائتان", "ثلاثمائة", "أربعمائة", "خمسمائة", "ستمائة", "سبعمائة", "ثمانمئة", "تسعمائة"]

    def two_digits_f(self, n):
        str_ret = ""
        n_1 = int(n[1])
        n_2 = int(n[2])
        if n_1 == 0:
            str_ret += self.one_digit[n_2]
        elif n_1 == 1:
            str_ret += self.two_digits[n_2]
        elif n_2 == 0:
            str_ret += self.tens_multiple[n_1]
        else:
            str_ret += self.one_digit[n_2]
            str_ret += " و "
            str_ret += self.tens_multiple[n_1]
        return str_ret

    def three_digits(self, n):
        str_ret = ""
        huns_int = int(n[0])
        if huns_int != 0:
            str_ret += self.hundreds[huns_int]
        tens_int = int(n[1:])
        if tens_int != 0:
            str_ret += " و "
            str_ret += self.two_digits_f(n)
        return str_ret

    def four_digits(self, n):
        str_ret = ""
        str_ret = self.one_digit[int(n[0])]
        str_ret += " ألف و "
        str_ret += self.three_digits(n[1:])
        return str_ret

    def five_digits(self, n):
        str_ret = ""
        str_ret = self.two_digits_f(n[0:2])
        str_ret += " ألف و "
        str_ret += self.three_digits(n[2:])
        return str_ret

    # arg = str
    def six_digits(self, n):
        str_ret = ""
        str_ret = self.three_digits(n[0:3])
        str_ret += " ألف و "
        str_ret += self.three_digits(n[3:])
        return str_ret

    def seven_digits(self, n):
        str_ret = ""
        str_ret = self.one_digit[int(n[0])]
        str_ret += " مليون و "
        str_ret += self.six_digits(n[1:])
        return str_ret

    def eight_digits(self, n):
        str_ret = ""
        str_ret = self.two_digits_f(n[0:2])
        str_ret += " مليون و "
        str_ret += self.six_digits(n[2:])
        return str_ret

    def nine_digits(self, n):
        str_ret = ""
        str_ret = self.three_digits(n[0:3])
        str_ret += " مليون و "
        str_ret += self.six_digits(n[3:])
        return str_ret

    def ten_digits(self, n):
        str_ret = ""
        str_ret = self.one_digit[int(n[0])]
        str_ret += " مليار و "
        str_ret += self.nine_digits(n[1:])
        return str_ret

    def _generate_total_in_string(self):
        # first we need to break the number into digits and loop through them.
        # with some logic surrounding the first three digits.
        for doc in self:
            number = doc.amount
            strn = str(number)
            length = len(strn)
            dec_digit = strn.find('.')
            num_digits = 0
            lower_digits_count = 0
            num = ""
            dec = ""
            if dec_digit != -1:
                # there is a .
                num_digits = dec_digit
                dec_index_1 = dec_digit + 1
                lower_digits_count = length - dec_digit - 1

                num = strn[0:dec_digit]
                dec = strn[dec_index_1:length]
            else:
                num_digits = length
                num = strn
                lower_digits_count = 0
                dec = ""

            str_ret = ""
            index = 0
            current_digit = len(num)
            if current_digit == 1:
                str_ret += doc.one_digit[int(num)]
            if current_digit == 2:
                str_ret += doc.two_digits_f(" " + num)
            if current_digit == 3:
                str_ret += doc.three_digits(num)
            if current_digit == 4:
                str_ret += doc.four_digits(num)
            if current_digit == 5:
                str_ret += doc.five_digits(num)
            if current_digit == 6:
                str_ret += doc.six_digits(num)
            if current_digit == 7:
                str_ret += doc.seven_digits(num)
            if current_digit == 8:
                str_ret += doc.eight_digits(num)
            if current_digit == 9:
                str_ret += doc.nine_digits(num)
            if current_digit == 10:
                str_ret += doc.ten_digits(num)

            if int(num) > 0:
                str_ret += " دينار"

            # now we add the dirhams
            if lower_digits_count == 0:
                dec += "000"
            if lower_digits_count == 2:
                dec += "0"
            elif lower_digits_count == 1:
                dec += "00"
            # now we have a normalized digits of three digits
            int_dec = int(dec)
            if int_dec == 0:
                str_ret += " فقط"
                return str_ret

            # check if we have actually a number
            if int(num) > 0:
                str_ret += " و "

            dec_num = len(dec)

            if dec_num == 1:
                dec_2 = int(dec[2:])
                str_ret += loza_bank_notification.one_digit[dec_2]
            if dec_num == 2:
                str_ret += doc.two_digits_f(doc, dec)
            if dec_num == 3:
                str_ret += doc.three_digits(dec)
            str_ret += " درهم"
            return str_ret

    @api.onchange('transaction_ids')
    def onchange_transaction_ids(self):
        amount_tmp = 0
        for rec in self:
            if rec.transaction_ids:
                for txid in rec.transaction_ids:
                    if txid:
                        amount_tmp += txid.amount
            self.amount = amount_tmp
            self.total = amount_tmp
            #            self.write({'amount': amount_tmp})
            #            self.write({'total': amount_tmp})
            self.total_string = self._generate_total_in_string()

    #            self.write({'total_string': rec.total_string})

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        amount_tmp = 0
        for rec in self:
            if rec.employee_id:
                self.partner_id = rec.employee_id.address_id
