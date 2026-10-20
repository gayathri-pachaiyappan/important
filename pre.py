import awswrangler as wr
con = wr.redshift.connect(connection="abt-aa-weesp-dydro-20261001-nonprod", dbname="nonprod")
print(wr.redshift.read_sql_query("SELECT current_user, current_database()", con=con))
print(wr.redshift.read_sql_query(
    "SELECT nspname FROM pg_namespace WHERE nspname = 'abt_aa_weesp_dydro_20261001'", con=con))
con.close()
