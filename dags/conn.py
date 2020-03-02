from airflow import DAG
from airflow.models import Connection
from airflow.utils.dates import days_ago
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta
from os import environ
from urllib import parse

airflow_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(seconds=1),
}

CONN_ID_OK='s3_ok'
CONN_ID_FAIL='s3_fail'
CONN_ID_PARSE_FAIL='s3_parse_fail'

def conn(conn_id: str, expect: str):
    c = BaseHook.get_connection(conn_id)
    password = c.password
    assert password == expect, "(actual) {} == {} (expected)".format(password, expect)

with DAG(
    "conn",
    default_args=airflow_args,
    description="connection string bug",
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=1),
) as dag:
    task = lambda conn_id, expect: PythonOperator(
        dag=dag,
        task_id=conn_id,
        python_callable=conn,
        op_args=[conn_id, expect],
    )
    conn_ok_task = task(CONN_ID_OK, environ.get('EXPECT_1'))
    conn_fail_task = task(CONN_ID_FAIL, environ.get('EXPECT_2'))
    conn_parse_fail_task = task(CONN_ID_PARSE_FAIL,  environ.get('EXPECT_3'))
