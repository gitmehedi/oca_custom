from openerp import models, fields, api, exceptions

class GanttChartParent(models.Model):
    _name='gantt.chart.parent'

    # Model Fields
    name=fields.Char(string='Name', size=100, required=True, help='Please enter name.')
    is_active=fields.Boolean(string='Active', default=True)

