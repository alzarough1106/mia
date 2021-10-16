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
#from datetime import datetime, date
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class AccountPayment(models.Model):
	_inherit = 'account.payment'

	def action_saraf(self):
		return