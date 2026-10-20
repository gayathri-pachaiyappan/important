poetry run python /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/datasharing.py --project_name data_share --line dydapi
2026-10-20 16:38:08,445 INFO     [                datasharing.py:50] args:
{'project_name': 'data_share', 'line_name': 'dydapi'}
2026-10-20 16:38:08,446 INFO     [                 misc_utils.py:689] get_base_config - searching for: dydapi/line_constants.toml
2026-10-20 16:38:08,453 INFO     [                 misc_utils.py:696] get_base_config - found path to file line_constants: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/line_constants.toml
2026-10-20 16:38:08,460 INFO     [                 misc_utils.py:796] get_config - found path to file project_config: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/data_share/project_config.toml
2026-10-20 16:38:08,464 INFO     [                datasharing.py:62] Version of abt_epd_gpmo_aa: 1.3.4
2026-10-20 16:38:08,956 INFO     [                credentials.py:1278] Found credentials in shared credentials file: ~/.aws/credentials
2026-10-20 16:38:10,711 INFO     [                datasharing.py:114] Going to proces DATA_SHARING item:
{'ACTIVE': True, 'TABLE_SELECTOR': 'equals', 'TABLE_NAME': 'dydapi_master_volumes_vol', 'INCREMENTAL': False, 'MODE': 'overwrite'}
2026-10-20 16:38:11,035 INFO     [          datasharing_utils.py:66] Loading table dydapi_master_volumes_vol into Redshift from s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/data/master/volumes/vol/
2026-10-20 16:38:13,873 INFO     [          datasharing_utils.py:300] create_availability_table dydapi_available_tables_full (['dydapi_master_volumes_vol']).
2026-10-20 16:38:21,890 INFO     [          datasharing_utils.py:309] Not writing empty table dydapi_available_tables_part.
2026-10-20 16:38:21,891 INFO     [                datasharing.py:150] === End write Data Sharing tables to redshift ===
