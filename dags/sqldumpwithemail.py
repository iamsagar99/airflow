from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'user',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 16),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def check_space(**context):
    ti = context['ti']
    output = ti.xcom_pull(task_ids='check_free_space', key='return_value')
    print(f"Output from check_free_space------------: {output}")
    
    lines = output.split('\n')
    res = lines[0]
    first_equal_pos = res.find('=')
    second_equal_pos = res.find('=', first_equal_pos + 1)

    # Extract the substrings after each equal sign
    is_enough_space = res[first_equal_pos + 1 : res.find(',', first_equal_pos)]
    msg = res[second_equal_pos + 1 :]

    print(f"Is enough space--------: {is_enough_space}")


    # is_enough_space = ti.xcom_pull(task_ids='check_free_space', key='return_value').split('\n')[0]
    if is_enough_space == 'true':
        return 'dump_database'
    else:
        return 'send_space_email'

def email_template(**context):
    ti = context['ti']

    output = ti.xcom_pull(task_ids='check_free_space', key='return_value')
    # print(f"Output from check_free_space------------: {output}")
    
    lines = output.split('\n')
    res = lines[0]
    first_equal_pos = res.find('=')
    second_equal_pos = res.find('=', first_equal_pos + 1)

    is_enough_space = res[first_equal_pos + 1 : res.find(',', first_equal_pos)]
    msg = res[second_equal_pos + 1 :]


    check_space_msg = msg
    dump_msg = ti.xcom_pull(task_ids='dump_database', key='return_value').split('\n')[0]
    delete_msg = ti.xcom_pull(task_ids='delete_old_backups', key='return_value').split('\n')[0] 
    
    html_content = f"""
    <h3>Database Backup Report</h3>
    <p><strong>Space Check:</strong> {check_space_msg}</p>
    <p><strong>Dump Status:</strong> {dump_msg}</p>
    <p><strong>Delete Status:</strong> {delete_msg}</p>
    """
    return html_content

def space_error_template(**context):
    ti = context['ti']

    output = ti.xcom_pull(task_ids='check_free_space', key='return_value')
    # print(f"Output from check_free_space------------: {output}")
    
    lines = output.split('\n')
    res = lines[0]
    first_equal_pos = res.find('=')
    second_equal_pos = res.find('=', first_equal_pos + 1)

    # Extract the substrings after each equal sign
    is_enough_space = res[first_equal_pos + 1 : res.find(',', first_equal_pos)]
    msg = res[second_equal_pos + 1 :]


    check_space_msg = msg
    
    html_content = f"""
    <h3>Error! Insufficient Storage</h3>
    <p><strong>Space Check:</strong> {check_space_msg}</p>
    """
    return html_content



dag = DAG(
    'backupMysql',
    default_args=default_args,
    description='A DAG to backup MySQL database and send email notification',
    schedule_interval='0 0 * * *',  # Cron ,
)

check_free_space = BashOperator(
    task_id='check_free_space',
    bash_command='bash /Users/sagarpoudel/airflow/bash_scripts/check_free_space.sh ',
    dag=dag,
    do_xcom_push=True,
)

branch_check_space = BranchPythonOperator(
    task_id='branch_check_space',
    provide_context=True,
    python_callable=check_space,
    dag=dag,
)

dump_database = BashOperator(
    task_id='dump_database',
    bash_command='bash /Users/sagarpoudel/airflow/bash_scripts/dump_db.sh ',
    dag=dag,
    do_xcom_push=True,
)

delete_old_backups = BashOperator(
    task_id='delete_old_backups',
    bash_command='bash /Users/sagarpoudel/airflow/bash_scripts/delete.sh ',
    dag=dag,
    do_xcom_push=True,
)

send_space_email = EmailOperator(
    task_id='send_space_email',
    to='iamsagar099@gmail.com',
    subject='Database Backup Failed: Not Enough Space',
    html_content=space_error_template,
    dag=dag,
)

send_final_email = EmailOperator(
    task_id='send_final_email',
    to='iamsagar099@gmail.com',
    subject='Database Backup Status',
    html_content="{{ task_instance.xcom_pull(task_ids='email_template', key='return_value') }}",
    dag=dag,
)

email_template = PythonOperator(
    task_id='email_template',
    provide_context=True,
    python_callable=email_template,
    dag=dag,
)

check_free_space >> branch_check_space
branch_check_space >> dump_database >> delete_old_backups >> email_template >> send_final_email
branch_check_space >> send_space_email
