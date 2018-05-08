from datetime import datetime

from odoo import models, fields, api


class QuestionPaper(models.TransientModel):
    _name = 'questions.paper.wizard'

    limit = fields.Integer(string='Question Limit', required=True, default=50)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date', default=datetime.now())

    category_id = fields.Many2one('question.category', string='Category', required=True)
    subject_id = fields.Many2one('exam.subject', string='Subject', required=True)

    @api.multi
    def report_print(self):
        data = {
            'category_id': self.category_id.id,
            'category_name': self.category_id.name,
            'subject_id': self.subject_id.id,
            'subject_name': self.subject_id.name,
            'limit': self.limit,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
        data['form'].update(self.read(
            ['limit', 'start_date', 'end_date', 'category_id', 'subject_id'])[0])

        return self.env.ref('opa_question.action_report_prepare_questions').report_action(self, data=data)
