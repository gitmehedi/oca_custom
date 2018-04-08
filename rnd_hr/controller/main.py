# -*- coding: utf-8 -*-

import json

from collections import OrderedDict
from openerp import http  # @UnresolvedImport
from openerp.addons.website.controllers.main import Website
from openerp.http import request  # @UnresolvedImport

FIELDS = ['id', 'parent_id', 'name', 'job_id', 'work_location',
          'work_email', 'work_phone', 'mobile_phone']
ADDITION = {
    'work_phone': "Phone: %s",
    'mobile_phone': "Mobile: %s"
}


class Main(Website):

    @http.route(['/burndown/get_chart/<int:emp_id>'],
                type='http', auth="public", website=True)
    def get_chart(self,emp_id):

        Model = request.env['rnd.rostering'].sudo()
        ids = Model.browse(emp_id)
        # manager = employee_ids.parent_id
        # employee_ids |= manager
        # employee_ids |= Model.search([('parent_id', 'child_of', employee_id)])
        # data_source = self.get_chart_data_source(employee_ids)
        print emp_id,"Values:", [val.hours for val in ids.line_ids]
        data = {"values":[val.hours for val in ids.line_ids]}


        return json.dumps(data)

    def get_chart_data_source(self, employee_ids):
        baseUri = '/web/image/' + 'hr.employee/'
        res = []
        for employee in employee_ids:
            employee_dict = OrderedDict()
            for field in FIELDS:
                field_value = None
                if field == "parent_id":
                    field_value = getattr(employee, field, None)
                    field_value = field_value and field_value.id or None
                elif field.endswith("id") and field != 'id':
                    field_value = getattr(employee, field, None)
                    field_value = field_value and field_value.name or ''
                else:
                    field_value = getattr(employee, field, None)

                field_value = field in ADDITION and field_value and (
                    ADDITION[field] % field_value) or field_value
                employee_dict[field] = field_value
            employee_dict['image'] = baseUri + str(employee.id) + '/image'
            res.append(employee_dict)
        return res
