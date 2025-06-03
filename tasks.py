# tasks.py
from celery_app import app
from queries import run_query1, run_query2, run_query3, run_query4, run_query5
import logging

logging.basicConfig(filename='tasks.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.task
def run_query_task1():
    try:
        logging.info("Running task1")
        data = run_query1()
        return {'status': 'success', 'data': data}
    except Exception as e:
        logging.error(f"task1 failed: {str(e)}")
        return {'status': 'failed', 'data': str(e)}

@app.task
def run_query_task2():
    try:
        logging.info("Running task2")
        data = run_query2()
        return {'status': 'success', 'data': data}
    except Exception as e:
        logging.error(f"task2 failed: {str(e)}")
        return {'status': 'failed', 'data': str(e)}

@app.task
def run_query_task3():
    try:
        logging.info("Running task3")
        data = run_query3()
        return {'status': 'success', 'data': data}
    except Exception as e:
        logging.error(f"task3 failed: {str(e)}")
        return {'status': 'failed', 'data': str(e)}

@app.task
def run_query_task4():
    try:
        logging.info("Running task4")
        data = run_query4()
        return {'status': 'success', 'data': data}
    except Exception as e:
        logging.error(f"task4 failed: {str(e)}")
        return {'status': 'failed', 'data': str(e)}
    
@app.task
def run_query_task5():
    try:
        logging.info("Running task5")
        data = run_query5()
        return {'status': 'success', 'data': data}
    except Exception as e:
        logging.error(f"task5 failed: {str(e)}")
        return {'status': 'failed', 'data': str(e)}