
Airflow operator that can send messages to MS Teams

Example code:

    op1 = MSTeamsWebhookOperator(task_id='msteamtest',
        http_conn_id='msteams_webhook_url',
        message = "Hello from Airflow!",
        subtitle = "This is the **subtitle**",
        #proxy = "https://yourproxy.domain:3128/",
        dag=dag)

Which results in 

![example](example.png)        

You will need to prepare the HTTP Hook:

    Conn Type = HTTP  
    Host = https://outlook.office.com/webhook/....full-url...


