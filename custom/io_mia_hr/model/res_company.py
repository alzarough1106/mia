# -*- coding: utf-8 -*-
############################################################################
#
# Abr Afrikia LTD CONFIDENTIAL
# __________________
#
#  [2020] - [2021] Abr Afrikia Limited - Tripoli Libya
#  All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of Abr Afrikia Limited and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to Abr Afrikia Limited
# and its suppliers and may be covered by International Laws and Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Abr Afrikia Limited
#
#############################################################################
from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def create(self, vals):
        inherit_id = vals.get('inherit_id', False)
        if inherit_id:
            # this is an inheritance
            del vals['inherit_id']
            super(ResCompany, self.browse(inherit_id)).write(vals)
            return self
        return super(ResCompany, self).create(vals)
