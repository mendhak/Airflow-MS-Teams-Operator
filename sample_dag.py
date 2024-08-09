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
    def get_formatted_date(**kwargs):
        iso8601date = kwargs["execution_date"].strftime("%Y-%m-%dT%H:%M:%SZ")
        # Teams date/time formatting: https://learn.microsoft.com/en-us/adaptive-cards/authoring-cards/text-features#datetime-example 
        formatted_date = (
            f"{{{{DATE({iso8601date}, SHORT)}}}} at {{{{TIME({iso8601date})}}}}"
        )
        print(formatted_date)
        return formatted_date

    formatted_date = get_formatted_date()

    op1 = MSTeamsPowerAutomateWebhookOperator(
        task_id="send_to_teams",
        http_conn_id="msteams_webhook_url",
        card_width_full=True,
        header_bar_show=True,
        header_bar_style="good",
        heading_title="Message from Airflow Local",
        heading_title_size="medium",
        heading_subtitle=formatted_date,
        heading_subtitle_subtle=True,
        heading_show_logo=True,
        body_message="**lorem_ipsum** has successfully run in **localhost**",
        body_message_color_type="warning",
        button_text="View logs",
        button_url="http://localhost:8080",
        button_style="default",
        button_show=True,
    )


sample_dag()
