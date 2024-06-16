from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.email import EmailOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': 'iamsagar099@gmail.com',
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

dag = DAG(
    'Greeting_Email', 
    default_args=default_args,
    description='Send email Every Morning',
    schedule_interval='0 6 * * *',  # Cron 
    start_date=datetime(2024, 6, 15),
    catchup=False,
)

send_email = EmailOperator(
    task_id='send_email_task',
    to=['iamsagar099@gmail.com','susmapant@gmail.com'], 
    subject='Greeting from Sagar',
    html_content='<p>Good Morning! Have a wonderful day<br/><em>yours faithfully <br/> Buddhi Sagar Poudel [ARL]</em></p>',
    dag=dag,
)
#dag set 
send_email
