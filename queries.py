# queries.py
import psycopg2
import logging
import time

logging.basicConfig(filename='queries.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONFIG = {
    'dbname': 'ecomanalyticsdb',
    'user': 'postgres',
    'password': 'rev123',
    'host': 'localhost',
    'port': '5432'
}

def execute_query(query_name: str, query: str) -> list[dict]:
    try:
        logging.info(f"Executing {query_name}")
        start_time = time.time()
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
        duration = time.time() - start_time
        logging.info(f"{query_name} completed in {duration:.2f} seconds, returned {len(result)} rows")
        return result
    except Exception as e:
        logging.error(f"{query_name} failed: {str(e)}")
        raise

def run_query1():
    query = """
    SELECT 
        CONCAT('Q', EXTRACT(QUARTER FROM o.order_approved_at::timestamp)) AS quarter,
        EXTRACT(YEAR FROM o.order_approved_at::timestamp) AS year,
        ROUND(AVG(p.payment_value)::numeric, 2) AS average_revenue
    FROM order_payment_dataset p
    JOIN order_dataset o ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY year, quarter
    ORDER BY year, quarter;
    """
    return execute_query("query1", query)

def run_query2():
    query = """
    SELECT 
        p.product_id,
        p.product_category_name,
        COUNT(*) AS jumlah_transaksi,
        SUM(oi.price) AS total_pendapatan
    FROM order_items_dataset oi
    JOIN product_id p ON oi.product_id = p.product_id
    JOIN order_dataset o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.product_id, p.product_category_name
    ORDER BY jumlah_transaksi DESC
    LIMIT 10;
    """
    return execute_query("query2", query)

def run_query3():
    query = """
    SELECT 
        EXTRACT(YEAR FROM o.order_approved_at::timestamp) AS tahun,
        EXTRACT(MONTH FROM o.order_approved_at::timestamp) AS bulan,
        ROUND(SUM(oi.price)::numeric, 2) AS total_penjualan,
        COUNT(DISTINCT o.order_id) AS jumlah_transaksi
    FROM order_dataset o
    JOIN order_items_dataset oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY tahun, bulan
    ORDER BY tahun, bulan;
    """
    return execute_query("query3", query)

def run_query4():
    query = """
    SELECT 
        p.product_id,
        p.product_category_name,
        SUM(oi.order_item_id) AS total_terjual
    FROM product_id p
    JOIN order_items_dataset oi ON p.product_id = oi.product_id
    JOIN order_dataset o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.product_id, p.product_category_name
    ORDER BY total_terjual DESC;
    """
    return execute_query("query4", query)

def run_query5():
    query = """
    SELECT 
        p.product_id,
        p.product_category_name,
        SUM(oi.order_item_id) AS total_terjual,
        CASE 
            WHEN SUM(oi.order_item_id) > 100 THEN 'Perlu Restok'
            ELSE 'Cukup'
        END AS status_restok
    FROM product_id p
    JOIN order_items_dataset oi ON p.product_id = oi.product_id
    JOIN order_dataset o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.product_id, p.product_category_name
    ORDER BY total_terjual DESC;
    """
    return execute_query("query5", query)
