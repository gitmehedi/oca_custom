# -*- coding: utf-8 -*-
{
    'name': 'Stream Process with Kafka',
    'description': """Stream Process with Kafka and Zookeeper in Python""",
    "author": "Md Mehedi Hasan",
    "website": "https://www.swapon.me",
    "version": "15.0",
    "license": "AGPL-3",
    'category': 'Process',
    'depends': [
        'mail',
    ],
    'data': [
        'security/users.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/res_config_settings.xml',
        'views/kafka_topics_views.xml',
    ],
    'installable': True,
}

