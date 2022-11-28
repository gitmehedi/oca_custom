# Copyright 2020 Creu Blanca
# Copyright 2017-2019 MuK IT GmbH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    kafka_bootstrap_server = fields.Char(string="Server", help="Bootstrap Server", required=True,
                                         config_parameter="stream_kafka.bootstrap_server")

