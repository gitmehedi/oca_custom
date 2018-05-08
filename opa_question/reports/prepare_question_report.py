from odoo import models, fields, api


class QuestionsPaperReport(models.AbstractModel):
    _name = 'report.opa_question.prepare_questions_qweb'

    @api.model
    def get_report_values(self, docids, data=None):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
        }
