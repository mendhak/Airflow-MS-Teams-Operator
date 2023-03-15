# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults
from ms_teams_webhook_hook import MSTeamsWebhookHook
import logging


class MSTeamsWebhookOperator(SimpleHttpOperator):
    """
    This operator allows you to post messages to MS Teams using the Incoming Webhooks connector.
    Takes both MS Teams webhook token directly and connection that has MS Teams webhook token.
    If both supplied, the webhook token will be appended to the host in the connection.

    :param http_conn_id: connection that has MS Teams webhook URL
    :type http_conn_id: str
    :param webhook_token: MS Teams webhook token
    :type webhook_token: str
    :param message: The message you want to send on MS Teams
    :type message: str
    :param subtitle: The subtitle of the message to send
    :type subtitle: str
    :param button_text: The text of the action button
    :type button_text: str
    :param button_url: The URL for the action button click
    :type button_url : str
    :param theme_color: Hex code of the card theme, without the #
    :type message: str
    :param proxy: Proxy to use when making the webhook request
    :type proxy: str
    """

    template_fields = ('message', 'subtitle',)

    @apply_defaults
    def __init__(self,
                 http_conn_id=None,
                 webhook_token=None,
                 message="",
                 subtitle="",
                 button_text="",
                 button_url="",
                 theme_color="00FF00",
                 proxy=None,
                 *args,
                 **kwargs):

        super(MSTeamsWebhookOperator, self).__init__(endpoint=webhook_token, *args, **kwargs)
        self.http_conn_id = http_conn_id
        self.webhook_token = webhook_token
        self.message = message
        self.subtitle = subtitle
        self.button_text = button_text
        self.button_url = button_url
        self.theme_color = theme_color
        self.proxy = proxy
        self.hook = None

    def execute(self, context):
        """
        Call the SparkSqlHook to run the provided sql query
        """
        self.hook = MSTeamsWebhookHook(
            self.http_conn_id,
            self.webhook_token,
            self.message,
            self.subtitle,
            self.button_text,
            self.button_url,
            self.theme_color,
            self.proxy
        )
        self.hook.execute()
        logging.info("Webhook request sent to MS Teams")
