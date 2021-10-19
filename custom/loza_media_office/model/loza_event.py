# -*- coding: utf-8 -*-
############################################################################
#
# LOZA LTD CONFIDENTIAL
# __________________
#
#  [2020] - [2021] Loza Limited - Tripoli Libya
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Loza Limited and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to Loza Limited
# and its suppliers and may be covered by International Laws and Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Loza Limited
#
#############################################################################

from odoo import api, fields, models, _
from datetime import date, datetime
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import pytz

class loza_event(models.Model):
    _name = "loza.event"
    _inherit = 'mail.thread'
    _event = 'date desc'
    _rec_name = 'sequence'
    _description = 'An Event for execution'

    sequence = fields.Char(string="Event ID", readonly=True, copy=True)
    title = fields.Char(string="Title of the Event", )
    date = fields.Datetime(string='Event Date')
    summary = fields.Text(string="Event Summary", )
    place = fields.Many2many('loza.office',string='Places')
    quests = fields.Many2many('loza.event.quest',string='Quests')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('approved', 'Approved'),
        ('distributed', 'Distributed'),
        ('finished', 'Finished'),
        ('close', 'Close'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    type = fields.Selection([
        ('conferences', 'Conferences'),
        ('vip events', 'VIP Events'),
        ('poll', 'Poll'),
    ], string='Event Type', readonly=True, index=True, copy=False, default='conference', tracking=True)

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('loza.event')
        result = super(loza_event, self).create(vals)
        return result


    # currency_id = fields.Many2one('res.currency', string='Currency', default=_get_default_currency)
    # list_price = fields.Float('Price', digits='Product Price', related="consultations_id.list_price")
    # price_letter = fields.Char(string="السعر بالحروف")
    # institution_partner_id = fields.Many2one('res.partner', domain=[('is_institution', '=', True)],
    #                                          string="Health Center")
    # comission_paid = fields.Boolean(string="Commission Paid?", default=False)
    # comission_id = fields.Many2one('account.move', 'Commission Invoice')
    # radiology_count = fields.Integer(compute='get_radiology_count')
    # nurse = fields.Many2one('loza.nurse', string='Nurse', default=_get_nurse)
    # nurse_case = fields.Boolean(string="Nurse Case?", default=False)
    #
    # @api.model
    # def _default_clinic(self):
    #     return self.env.ref('loza_core_hms.default_loza_clinic_emergency_sub_category').id
    #
    # def _default_service(self):
    #     # go to default if exists
    #     return self.env.ref('loza_clinic.product_product_free_entry')
    #     # return self.env['product.product'].search(
    #     #     [('categ_id', '=', emergency.service_category.id), ('group_default', '=', True)], limit=1)
    #
    # def get_event_count(self):
    #     count = self.env['loza.make.event.appointment'].search_count([('ambulance_id', '=', self.id)])
    #     self.event_count = count
    #
    # event_count = fields.Integer(compute='get_event_count')
    #
    # def get_bills_count(self):
    #     count = self.env['account.move'].search_count([('partner_id', '=', self.patient_id.patient_id.id),
    #                                                    ('payment_state', 'in', ('not_paid', 'in_payment', 'partial'))])
    #     self.bills_count = count
    #
    # bills_count = fields.Integer(compute='get_bills_count')
    #
    # #	inpatient_registration_id = fields.Many2one('medical.inpatient.registration',string="Inpatient Registration")
    # # inpatient_registration_id = fields.Many2one('medical.inpatient.registration',string="Inpatient Registration")
    # patient_status = fields.Selection([
    #     ('ambulatory', 'Ambulatory'),
    #     ('outpatient', 'Outpatient'),
    #     ('inpatient', 'Inpatient'),
    # ], 'Patient status', default='ambulatory', readonly="1")
    # patient_id = fields.Many2one('loza.patient', 'Patient', required=True)
#     urgency_level = fields.Selection([
#         ('normal', 'Normal'),
#         ('urgent', 'Urgent'),
#         ('emergency', 'Medical Emergency'),
#     ], 'Urgency Level', default="emergency")
#     barcode = fields.Char('Barcode', compute='_compute_barcode', inverse='_set_barcode', search='_search_barcode')
#     appointment_count = fields.Integer(string='Lab Request', compute='get_appointment_count')
#     appointment_date = fields.Datetime('Ambulance Date', required=True, default=datetime.now())
#     appointment_end = fields.Datetime('Appointment End')
#     doctor_id = fields.Many2one('loza.physician', 'Physician', domain="[('is_ambulance', '=', True)]")
#     nurse_id = fields.Many2one('loza.nurse', 'Nurse')
#     clinic = fields.Many2one('loza.clinic', string='Clinic', required=True, readonly="True", default=_default_clinic)
#     attendance_ids = fields.One2many('resource.calendar.attendance', 'calendar_id', 'Working Time',
#                                      readonly=False, copy=True,
#                                      related='resource_calendar_id.attendance_ids')
#     resource_calendar_id = fields.Many2one('resource.calendar', string='Working Times',
#                                            related='doctor_id.resource_calendar_id')
#     duration = fields.Integer('Duration', default='1')
#
#     # TODO: Move it to the Hospitalization Module
#     no_invoice = fields.Boolean(string='Invoice exempt', default=False)
#     validity_status = fields.Selection([
#         ('invoice', 'Invoice'),
#         ('tobe', 'To be Invoiced'),
#     ], 'Validity Status', readonly=True, default='tobe')
#
#     appointment_validity_date = fields.Datetime('Validity Date')
#     consultations_id = fields.Many2one('product.product', 'Emergency Service', required=True, default=_default_service)
#     # comments = fields.Text(string="Comments")
# #    followup = fields.Datetime(string="Followup", default=datetime.now())
#     complaints = fields.Text(string="Complaints")
#     examination = fields.Text(string="Examination")
#     advice = fields.Text(string="Advice")
#     diagnosis = fields.Text(string="Diagnosis")
#     insured_companies = fields.Char(string="Insured Companies", store=True, related='patient_id.insured_companies')
#     id_number = fields.Integer(string="Id Number", store=True, related='patient_id.id_number')
#     employer = fields.Char(string="Employer", store=True, related='patient_id.employer')
#     insurance = fields.Selection(string="Insurance", store=True, related='patient_id.insurance')
#     # invoice_to_insurer = fields.Boolean('Invoice to Insurance')
#     # medical_patient_psc_ids = fields.Many2many('medical.patient.psc',string='Pediatrics Symptoms Checklist')
#     loza_prescription_event_ids = fields.One2many('loza.prescription.event', 'appointment_id', string='Prescription')
#     Prescription_count = fields.Integer(compute='get_Prescription_count')
#     name_pa = fields.Integer(compute='get_name_pa')
#     # insurer_id = fields.Many2one('loza.insurance','Insurer')
#     Results_count = fields.Integer(compute='get_Results_count')
#     user_id = fields.Many2one('res.users', string='My User', readonly='True', default=lambda self: self.env.user)
#     transfer = fields.Many2one('loza.clinic.transfer', string="Transfer Note")

    # @api.depends('patient_id.barcode')
    # def _compute_barcode(self):
    #     self.barcode = False
    #     for template in self:
    #         if len(template.patient_id) == 1:
    #             template.barcode = template.patient_id.barcode
    #
    # def _set_barcode(self):
    #     if len(self.patient_id) == 1:
    #         self.patient_id.barcode = self.barcode
    #
    # def _search_barcode(self, operator, value):
    #     templates = self.with_context(active_test=False).search([('patient_id.barcode', operator, value)])
    #     return [('id', 'in', templates.ids)]
    #
    # @api.onchange('appointment_date')
    # def onchange_appointment_date(self):
    #     for rec in self:
    #         if rec.appointment_date:
    #             d1 = rec.appointment_date
    #             hour = d1.hour + rec.duration
    #             d2 = d1 + timedelta(hours=1)
    #             rec.appointment_validity_date = d2
    #
    # def open_patient_History(self):
    #     return {
    #         'name': _('patient History'),
    #         'domain': [('patient_id', '=', self.patient_id.id)],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.ambulance',
    #         'type': 'ir.actions.act_window',
    #     }
    #
    # def open_radiology_events(self):
    #     return {
    #         'name': _('Radiology History'),
    #         'domain': [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('source_type', '=', '1')],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.radiology',
    #         'type': 'ir.actions.act_window',
    #     }
    #
    # # def open(self):
    # #     return {datetime.now()}
    #
    # def open_Lab_request(self):
    #     return {
    #         'name': _('Analysis Test Request'),
    #         'domain': [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('state', '!=', 'done'),
    #                    ('state', '!=', 'cancel'), ('state', '!=', 'disable')],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.patient.lab.test',
    #         'type': 'ir.actions.act_window',
    #     }
    #
    # def open_Lab_Results(self):
    #     return {
    #         'name': _('Analysis Results'),
    #         'domain': [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('state', '=', 'closed')],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.lab',
    #         'type': 'ir.actions.act_window',
    #     }
    #
    # def open_prescription_request(self):
    #     return {
    #         'name': _('Prescription'),
    #         'domain': [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id)],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.prescription.event.quick',
    #         'type': 'ir.actions.act_window',
    #     }
    #
    # def get_appointment_count(self):
    #     count = self.env['loza.patient.lab.test'].search_count(
    #         [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('source_type', '=', '1'),
    #          ('state', '!=', 'done'),
    #          ('state', '!=', 'cancel'), ('state', '!=', 'disable')])
    #     self.appointment_count = count
    #
    # def get_Prescription_count(self):
    #     count = self.env['loza.prescription.event.quick'].search_count(
    #         [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id)])
    #     self.Prescription_count = count
    #
    # def get_Results_count(self):
    #     count = self.env['loza.lab'].search_count(
    #         [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('state', '=', 'closed')])
    #     self.Results_count = count
    #
    # def get_name_pa(self):
    #     count = self.env['loza.appointment'].search_count([('patient_id', '=', self.patient_id.id)])
    #     self.name_pa = count
    #
    # def loza_patient_outstanding_bills(self):
    #     return {
    #         'name': _('Outstanding Bills'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'tree,form',
    #         'binding_view_types': 'tree',
    #         'domain': [('partner_id', '=', self.patient_id.patient_id.id),
    #                    ('payment_state', 'in', ('not_paid', 'in_payment', 'partial'))],
    #         'res_model': 'account.move',
    #         'context': {
    #             'source_id': self.id,
    #             'source_type': '1',
    #             'patient_id': self.patient_id.id,
    #             'doctor_id': self._get_doctor_id(),
    #         }
    #     }
    #
    # def action_prepare_invoices(self):
    #     # go through the module  itself
    #     if not self.invoice_id:
    #         self.create_clinic_invoice(True)
    #
    #     # radiology time
    #     list = self.env['loza.radiology'].search(
    #         [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('source_type', '=', '1'),
    #          ('state', '=', 'ready')])
    #     for rad in list:
    #         if not rad.is_invoiced:
    #             rad.create_radiology_invoice(True)
    #         else:
    #             # it has been invoiced but not paid
    #             if rad.invoice_id.state == 'draft':
    #                 rad.invoice_id.action_post()
    #
    #     # Lab Analysis
    #     list = self.env['loza.patient.lab.test'].search(
    #         [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('source_type', '=', '1'),
    #          ('state', '=', 'ready')])
    #     for lab in list:
    #         if not lab.is_invoiced:
    #             lab.action_create_lab_invoice2(True)
    #         else:
    #             # it has been invoiced but not paid
    #             if lab.invoice_id.state == 'draft':
    #                 lab.invoice_id.action_post()
    #     # Events
    #     list = self.env['loza.make.event.appointment'].search(
    #         [('ambulance_id', '=', self.id), ('state', '=', 'submitted')])
    #     for event in list:
    #         if not event.is_invoiced:
    #             event.action_create_event_invoice(True)
    #         else:
    #             # it has been invoiced but not paid
    #             if event.invoice_id.state == 'draft':
    #                 event.invoice_id.action_post()
    #     # Last Check, if there are no invoices and the state is draft, move it to paid
    #     if self.bills_count == 0:
    #         if self.state == 'new':
    #             #move it to paid state
    #             self.write({'state': "paid"})
    #     return
    #
    # def action_loza_appointment_cancelled(self):
    #     if self.state == 'new':
    #         if self.is_invoiced == True:
    #             if self.invoice_id:
    #                 self.invoice_id.button_cancel()
    #                 # msg_body = 'moved state to canceled'
    #                 # for msg in self:
    #                 #     msg.message_post(body=msg_body)
    #
    #     self.write({'state': "cancelled"})
    #     return
    #
    # def action_loza_appointment_closed(self):
    #     appointment_listings = self.env['loza.make.event.appointment'].search([('ambulance_id', '=', self.id)])
    #
    #     if not self.complaints:
    #         raise UserError("You have forgotten to write the initial complaints")
    #     if not self.examination:
    #         raise UserError("You have forgotten to write an examination")
    #     if not self.diagnosis:
    #         raise UserError("You have forgotten to write a diagnosis")
    #     if not self.advice:
    #         raise UserError("You have forgotten to write an advice")
    #
    #     for listing in appointment_listings:
    #         if listing.state not in ('paid', 'cancelled'):
    #             raise UserError("There is an Event which has not been Paid/Closed")
    #
    #
    #     radiology = self.env['loza.radiology'].search(
    #         [('patient_id', '=', self.patient_id.id), ('source_id', '=', self.id), ('source_type', '=', '1')])
    #     for listing in radiology:
    #         if listing.state in ('ready', 'draft'):
    #             raise UserError("There is a Radiology Report which has not been Paid/Closed")
    #
    #     lab_requests = self.env['loza.patient.lab.test'].search(
    #         [
    #             ('patient_id', '=', self.patient_id.id),
    #             ('source_id', '=', self.id), ('source_type', '=', '1'),
    #             ('state', 'not in', ('done', 'cancel', 'disable'))
    #          ])
    #
    #     for listing in lab_requests:
    #         if listing.state in ('ready', 'draft'):
    #             raise UserError("There is a Lab Test which has not been Paid/Closed")
    #         # msg_body = 'moved state to closed'
    #         # for msg in self:
    #         #     msg.message_post(body=msg_body)
    #     self.write({'state': "closed"})
    #     return
    #
    # # def action_loza_appointment_followup(self):
    # #     # msg_body = 'Moved State to followup'
    # #     # for msg in self:
    # #     #     msg.message_post(body=msg_body)
    # #     self.write({'state': "followup"})
    # #     return
    #
    # def action_loza_ambulance_paid(self):
    #     # msg_body = 'Moved State to paid'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     # TODO
    #     # get something for comission payment
    #     # util = loza_util_account.loza_util_account()
    #     # util.create_commission_invoice(self, 'ت.س.ع')
    #     self.write({'state': "paid"})
    #     return self.env['ir.model.data']
    #
    # def action_loza_appointment_draft(self):
    #     # msg_body = 'Moved State to new'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     self.write({'state': "new"})
    #
    #     return self.env['ir.model.data']
    #
    # @api.onchange('list_price')
    # def onchange_list_price(self):
    #     util = loza_util_account.loza_util_account()
    #     # self.price_letter = util.convert_number_to_alphabet(self.list_price)
    #     self.write({'price_letter': util.convert_number_to_alphabet(self.list_price)})
    #
    # @api.onchange('patient_id')
    # def onchange_name(self):
    #     # ins_obj = self.env['medical.insurance']
    #     # ins_record = ins_obj.search([('medical_insurance_partner_id', '=', self.patient_id.patient_id.id)])
    #     # if len(ins_record)>=1:
        # 	self.insurer_id = ins_record[0].id
        # else:
        # self.insurer_id = False
        # return

    # def make_event(self):
    #     return {
    #         'name': _('Make Event'),
    #         'view_mode': 'form',
    #         'res_model': 'loza.patient.lab.test',
    #         'type': 'ir.actions.act_window',
    #         'context': {'default_source_id': self.id, 'default_source_type': '1', },
    #     }
    #
    # # @api.onchange('inpatient_registration_id')
    # #	def onchange_patient(self):
    # #		if not self.inpatient_registration_id:
    # #			self.patient_id = ""
    # #		inpatient_obj = self.env['medical.inpatient.registration'].browse(self.inpatient_registration_id.id)
    # #		self.patient_id = inpatient_obj.id
    #
    # def confirm(self):
    #     # msg_body = 'Moved State to confirmed'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     self.write({'state': 'confirmed'})
    #
    # def done(self):
    #     # msg_body = 'Moved State to Done'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     self.write({'state': 'done'})
    #
    # def cancel(self):
    #     # msg_body = 'Moved State to cancel'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     self.write({'state': 'cancel'})
    #
    # def print_prescription(self):
    #     return self.env.ref('loza_core_hms.report_print_prescription').report_action(self)
    #
    # def view_patient_invoice(self):
    #     # msg_body = 'Moved State to cancel'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     self.write({'state': 'cancel'})
    #
    # def transfer_state(self):
    #     # create the transfer first
    #     # msg_body = 'Moved State to transfer'
    #     # for msg in self:
    #     #     msg.message_post(body=msg_body)
    #     self.write({'state': 'transfer'})
    #
    # def _get_doctor_id(self):
    #     doctor_id = None
    #     if self.doctor_id:
    #         doctor_id = self.doctor_id.id
    #     return doctor_id
    #
    # def create_clinic_invoice(self, returnNoData=True):
    #     active_id = self._context.get('active_id')
    #     list_of_ids = []
    #     lab_req_obj = self.env['loza.ambulance']
    #     account_invoice_obj = self.env['account.move']
    #     account_invoice_line_obj = self.env['account.move.line']
    #     ir_property_obj = self.env['ir.property']
    #     if active_id:
    #         lab_req = lab_req_obj.browse(active_id)
    #         lab_req.validity_status = 'invoice'
    #         #            seq = self.env['ir.sequence'].next_by_code('invoice.sequence')
    #         if lab_req.is_invoiced == True:
    #             raise UserError('All ready Invoiced.')
    #         passed_id = lab_req.name
    #         if lab_req.no_invoice == False:
    #             sale_journals = self.env['account.journal'].search([('code', '=', 'خ.س.ع')], limit=1)
    #             invoice_vals = {
    #                 'name': passed_id,
    #                 'invoice_origin': lab_req.name or '',
    #                 'move_type': 'out_invoice',
    #                 #                'ambulance_ref': lab_req.name,
    #                 'journal_id': sale_journals.id,
    #                 'payment_reference': passed_id,
    #                 'partner_id': lab_req.patient_id.patient_id.id or False,
    #                 'partner_shipping_id': lab_req.patient_id.patient_id.id,
    #                 'currency_id': lab_req.patient_id.patient_id.currency_id.id,
    #                 'invoice_payment_term_id': False,
    #                 'fiscal_position_id': lab_req.patient_id.patient_id.property_account_position_id.id,
    #                 'team_id': False,
    #                 'invoice_date': date.today(),
    #                 'doctor_id': lab_req._get_doctor_id(),
    #                 'company_id': lab_req.patient_id.patient_id.company_id.id or False,
    #                 'source_id': self.id,
    #                 'source_type': '1',
    #             }
    #             res = account_invoice_obj.create(invoice_vals)
    #             invoice_line_account_id = False
    #             if lab_req.consultations_id.id:
    #                 invoice_line_account_id = lab_req.consultations_id.property_account_income_id.id or lab_req.consultations_id.categ_id.property_account_income_categ_id.id or False
    #             if not invoice_line_account_id:
    #                 inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
    #             if not invoice_line_account_id:
    #                 raise UserError(_('There is no income account defined for this product: "%s". '
    #                                   'You may have to install a chart of account from Accounting app, '
    #                                   'settings menu.') % (lab_req.consultations_id.name,))
    #
    #             tax_ids = []
    #             taxes = lab_req.consultations_id.taxes_id.filtered(lambda
    #                                                                    r: not lab_req.consultations_id.company_id or r.company_id == lab_req.consultations_id.company_id)
    #             tax_ids = taxes.ids
    #             invoice_line_vals = {
    #                 'name': lab_req.consultations_id.name or '',
    #                 'account_id': invoice_line_account_id,
    #                 'price_unit': lab_req.consultations_id.lst_price,
    #                 'product_uom_id': lab_req.consultations_id.uom_id.id,
    #                 'quantity': 1,
    #                 'product_id': lab_req.consultations_id.id,
    #             }
    #
    #             res1 = res.write({'invoice_line_ids': ([(0, 0, invoice_line_vals)])})
    #             # post payment
    #             res.action_post()
    #
    #             list_of_ids.append(res.id)
    #             if list_of_ids:
    #                 imd = self.env['ir.model.data']
    #                 lab_req_obj_brw = lab_req_obj.browse(self._context.get('active_id'))
    #                 lab_req_obj_brw.write({'is_invoiced': True})
    #                 lab_req_obj_brw.write({'invoice_id': res.id})
    #                 action = imd.xmlid_to_object('account.action_move_out_invoice_type')
    #                 list_view_id = imd.xmlid_to_res_id('account.view_invoice_tree')
    #                 form_view_id = imd.xmlid_to_res_id('account.view_move_form')
    #                 result = {
    #                     'name': action.name,
    #                     'help': action.help,
    #                     'type': action.type,
    #                     'views': [[form_view_id, 'form']],
    #                     'target': action.target,
    #                     'context': action.context,
    #                     'res_model': action.res_model,
    #                     'res_id': res.id,
    #
    #                 }
    #                 if list_of_ids:
    #                     result['domain'] = "[('id','in',%s)]" % list_of_ids
    #         else:
    #             raise UserError(_(' The ambulance case is invoice exempt  '))
    #         if returnNoData:
    #             return res
    #         else:
    #             return result
    #
    # def loza_patient_event_history(self):
    #     return {
    #         'name': _('Event History'),
    #         'domain': [('ambulance_id', '=', self.id)],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.make.event.appointment',
    #         'type': 'ir.actions.act_window',
    #         'context': dict(
    #             self.env.context,
    #             ambulance_id=self.id,
    #         ),
    #     }
    #
    # def make_event_radiology_ambulance(self):
    #     return {
    #         'name': 'New Radiology Service',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'loza.radiology',
    #         'view_mode': 'form',
    #         'target': 'current',
    #         'context': {
    #             'default_patient_id': self.patient_id.id,
    #             'default_doctor_id': self._get_doctor_id(),
    #             'default_affiliate': '1',
    #             'default_source_id': self.id,
    #             'default_source_type': '1',  # Ambulance
    #         },
    #     }
    #
    # def action_clinic_transfer(self):
    #
    #     return {
    #         'name': 'Transfer Case',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'loza.clinic.transfer',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'res_id': self.transfer.id,
    #         'context': {
    #             'default_patient_id': self.patient_id.id,
    #             'default_ambulance_id': self.id,
    #         },
    #     }
    #
    # def open_inpatient(self):
    #     return {
    #         'name': 'Inpatient',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'loza.inpatient.registration',
    #         'view_mode': 'form',
    #         'target': 'new',
    #     }
    #
    # def open_payment_receipts(self):
    #     return {
    #         'name': _('Payment Receipts'),
    #         'domain': [('source_id', '=', self.id), ('source_type', '=', '1'), ('patient_id', '=', self.patient_id.id)],
    #         'view_mode': 'tree,form',
    #         'res_model': 'loza.receipt',
    #         'type': 'ir.actions.act_window',
    #     }
