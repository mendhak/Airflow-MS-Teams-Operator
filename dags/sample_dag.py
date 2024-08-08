import pendulum

from airflow.decorators import dag, task

from ms_teams_webhook_operator import MSTeamsWebhookOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def sample_dag():

    @task()
    def print_something(some_value: float):
        print(f"Total order value is: {some_value:.2f}")
        

    op1 = MSTeamsWebhookOperator(task_id='send_to_teams',
        http_conn_id='msteams_webhook_url',
        message = "Hello from Airflow!",
        subtitle = "This is the **subtitle**",
        button_text = "My button",
        button_url = "https://example.com",
        theme_color = "00FF00",
        #proxy = "https://yourproxy.domain:3128/",
        )

    print_something(123.45) >> op1


sample_dag()
