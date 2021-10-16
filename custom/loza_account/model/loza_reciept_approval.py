from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class loza_reciept_approval(models.Model):
    _name = "loza.reciept.approval"
    _inherit = ['mail.thread']
    _order = "kabad_id desc"
    _rec_name = "kabad_id"
    _sql_constraints = [
        ('name_uniq', 'unique (kabad_id)', 'The name of the Kabad Document')
    ]

    kabad_id = fields.Char(string='أذن القبض', copy=False,  readonly=True)
    kabad_type = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Cheaque'),
    ], string='Kabad Type', default='cash')


    partner_id = fields.Many2one('res.partner', string="أسم الجهة")

    recepient_id = fields.Many2one('res.partner', string="أسم المستلم")
    recepient_id_no = fields.Char(string='رقم الهوية')

#    department_id = fields.Many2one('hr.department',string='مركز التكلفة')
#    journal_id = fields.Many2one('account.journal', string="Journal")

    payment_date = fields.Date(string="تاريخ المعاملة", default=datetime.today())

    @api.model
    def _get_default_currency(self):
        return self.env.company.currency_id



    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='المبلغ المستلم',currency_field='currency_id',compute="_compute_amount", readonly=True)
#    debit_account_id = fields.Many2one('account.account', string="Debit Account")
#    credit_account_id = fields.Many2one('account.account', string="Credit Account")
    total = fields.Float(string="Total")
    total_string = fields.Char(string="Total in letters")
    transaction_ids = fields.One2many('transaction.cash.reciept', 'kabad_id',string="Cash Transactions Details", copy=False)
    check_ids = fields.One2many('transaction.check.reciept', 'kabad_id',string="Check Transactions Details", copy=False)


    attachment_ids = fields.One2many('loza.transaction.attachment', 'kabad_id', string="Attachments", copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('posted', 'Posted'),
    ], string='State', readonly=True, default='draft')

    prepare_id = fields.Many2one('hr.employee', string="أسم المستلم")
    prepare_id_jobtitle = fields.Char(string="الصفة الوظيفية")
    safecarer_id = fields.Many2one('hr.employee', string="أمين الخزينة")

    @api.model
    def create(self, vals):
        vals['kabad_id'] = self.env['ir.sequence'].next_by_code('loza.reciept.approval') or 'SRF'
        result = super(loza_reciept_approval, self).create(vals)
        msg_body = 'تم إنشاء إذن القبض'
        for msg in self:
            msg.message_post(body=msg_body)
        return result

    def action_confirm_kabad(self):
        msg_body = 'تم استلام المبلغ'
        for msg in self:
            msg.message_post(body=msg_body)
        self.write({'state': "received"})
        return

    def _compute_amount(self):
        for doc in self:
            total_untaxed = 0.0
            if doc.kabad_type == 'cash':
                for line in doc.transaction_ids:
                    total_untaxed += line.amount
            if doc.kabad_type == 'check':
                for line in doc.check_ids:
                    total_untaxed += line.amount
            doc.amount = total_untaxed
            doc.total_string = self._generate_total_in_string()

    one_digit = ["", "واحد", "اثنان" , "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]


    two_digits = ["عشرة", "أحد عشر", "اثنا عشر", "ثلاثة عشر" , "أربعة عشر", "خمسة عشر", "ستة عشر", "سبعة عشر", "ثمانية عشر", "تسعة عشر"]

    tens_multiple = ["", "عشرة", "عشرين", "ثلاثون" , "أربعون" , "خمسون", "ستون", "سبعون", "ثمانون", "تسعين"]

    tens_power = ["مائة", "ألف", "مليون", "مليار"]

    hundreds = ["", "مائة", "مائتان", "ثلاثمائة", "أربعمائة", "خمسمائة", "ستمائة", "سبعمائة", "ثمانمئة", "تسعمائة"]


    def two_digits_f(self, n):
        str_ret = ""
        len_n = len(n)
        if len_n == 2:
            n = "0" + n
        if len_n == 1:
            n = "00" + n

        n_1 = int(n[1])
        n_2 = int(n[2])
        if n_1 == 0:
            str_ret += loza_reciept_approval.one_digit[n_2]
        elif n_1 == 1:
            str_ret += loza_reciept_approval.two_digits[n_2]
        elif n_2 == 0:
            str_ret += loza_reciept_approval.tens_multiple[n_1]
        else:
            str_ret += loza_reciept_approval.one_digit[n_2]
            str_ret += " و "
            str_ret += loza_reciept_approval.tens_multiple[n_1]
        return str_ret

    def three_digits(self, n):
        str_ret = ""
        huns_int = int(n[0])
        if huns_int != 0:
            str_ret += loza_reciept_approval.hundreds[huns_int]
        ones_int = int(n[2:])
        tens_int = int(n[1:])
        if tens_int != 0:
            if huns_int != 0:
                str_ret += " و "
            str_ret += self.two_digits_f(n)
        elif ones_int != 0:
            if huns_int != 0:
                str_ret += " و "
            str_ret += loza_reciept_approval.one_digit[ones_int]
        return str_ret

    def four_digits(self,n):
        str_ret = ""
        str_ret = loza_reciept_approval.one_digit[int(n[0])]
        str_ret += " ألف و "
        str_ret += self.three_digits(n[1:])
        return str_ret

    def five_digits(self,n):
        str_ret = ""
        str_ret = self.two_digits_f(n[0:2])
        str_ret += " ألف و "
        str_ret += self.three_digits(n[2:])
        return str_ret

    # arg = str
    def six_digits(self,n):
        str_ret = ""
        str_ret = self.three_digits(n[0:3])
        str_ret += " ألف و "
        str_ret += self.three_digits(n[3:])
        return str_ret

    def seven_digits(self,n):
        str_ret = ""
        str_ret = loza_reciept_approval.one_digit[int(n[0])]
        str_ret += " مليون و "
        str_ret += self.six_digits(n[1:])
        return str_ret

    def eight_digits(self,n):
        str_ret = ""
        str_ret = self.two_digits_f(n[0:2])
        str_ret += " مليون و "
        str_ret += self.six_digits(n[2:])
        return str_ret

    def nine_digits(self,n):
        str_ret = ""
        str_ret = self.three_digits(n[0:3])
        str_ret += " مليون و "
        str_ret += self.six_digits(n[3:])
        return str_ret

    def ten_digits(self,n):
        str_ret = ""
        str_ret = loza_reciept_approval.one_digit[int(n[0])]
        str_ret += " مليار و "
        str_ret += self.nine_digits(n[1:])
        return str_ret


    def _generate_total_in_string(self):
        # first we need to break the number into digits and loop through them.
        # with some logic
        for doc in self:
            number = 0.0
            if doc.amount:
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
                lower_digits_count = length - dec_digit -1
                num = strn[0:dec_digit]
                dec = strn[dec_index_1:length]
            else:
                num_digits = length
                num = strn
                lower_digits_count = 0
                dec = "000"

            # make sure lower digit count is 3
            if lower_digits_count > 3:
                lower_digits_count = 3
                dec = dec[0:3]

            str_ret = ""
            index = 0
            dec_len = len(num)
            if dec_len == 1:
                str_ret += loza_reciept_approval.one_digit[int(num)]
            if dec_len == 2:
                str_ret += doc.two_digits_f(" " + num)
            if dec_len == 3:
                str_ret += doc.three_digits(num)
            if dec_len == 4:
                str_ret += doc.four_digits(num)
            if dec_len == 5:
                str_ret += doc.five_digits(num)
            if dec_len == 6:
                str_ret += doc.six_digits(num)
            if dec_len == 7:
                str_ret += doc.seven_digits(num)
            if dec_len == 8:
                str_ret += doc.eight_digits(num)
            if dec_len == 9:
                str_ret += doc.nine_digits(num)
            if dec_len == 10:
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
            #now we have a normalized digits of three digits
            dec_num = len(dec)
            if int(dec) == 0:
                str_ret += " فقط"
                return str_ret

            # check if we have actually a number
            if int(num) > 0:
                str_ret += " و "

            if dec_num == 1:
                dec_2 = int(dec[2:])
                str_ret += loza_reciept_approval.one_digit[dec_2]
            if dec_num == 2:
                str_ret += doc.two_digits_f(doc,dec)
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
            self.total_string = self._generate_total_in_string()


    @api.onchange('check_ids')
    def onchange_check_ids(self):
        amount_tmp = 0
        for rec in self:
            if rec.check_ids:
                for txid in rec.check_ids:
                    if txid:
                        amount_tmp += txid.amount
            self.amount = amount_tmp
            self.total = amount_tmp
            self.total_string = self._generate_total_in_string()

