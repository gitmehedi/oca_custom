from odoo import models, fields, api, _

from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer
import time
from json import dumps, loads


class CollectStreams(models.Model):
    _name = 'collect.streams'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Collect Streams'
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    log_file = fields.Char(string='Log File', required=True, default=3)
    log_ids = fields.One2many('collect.streams.logs', 'line_id')
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Approved'), ('reject', 'Rejected')], default='draft',
                             string='Status', track_visibility='onchange')

    def start_streams(self):
        connect = self.connect_kafka()
        sleep_time_in_seconds = 1

        try:
            with open(self.log_file, 'r', errors='ignore') as f:
                while True:
                    for line in f:
                        if line:
                            journal = {'key': 'move', 'vals': line.strip()}
                            connect['pro'].send('cassandra', value=journal)
                            print(line.strip())
                    time.sleep(sleep_time_in_seconds)
        except IOError as e:
            print('Cannot open the file {}. Error: {}'.format(self.log_file, e))

    def collect_logs(self):
        connect = self.connect_kafka()

        for message in connect['cons']:
            if message.value['key'] == 'move':
                self.log_ids.create({'message': message.value['vals'],
                                     'line_id': self.id})
                self.env.cr.commit()
                continue

    def delete_topic(self):
        if self.state == 'approve':
            connect = self.connect_kafka()
            try:
                delete = connect['adm'].delete_topics(topics=[self.name])
                if delete:
                    self.state = 'reject'
            except Exception as e:
                print(e)

    def connect_kafka(self):
        address = self.env['ir.config_parameter'].sudo().get_param('stream_kafka.bootstrap_server')
        consumer = KafkaConsumer('cassandra',
                                 bootstrap_servers=[address],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 group_id='my-group',
                                 value_deserializer=lambda x: loads(x.decode('utf-8')))
        producer = KafkaProducer(bootstrap_servers=[address], value_serializer=lambda x: dumps(x).encode('utf-8'))
        admin_client = KafkaAdminClient(bootstrap_servers=[address])
        return {
            'cons': consumer,
            'pro': producer,
            'adm': admin_client,
        }

    @api.onchange("name")
    def onchange_strips(self):
        if self.name:
            self.name = self.name.strip()

    def act_draft(self):
        if self.state == 'reject':
            self.write({
                'state': 'draft',
                'pending': True,
                'active': False,
            })

    def act_approve(self):
        if self.state == 'draft':
            self.write({
                'state': 'approve',
                'pending': False,
                'active': True,
            })

    def act_reject(self):
        if self.state == 'draft':
            self.write({
                'state': 'reject',
                'pending': False,
                'active': False,
            })


class CollectStreamsLog(models.Model):
    _name = 'collect.streams.logs'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Collect Streams Log'
    _order = "id desc"

    message = fields.Text(string='Message')
    line_id = fields.Many2one('collect.streams', ondelete='cascade', string='Message')
