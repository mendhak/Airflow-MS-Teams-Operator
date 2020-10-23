
Airflow operator that can send messages to MS Teams

Example:

    op1 = MSTeamsWebhookOperator(task_id='msteamtest',
        http_conn_id='msteams_webhook_url',
        message = "Hello from Airflow!",
        subtitle = "This is the **subtitle**",
        button_text = "My button",
        button_url = "https://example.com",
        theme_color = "00FF00",
        #proxy = "https://yourproxy.domain:3128/",
        dag=dag)


Results in:

![example](example.png)        


## Usage

For setup and usage instructions see [the writeup here](https://code.mendhak.com/Airflow-MS-Teams-Operator/)


## Contribute

Any feature requests, please fork and submit a PR. 

### Wishlist

Ability to create potentialActions as seen here:

https://docs.microsoft.com/en-us/outlook/actionable-messages/actionable-messages-via-connectors

## License

Apache 2.0 (see code file headers) 