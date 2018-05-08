# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class Subject(models.Model):
    _name = 'exam.subject'
    _description = 'Subject.'
    _order = 'id ASC'

    name = fields.Char(string="Title", required="True")
    code = fields.Char(string="Code", required="True")

    line_ids = fields.One2many('exam.questions', 'subject_id')

class Category(models.Model):
    _name = 'question.category'
    _description = 'Category'
    _order = 'id ASC'

    name = fields.Char(string="Title", required="True")
    code = fields.Char(string="Code", required="True")

    line_ids = fields.One2many('exam.questions', 'category_id')


class Questions(models.Model):
    _name = 'exam.questions'
    _description = 'Questions.'

    name = fields.Char(string='Title', required="True")
    meaning = fields.Text(string='Meaning')
    translation = fields.Text(string='Translation')
    sentance = fields.Text(string='Sentance')
    date = fields.Datetime(default=datetime.now())

    subject_id = fields.Many2one('exam.subject', string='Subject', required='True')
    category_id = fields.Many2one('question.category', string='Category')
