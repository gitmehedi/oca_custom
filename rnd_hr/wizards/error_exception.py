from odoo import models, fields,api,_

class ErrorExceptionWizard(models.Model):
    _name='error.exception.wizard'

    # name = fields.Char()


    @api.one
    def update_date(self,context=None):
        print "normal function call from wizard."

