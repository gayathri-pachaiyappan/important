SQL_statement: 
            SELECT
                
             B."tag" AS "tag",
             B."value" AS "value",
             N."value" AS "next_value",
             B."epoch" AS "start_time",
             N."epoch" AS "next_time"
            
            FROM "abt_aa_weesp_dydro_20261001_nonprod"."dydro_prep_pcs_undefined" AS B
            INNER JOIN "abt_aa_weesp_dydro_20261001_nonprod"."dydro_prep_pcs_undefined" AS N
                ON N.prev_row_id = B.row_id
            
            WHERE B."tag" IN (-8801123487727717193,-3249277712547132446)
                AND B."row_id" <> B."prev_row_id"
                AND N."row_id" <> N."prev_row_id"
                AND N."epoch" > B."epoch"
                AND B."epoch" < 1643978294.59
                AND N."epoch" > 1639658294.59
                AND B."partition_id" >= 18975.9
                AND N."partition_id" >= 18976.9
            
           
2026-10-20 11:45:52,736 ERROR    [               athena_utils.py:661] ERROR: SQL Query FAILED: TYPE_MISMATCH:line 14:21: IN value and list items must be the same type or coercible to a common type. Cannot find common type between varchar and bigint, all types (without duplicates): [varchar, bigint]. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/6919b4b9-7373-44d5-8ca9-2d741a164007' before retrying. Athena will not delete data in your account.
Traceback (most recent call last):
  File "/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/pcs_features.py", line 185, in <module>
    main()  # Use a separate main function so it can be tested.
  File "/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/pcs_features.py", line 148, in main
    tag_utils.clean_fill_cache(tags=tags_in_use, time_range=cache_time_range)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/abt_epd_gpmo_aa/tag_utils.py", line 483, in clean_fill_cache
    add_to_cache(tags, time_range)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/abt_epd_gpmo_aa/tag_utils.py", line 390, in add_to_cache
    df_data = athena_utils.get_pcs_table_free_query(
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/abt_epd_gpmo_aa/athena_utils.py", line650, in get_pcs_table_free_query
    return wr.athena.read_sql_query(
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/_config.py", line 496, in wrapper
    return function(**args)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_read.py", line 960, in read_sql_query
    return _resolve_query_without_cache(
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_read.py", line 434, in _resolve_query_without_cache
    return _resolve_query_without_cache_ctas(
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_read.py", line 273, in _resolve_query_without_cache_ctas
    ctas_query_info: Dict[str, Union[str, _QueryMetadata]] = create_ctas_table(
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/_config.py", line 496, in wrapper
    return function(**args)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_utils.py", line 856, in create_ctas_table
    raise ex
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_utils.py", line 835, in create_ctas_table
    response["ctas_query_metadata"] = _get_query_metadata(
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_utils.py", line 200, in _get_query_metadata
    _query_execution_payload = wait_query(query_execution_id=query_execution_id, boto3_session=boto3_session)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/awswrangler/athena/_utils.py", line 1124, in wait_query
    raise exceptions.QueryFailed(response["Status"].get("StateChangeReason"))
awswrangler.exceptions.QueryFailed: TYPE_MISMATCH: line 14:21: IN value and list items must be the same type or coercible to a common type. Cannot find common type between varchar and bigint, all types (without duplicates): [varchar, bigint]. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/6919b4b9-7373-44d5-8ca9-2d741a164007' before retrying. Athena will not delete data in your account.
