# celeryconfig.py
from kombu import Queue

broker_url = 'amqp://guest:guest@localhost:5672//'
result_backend = 'rpc://'

task_queues = (
    Queue('queue1', routing_key='queue1'),
    Queue('queue2', routing_key='queue2'),
    Queue('queue3', routing_key='queue3'),
    Queue('queue4', routing_key='queue4'),
    Queue('queue5', routing_key='queue5'),
)

task_routes = {
    'tasks.run_query_task1': {'queue': 'queue1', 'routing_key': 'queue1'},
    'tasks.run_query_task2': {'queue': 'queue2', 'routing_key': 'queue2'},
    'tasks.run_query_task3': {'queue': 'queue3', 'routing_key': 'queue3'},
    'tasks.run_query_task4': {'queue': 'queue4', 'routing_key': 'queue4'},
    'tasks.run_query_task5': {'queue': 'queue5', 'routing_key': 'queue5'},
}

task_time_limit = 600
task_soft_time_limit = 540
task_default_retry_delay = 30
task_max_retries = 3
broker_connection_retry_on_startup = True
worker_prefetch_multiplier = 3