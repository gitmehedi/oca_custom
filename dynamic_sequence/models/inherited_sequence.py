from openerp import models, fields, api, exceptions


class IRSequence(models.Model):
    _inherit = 'ir.sequence'

    operating = fields.Char(string='Operating')

    def get_next_char(self, number_next):
        res = super(IRSequence, self).get_next_char(number_next)
        return self.operating + '/' + res
