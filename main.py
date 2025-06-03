from tasks import run_query_task1, run_query_task2, run_query_task3, run_query_task4, run_query_task5
import pandas as pd
import logging
from celery.exceptions import TimeoutError as CeleryTimeoutError

logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting main script")
    print("Menjalankan task Celery...")

    try:
        tasks = [
            (run_query_task1, "task1", "queue1"),
            (run_query_task2, "task2", "queue2"),
            (run_query_task3, "task3", "queue3"),
            (run_query_task4, "task4", "queue4"),
            (run_query_task5, "task5", "queue5"),
        ]

        async_results = []
        for task, task_name, queue in tasks:
            res = task.apply_async(queue=queue)
            async_results.append((res, task_name))
            print(f"Task {task_name} ID: {res.id}")
            logging.info(f"Task {task_name} ID: {res.id} sent to {queue}")

        results = []
        for res, task_name in async_results:
            try:
                result = res.get(timeout=600)
                print(f"Task {task_name} status: {res.status}")
                logging.info(f"Task {task_name} status: {res.status}, Result received")

                if isinstance(result, dict) and result.get('status') == 'success':
                    results.append((task_name, result['data']))
                else:
                    error_msg = result.get('data') if isinstance(result, dict) else str(result)
                    print(f"Task {task_name} gagal: {error_msg}")
                    logging.warning(f"Task {task_name} gagal: {error_msg}")
                    results.append((task_name, None))

            except CeleryTimeoutError:
                logging.error(f"Task {res.id} ({task_name}) timed out")
                print(f"Task {task_name} status: TIMEOUT")
                results.append((task_name, None))
            except Exception as e:
                logging.error(f"Task {res.id} ({task_name}) failed: {str(e)}")
                print(f"Task {task_name} status: FAILED, Error: {str(e)}")
                results.append((task_name, None))

        for task_name, data in results:
            try:
                if data is None:
                    print(f"Tidak ada data valid untuk {task_name}, skip simpan ke file.")
                    continue

                df = pd.DataFrame(data)
                df.to_excel(f'ecom_analytics_{task_name}.xlsx', index=False)
                print(f"Hasil {task_name} disimpan ke 'ecom_analytics_{task_name}.xlsx'")
            except Exception as e:
                logging.error(f"Gagal menyimpan hasil {task_name} ke Excel: {str(e)}")
                print(f"Gagal menyimpan hasil {task_name} ke Excel: {str(e)}")

    except Exception as e:
        logging.error(f"Kesalahan utama: {str(e)}")
        print(f"Kesalahan utama: {str(e)}")

if __name__ == "__main__":
    main()