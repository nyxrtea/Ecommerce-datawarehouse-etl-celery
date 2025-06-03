from queries import run_query1
try:
    result = run_query1()
    print(f"Query1 menghasilkan {len(result)} baris:", result[:5])
except Exception as e:
    print(f"Error: {e}")