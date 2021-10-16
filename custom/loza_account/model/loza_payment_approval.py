from odoo import models, fields, api, _
from datetime import datetime, timedelta

class loza_payment_approval(models.Model):
    _name = "loza.payment.approval"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'resource.mixin', 'image.mixin']

    _order = "saraf_id desc"
    _rec_name = "saraf_id"
    _sql_constraints = [
        ('name_uniq', 'unique (saraf_id)', 'The name of the Saraf Document')
    ]

    saraf_id = fields.Char(string='أذن الصرف', copy=False,  readonly=True)


    partner_id = fields.Many2one('res.partner', string="أسم الجهة")
    partner_type = fields.Selection([
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    ], string='Recipient Type', default='employee')

    saraf_type = fields.Selection([
        ('cash', 'Cash'),
        ('check', 'Cheaque'),
        ('wire', 'Transfer'),
    ], string='Saraf Type', default='cash')

    employee_id = fields.Many2one('hr.employee', string="Employee")
    saraf_category = fields.Many2one('loza.payment.category', string="Category of Saraf")
    department_id = fields.Many2one('account.journal',string='مركز التكلفة')
#    journal_id = fields.Many2one('account.journal', string="Journal")
    partner_bank_id = fields.Many2one('res.partner.bank', string="Wire To/Bank Account")
    bank_id = fields.Many2one('res.partner.bank', string="From Company/Bank Account")
    wire_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External'),
    ], string='Wire Type', default='internal')

    payment_date = fields.Date(string="Payment Date", default=datetime.today())

    @api.model
    def _get_default_currency(self):
        return self.env.company.currency_id
 #       return self.journal_id.company_id.currency_id


    payment_id = fields.Many2one('account.payment', string="سجل المدفوع")
    recepient_id = fields.Many2one('res.partner', string="أسم المستلم")
    recepient_id_no = fields.Char(string='رقم الهوية')

    currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    amount = fields.Monetary(string='Amount',currency_field='currency_id',compute="_compute_amount", readonly=True)
 #   debit_account_id = fields.Many2one('account.account', string="Debit Account")
 #   credit_account_id = fields.Many2one('account.account', string="Credit Account")
    total = fields.Float(string="Total")
    total_string = fields.Char(string="Total in letters")
    transaction_ids = fields.One2many('transaction.cash.payment', 'saraf_id',string="Cash Transactions Details", copy=False)
    wire_ids = fields.One2many('transaction.wire', 'saraf_id',string="Wire Transactions Details", copy=False)
    check_ids = fields.One2many('transaction.check.payment', 'saraf_id',string="Check Transactions Details", copy=False)
    attachment_ids = fields.One2many('loza.transaction.attachment', 'saraf_id', string="Attachments", copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Auditing'),
        ('audited', 'CFO Approval'),
        ('cfo_approved', 'For Payment'),
        ('accounts', 'Accountants'),
        ('done', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string='State', readonly=True, default='draft')

    def _get_default_user(self):
        #TODO check if employee exists, just in case
        return self.env['hr.employee'].search([('user_id','=',self.env.user.id)],limit=1)

    prepare_id = fields.Many2one('hr.employee', string="إعداد",default=_get_default_user,readonly=1)
    auditor_id = fields.Many2one('hr.employee', string="المراجع الداخلي")
    cfo_id = fields.Many2one('hr.employee', string="المدير المالي")
    safecarer_id = fields.Many2one('hr.employee', string="أمين الخزينة")
    # hof_id = fields.Many2one('hr.employee', string="أمين الصندوق")
    # chairman_id = fields.Many2one('hr.employee', string="رئيس اللجنة")

    bank_account = fields.Many2one('res.partner.bank',string='رقم الحساب')
    bank_name = fields.Char(string="أسم المصرف")


    @api.onchange('bank_account')
    def onchange_bank_account(self):
        amount_tmp = 0;
        for rec in self:
            if rec.bank_account:
                rec.bank_name = rec.bank_account.bank_id.name
                self.bank_name = rec.bank_name
        return {}

    @api.model
    def create(self, vals):
        vals['saraf_id'] = self.env['ir.sequence'].next_by_code('loza.payment.approval') or 'SRF'
        result = super(loza_payment_approval, self).create(vals)
        msg_body = 'تم إنشاء إذن الصرف'
        for msg in self:
            msg.message_post(body=msg_body)
        return result

    def _lock_transactions(self,lock_type='half_lock'):
        for t in self.transaction_ids:
            t.state = lock_type
        for t in self.check_ids:
            t.state = lock_type
        for t in self.wire_ids:
            t.state = lock_type

    def action_confirm_saraf(self):
        msg_body = 'تم تأكيد إذن الصرف'
        for msg in self:
            msg.message_post(body=msg_body)
        # half-lock the transactions
        self._lock_transactions('half_lock')
        self.write({'state': "ready"})
        return

    def action_confirm_audit(self):
        msg_body = 'تم أعتماده من المراجعة'
        for msg in self:
            msg.message_post(body=msg_body)
        self.write({'state': "audited"})
        return

    def action_do_saraf(self):
        msg_body = 'تم الصرف والترحيل'
        for msg in self:
            msg.message_post(body=msg_body)
        self.write({'state': "done"})
        return

    def action_do_return(self):
        msg_body = 'لم تعتمد'
        for msg in self:
            msg.message_post(body=msg_body)
        # half-lock the transactions
        self._lock_transactions('open')
        self.write({'state': "draft"})
        return



    def action_confirm_cash_registrar(self):
        msg_body = 'تم الدفع وتحويله إلى الحسابات من قبل أمين الخزينة'
        for msg in self:
            msg.message_post(body=msg_body)
        # lock transactions
        self.write({'state': "accounts"})
        return

    def action_confirm_post_accounts(self):
        if self.saraf_type == 'cash':
            for tx in self.transaction_ids:
                jid = self.env['account.journal'].search([('name', '=', 'الخزينة الرئيسية')],limit=1)
                account_payable = self.env['account.account'].search([('code','=','211000')])

                payment_method_id = self.env.ref('account.account_payment_method_manual_out').id
                partner_id = self.partner_id.id
                company_id = self.env.ref('base.main_company').id

                payment = self.env['account.payment'].create({
                    'payment_type'          : 'outbound',
                    'amount'                : tx.amount,
                    'ref'                   : tx.description,
                    'currency_id'           : self.env.company.currency_id.id,
                    'date'                  : datetime.now().strftime('%Y') + '-' + '09' + '-01',
                    'is_internal_transfer'  : False,
                    'partner_type'          : 'supplier',
                    'destination_account_id': account_payable.id,
                    'journal_id'            : jid.id,
                    'payment_method_id'     : payment_method_id,
                    'partner_id'            : partner_id,
                    'company_id'            : company_id,
                })
        # if self.saraf_type == 'check':
        #     jid = self.env['account.journal'].search([('bank_account_id', '=', self.bank_account.id)], limit=1).id
        #     for tx in self.check_ids:
        #         payment = self.env['account.payment'].create({
        #             'payment_type': 'outbound',
        #             'amount': tx.amount,
        #             'ref': tx.,
        #             'currency_id': self.env.company.currency_id.id,
        #             'journal_id': jid,
        #             'destination_account_id': self.credit_account_id.id,
        #             'company_id': self.env.ref('base.main_company').id,
        #             'date': datetime.now().strftime('%Y') + '-' + '09' + '-01',
        #             'partner_id': self.partner_id.id,
        #             'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id,
        #             'is_internal_transfer': False,
        #         })

        payment.action_post()
        self.payment_id = payment.id
        msg_body = 'تم الدفع وتحويله إلى قيد من قبل أمين الخزينة'
        for msg in self:
            msg.message_post(body=msg_body)
        self.write({'state': "done"})
        return

    # def action_confirm_hof(self):
    #     msg_body = 'تم إعتماد إذن الصرف من أمين الصندوق'
    #     for msg in self:
    #         msg.message_post(body=msg_body)
    #     self.write({'state': "hof_approved"})
    #     activity_type = self.env.ref('loza_account.loza_chairman_approval')
    #     deadline_date = fields.Date.today() + timedelta(days=5)
    #
    #     create_vals = {
    #         'activity_type_id': activity_type.id,
    #         'summary': 'إذن الصرف جاهز للاعتماد من  رئيس المجلس',
    #         #                    'automated': True,
    #         'note': 'urgent in 5 days',
    #         'date_deadline': deadline_date,
    #         'res_model_id': self.env['ir.model'].search([('model', '=', 'loza.payment.approval')], limit=1).id,
    #         'res_id': self.id,
    #         'user_id': activity_type.default_user_id.id
    #     }
    #     self.env['mail.activity'].create(create_vals)
    #     return
    #
    # def action_confirm_chairman(self):
    #     msg_body = 'تم إعتماد إذن الصرف من رئيس مجلس الإدارة'
    #     for msg in self:
    #         msg.message_post(body=msg_body)
    #     self.write({'state': "chairman_approved"})
    #     return

    def action_confirm_cfo(self):
        msg_body = 'تم إعتماد إذن الصرف من رئيس قسم المالية'
        for msg in self:
            msg.message_post(body=msg_body)
        self.write({'state': "cfo_approved"})
        activity_type = self.env.ref('loza_account.loza_cfo_approval')
        deadline_date = fields.Date.today() + timedelta(days=3)

        create_vals = {
            'activity_type_id': activity_type.id,
            'summary': 'إذن الصرف جاهز للاعتماد من أمين الصندوق',
            #                    'automated': True,
            'note': 'urgent in 5 days',
            'date_deadline': deadline_date,
            'res_model_id': self.env['ir.model'].search([('model', '=', 'loza.payment.approval')], limit=1).id,
            'res_id': self.id,
            'user_id': activity_type.default_user_id.id
        }
        self.env['mail.activity'].create(create_vals)
        return
    def action_cancelled(self):
        msg_body = 'تم إلغاء إذن الصرف'
        for msg in self:
            msg.message_post(body=msg_body)
        self.write({'state': "cancelled"})
        return


    def _compute_amount(self):
        for doc in self:
            total_untaxed = 0.0
            if doc.saraf_type == 'cash':
                for line in doc.transaction_ids:
                    total_untaxed += line.amount
            elif doc.saraf_type == 'wire':
                for line in doc.wire_ids:
                    total_untaxed += line.amount
            else:
                for line in doc.check_ids:
                    total_untaxed += line.amount

            doc.amount = total_untaxed
            doc.total_string = doc._generate_total_in_string()

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
            str_ret += loza_payment_approval.one_digit[n_2]
        elif n_1 == 1:
            str_ret += loza_payment_approval.two_digits[n_2]
        elif n_2 == 0:
            str_ret += loza_payment_approval.tens_multiple[n_1]
        else:
            str_ret += loza_payment_approval.one_digit[n_2]
            str_ret += " و "
            str_ret += loza_payment_approval.tens_multiple[n_1]
        return str_ret

    def three_digits(self, n):
        str_ret = ""
        huns_int = int(n[0])
        if huns_int != 0:
            str_ret += loza_payment_approval.hundreds[huns_int]
        ones_int = int(n[2:])
        tens_int = int(n[1:])
        if tens_int != 0:
            if huns_int != 0:
                str_ret += " و "
            str_ret += self.two_digits_f(n)
        elif ones_int != 0:
            if huns_int != 0:
                str_ret += " و "
            str_ret += loza_payment_approval.one_digit[ones_int]
        return str_ret

    def four_digits(self,n):
        str_ret = ""
        str_ret = loza_payment_approval.one_digit[int(n[0])]
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
        str_ret = loza_payment_approval.one_digit[int(n[0])]
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
        str_ret = loza_payment_approval.one_digit[int(n[0])]
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
                str_ret += loza_payment_approval.one_digit[int(num)]
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
                str_ret += loza_payment_approval.one_digit[dec_2]
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
            rec.amount = amount_tmp
            rec.total = amount_tmp
            rec.total_string = self._generate_total_in_string()

    @api.onchange('wire_ids')
    def onchange_wire_ids(self):
        amount_tmp = 0
        for rec in self:
            if rec.wire_ids:
                for txid in rec.wire_ids:
                    if txid:
                        amount_tmp += txid.amount
            rec.amount = amount_tmp
            rec.total = amount_tmp
            rec.total_string = self._generate_total_in_string()

    @api.onchange('check_ids')
    def onchange_check_ids(self):
        amount_tmp = 0
        for rec in self:
            if rec.check_ids:
                for txid in rec.check_ids:
                    if txid:
                        amount_tmp += txid.amount
            rec.amount = amount_tmp
            rec.total = amount_tmp
            rec.total_string = self._generate_total_in_string()


    @api.onchange('employee_id')
    def onchange_employee_id(self):
        amount_tmp = 0
        for rec in self:
            if rec.employee_id:
                rec.partner_id = rec.employee_id.address_id
