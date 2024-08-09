import pendulum

from airflow.decorators import dag, task

from ms_teams_powerautomate_webhook_operator import MSTeamsPowerAutomateWebhookOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def sample_dag():

    @task()
    def print_something(some_value: float):
        print(f"This task is complete. Final value, {some_value:.2f}")
        

    op1 = MSTeamsPowerAutomateWebhookOperator(task_id='send_to_teams',
        http_conn_id='msteams_webhook_url',
        heading_message="Airflow local test",
        heading_subtitle="This is a test message",
        body_message="**lorem_ipsum** ran successfully in **localhost**",
        button_text="View logs",
        button_url="http://localhost:8080",
        )

    print_something(123.45) >> op1


sample_dag()
