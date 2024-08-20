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
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.http.operators.http import HttpOperator
from airflow.utils.decorators import apply_defaults
import logging
import json


class MSTeamsPowerAutomateWebhookOperator(HttpOperator):
    """
    This operator allows you to post messages to MS Teams using the Incoming Webhooks connector.
    Takes both MS Teams webhook token directly and connection that has MS Teams webhook token.
    If both supplied, the webhook token will be appended to the host in the connection.

    :param http_conn_id: connection that has MS Teams webhook URL
    :type http_conn_id: str

    :param card_width_full: Whether to show the card in full width. If false, the card will be the MSTeams default
    :type card_width_full: bool
    :param header_bar_show: Whether to show the header in the card. If false, heading title, subtitle, logo won't be shown. 
    :type header_bar_show: bool
    :param header_bar_style: The style hint for the header bar: `default`, `emphasis`, `good`, `attention`, `warning`, `accent`.
    :type header_bar_style: str
    :param heading_title: The title of the card
    :type heading_title: str
    :param heading_title_size: The size of the heading_title: `default`, `small`, `medium`, `large`, `extraLarge`. 
    :param heading_subtitle: The subtitle of the card, just below the heading_title
    :type heading_subtitle: str
    :param heading_subtitle_subtle: Whether the subtitle should be subtle (toned down to appear less prominent)
    :param heading_show_logo: Whether to show the Airflow logo in the card
    :type heading_show_logo: bool
    :param body_message: The main message of the card
    :type body_message: str
    :param body_message_color_type: The color 'type' of the body message: `default`, `dark`, `light`, `accent`, `good`, `warning`, `attention`. 
    :param body_facts_dict: The dictionary of facts to show in the card
    :type body_facts_dict: dict
    :param button_text: The text of the action button
    :type button_text: str
    :param button_url: The URL for the action button click
    :type button_url: str
    :param button_style: The action style of the button: `default`, `positive`, `destructive`
    :param button_show: Whether to show the action button
    :type button_show: bool
    """

    template_fields = ("heading_title", "heading_subtitle", "body_message")

    @apply_defaults
    def __init__(
        self,
        http_conn_id=None,
        card_width_full=True,
        header_bar_show=True,
        header_bar_style="default",
        heading_title=None,
        heading_title_size="large",
        heading_subtitle=None,
        heading_subtitle_subtle=True,
        heading_show_logo=True,
        body_message="",
        body_message_color_type="default",
        body_facts_dict=None,
        button_text=None,
        button_url="https://example.com",
        button_style="default",
        button_show=True,
        *args,
        **kwargs
    ):

        super(MSTeamsPowerAutomateWebhookOperator, self).__init__(*args, **kwargs)
        self.http_conn_id = http_conn_id

        self.card_width_full = card_width_full

        self.header_bar_show = header_bar_show
        self.header_bar_style = header_bar_style
        self.heading_title = heading_title
        self.heading_title_size = heading_title_size
        self.heading_subtitle = heading_subtitle
        self.heading_subtitle_subtle = heading_subtitle_subtle
        self.heading_show_logo = heading_show_logo

        self.body_message = body_message
        self.body_message_color_type = body_message_color_type
        self.body_facts_dict = body_facts_dict

        self.button_text = button_text
        self.button_url = button_url
        self.button_show = button_show
        self.button_style = button_style

    def build_message(self):
        cardjson = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.0",
                        "body": [
                            {
                                "type": "Container",
                                "isVisible": self.header_bar_show,
                                "style": self.header_bar_style,
                                "bleed": True,
                                "minHeight": "15px",
                                "spacing": "None",
                                "items": [
                                    {
                                        "type": "ColumnSet",
                                        "columns": [
                                            {
                                                "type": "Column",
                                                "width": "auto",
                                                "items": [
                                                    {
                                                        "type": "Image",
                                                        "url": "data:image/png;base64,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",
                                                        "altText": "Airflow logo",
                                                        "size": "small",
                                                        "style": "default",
                                                        "isVisible": self.heading_show_logo,
                                                    }
                                                ],
                                            },
                                            {
                                                "type": "Column",
                                                "width": "stretch",
                                                "items": [
                                                    {
                                                        "type": "TextBlock",
                                                        "text": self.heading_title,
                                                        "weight": "bolder",
                                                        "size": self.heading_title_size,
                                                        "wrap": True,
                                                        "style": "heading",
                                                        "isVisible": self.heading_title is not None
                                                    },
                                                    {
                                                        "type": "TextBlock",
                                                        "spacing": "none",
                                                        "text": self.heading_subtitle,
                                                        "isSubtle": self.heading_subtitle_subtle,
                                                        "wrap": True,
                                                        "isVisible": self.heading_subtitle is not None
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "Container",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": self.body_message,
                                        "wrap": True,
                                        "color": self.body_message_color_type,
                                    },
                                    {
                                        "type": "FactSet",
                                        "isVisible": True,
                                        "facts": [
                                          
                                        ]
                                    }
                                ],
                            },
                        ],
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": self.button_text,
                                "url": self.button_url,
                                "style": self.button_style,
                            }
                        ],
                    },
                }
            ],
        }

        if self.body_facts_dict and len(self.body_facts_dict.items()) > 0:
            logging.info("Adding facts to the card")
            cardjson["attachments"][0]["content"]["body"][1]["items"][1]["facts"] = []
            for key, value in self.body_facts_dict.items():
                cardjson["attachments"][0]["content"]["body"][1]["items"][1]["facts"].append({"title": key, "value": value})
            

        if self.card_width_full:
            cardjson["attachments"][0]["content"]["msteams"] = {"width": "Full"}

        if not self.button_show or not self.button_text:
            del cardjson["attachments"][0]["content"]["actions"][0]


        return json.dumps(cardjson)

    def execute(self, context):
        """
        Call the http hook and just invoke it.
        """

        card_json = self.build_message()
        http = HttpHook(http_conn_id=self.http_conn_id, method="POST")
        http.run(data=card_json, headers={"Content-type": "application/json"})

        logging.info("Webhook request sent to MS Teams")
