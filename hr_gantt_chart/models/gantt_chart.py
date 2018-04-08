from openerp import models, fields, api, exceptions

class GanttChart(models.Model):
    _name='gantt.chart'

    # Model Fields
    name = fields.Char(string='Name', size=100, required=True, help='Please enter name.')
    date_start=fields.Date(string='Date Start', size=500, help='Please enter description.')
    date_stop=fields.Date(string='Date Stop', size=500, help='Please enter description.')
    is_active=fields.Boolean(string='Active', default=True)

    parent_id = fields.Many2one('gantt.chart.parent')
