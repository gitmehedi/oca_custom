from odoo import api, fields, models, _
from odoo import exceptions


class RnD(models.Model):
    _name = 'rnd.rostering'

    name = fields.Char(string='Number')
    line_ids = fields.One2many('rnd.rostering.line', 'line_id', string='Hours')

    @api.multi
    def exceptions_msg(self):
        print "dddddddddddddddddddddddddddd"
        wizard_form = self.env.ref('rnd_hr.error_exception_wizard_view', False)
        view_id = self.env['error.exception.wizard']
        # vals = {
        #     'name': 'this is for set name',
        # }
        # new = view_id.create(vals)
        return {
            'name': _('Hi I am wfdsafsafsadfizard, I am from python code'),
            'type': 'ir.actions.act_window',
            'res_model': 'error.exception.wizard',
            'res_id': view_id.id,
            'view_id': wizard_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'various_id': self.id}
        }

        # raise exceptions.UserError(_('This is UserError'))
        # raise exceptions.RedirectWarning(_())
        # raise exceptions.RedirectWarning(_('This is RedirectWarning'), 2, _('Go to the configuration panel'))
        # raise exceptions.AccessDenied(_('This is AccessDenied'))
        # raise exceptions.AccessError(_('This is AccessError'))
        # raise exceptions.MissingError(_('This is MissingError'))
        # raise exceptions.ValidationError(_('This is ValidationError'))
        # raise exceptions.DeferredException(_('This is DeferredException'))
        #
        #
        # @api.one
        # def another_function(self):
        #     return 'Mehedi'

        # raise exceptions.UserError(_('This is UserError'))


class RnDLine(models.Model):
    _name = 'rnd.rostering.line'

    hours = fields.Integer(string='Hours')
    line_id = fields.Many2one('rnd.rostering')
