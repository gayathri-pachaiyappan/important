import time
import boto3

athena = boto3.client("athena", region_name="eu-west-1")
TABLE = "osipi_olst_manuf"
SQL = f'SELECT MAX(partition_date) AS last_partition FROM "abt_ea_stagingdb_nonprod"."{TABLE}"'

# Fill in exactly what the console shows when your query works
CONSOLE_WORKGROUP = "abt-aa-weesp-dydro-20261001"   # top-right in Athena console
CONSOLE_CATALOG = "AwsDataCatalog"                  # "Data source" dropdown, left panel

def run(label, ctx, wg):
    try:
        qid = athena.start_query_execution(QueryString=SQL, QueryExecutionContext=ctx, WorkGroup=wg)["QueryExecutionId"]
        while True:
            st = athena.get_query_execution(QueryExecutionId=qid)["QueryExecution"]["Status"]
            if st["State"] in ("SUCCEEDED", "FAILED", "CANCELLED"):
                break
            time.sleep(1)
        print(f"[{st['State']}] {label}\n   {st.get('StateChangeReason', '')}")
    except Exception as e:
        print(f"[ERROR] {label}\n   {e}")

run("like console (catalog + db separate)", {"Catalog": CONSOLE_CATALOG, "Database": "abt_ea_stagingdb_nonprod"}, CONSOLE_WORKGROUP)
run("like our code (catalog.db as one string)", {"Database": "AwsDataCatalog.abt_ea_stagingdb_nonprod"}, "abt-aa-weesp-dydro-20261001")
run("db only, no catalog", {"Database": "abt_ea_stagingdb_nonprod"}, "abt-aa-weesp-dydro-20261001")
