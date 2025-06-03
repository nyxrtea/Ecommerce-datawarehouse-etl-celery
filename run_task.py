from tasks import run_queries

result = run_queries.delay()
print(f"Task dikirim. ID Task: {result.id}")
