from odoo import models, fields, api, _

from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer


class KafkaTopics(models.Model):
    _name = 'kafka.topics'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Kafka Topics'
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    no_of_partition = fields.Integer(string='No of Partition', required=True, default=3)
    replication_node = fields.Integer(string="Replication Node", required=True, default=3)
    active = fields.Boolean(string='Active', default=False, track_visibility='onchange')
    pending = fields.Boolean(string='Pending', default=True, track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('approve', 'Approved'), ('reject', 'Rejected')], default='draft',
                             string='Status', track_visibility='onchange')

    def create_topics(self):
        connect = self.connect_kafka()
        existing_topic_list = connect['cons'].topics()

        print(existing_topic_list)
        topic_list = []
        for topic in self:
            if topic.name not in existing_topic_list:
                new_topic = NewTopic(name=topic.name,
                                     num_partitions=topic.no_of_partition,
                                     replication_factor=topic.replication_node)
                topic_list.append(new_topic)

        try:
            if topic_list:
                connect['adm'].create_topics(new_topics=topic_list, validate_only=False)
        except Exception as e:
            print(e)

    def update_topics(self):
        connect = self.connect_kafka()
        existing_topic_list = connect['cons'].topics()

        topics = set(existing_topic_list) - {line.name for line in self}
        for topic in topics:
            exist = self.search([('name', '=', topic)])
            if not exist:
                self.create({'name': topic,
                             'active': True,
                             'pending': False,
                             'state': 'approve'})

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
        # address = 'localhost:9091'
        address = self.env['ir.config_parameter'].sudo().get_param('stream_kafka.bootstrap_server')
        consumer = KafkaConsumer(bootstrap_servers=address)
        admin_client = KafkaAdminClient(bootstrap_servers=[address])
        return {
            'cons': consumer,
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
