(cada) pachagx@APLTiHSOfxk5ELd:~/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod$ poetry run python /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/pcs_features.py --project_name volumes --line dydapi
2026-10-20 14:41:02,642 INFO     [               pcs_features.py:22] args:
{'project_name': 'volumes', 'line_name': 'dydapi'}
2026-10-20 14:41:02,642 INFO     [                 misc_utils.py:689] get_base_config - searching for: dydapi/line_constants.toml
2026-10-20 14:41:02,643 INFO     [                 misc_utils.py:696] get_base_config - found path to file line_constants: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/line_constants.toml
2026-10-20 14:41:02,645 INFO     [                 misc_utils.py:796] get_config - found path to file project_config: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/project_config.toml
2026-10-20 14:41:02,648 INFO     [               pcs_features.py:70] Version of abt_epd_gpmo_aa: 1.3.4
2026-10-20 14:41:02,975 INFO     [                credentials.py:1278] Found credentials in shared credentials file: ~/.aws/credentials
2026-10-20 14:41:03,428 INFO     [                  tag_utils.py:90] Initialising tag_utils...
2026-10-20 14:41:03,428 INFO     [                  tag_utils.py:125] Getting list of all PCS tags from database.
2026-10-20 14:41:04,860 INFO     [                  tag_utils.py:127] Scanning 0 tables for tags.
[]
2026-10-20 14:41:04,861 INFO     [                  tag_utils.py:134] Found tag types: []
2026-10-20 14:41:04,866 INFO     [                  tag_utils.py:204] Ready init tag_utils.
2026-10-20 14:41:04,867 INFO     [               pcs_features.py:76] Start processing PCS features for new batches.
2026-10-20 14:41:04,868 INFO     [                 misc_utils.py:390] Searching for volumes, found /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/.
2026-10-20 14:41:04,869 INFO     [                 misc_utils.py:417] Found project files  matching pcs_feature_definition_*: ['/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_batch_time_refinements.toml', '/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_feature_groups.toml']
2026-10-20 14:41:04,870 INFO     [                 misc_utils.py:499] Reading definitions from:
/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_batch_time_refinements.toml
2026-10-20 14:41:04,870 INFO     [                 misc_utils.py:499] Reading definitions from:
/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_feature_groups.toml
2026-10-20 14:41:06,430 ERROR    [               athena_utils.py:270] SQL_statement: 
            SELECT
                DISTINCT partition_id, regexp_replace("$path", '/[^/]*$') AS "s3_path" 
            FROM abt_aa_weesp_dydro_20261001_nonprod."dydapi_feat_volumes_pcs_float"
            WHERE 
    partition_id in (
        SELECT DISTINCT partition_id
        FROM "abt_aa_weesp_dydro_20261001_nonprod"."dydapi_feat_volumes_pcs_float"
        ORDER BY partition_id DESC
        LIMIT 2
    )
    
            
2026-10-20 14:41:06,431 ERROR    [               athena_utils.py:271] ERROR: SQL Query FAILED: TABLE_NOT_FOUND: line 9:3: Table 'awsdatacatalog.abt_aa_weesp_dydro_20261001_nonprod.dydapi_feat_volumes_pcs_float' does notexist. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/fa8be4c8-de88-43ef-b51b-4361c337de3f' before retrying. Athena will not delete data in your account.
2026-10-20 14:41:06,431 WARNING  [    pcs_basic_feature_utils.py:148] WARNING: Remove last two partitions FAILED: TABLE_NOT_FOUND: line 9:3: Table 'awsdatacatalog.abt_aa_weesp_dydro_20261001_nonprod.dydapi_feat_volumes_pcs_float' does not exist. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/fa8be4c8-de88-43ef-b51b-4361c337de3f' before retrying. Athena will not delete data in your account.
Traceback (most recent call last):
  File "/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/pcs_features.py", line 185, in <module>
    main()  # Use a separate main function so it can be tested.
  File "/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/pcs_features.py", line 88, in main
    tags_in_use = pcs_basic_feature_utils.get_tags_in_use(feature_definitions)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/abt_epd_gpmo_aa/pcs_basic_feature_utils.py", line 119, in get_tags_in_use
    pcs_tag_list = tag_utils.get_tag_list(include_undefined=False)
  File "/home/pachagx/miniconda3/envs/cada/lib/python3.9/site-packages/abt_epd_gpmo_aa/tag_utils.py", line 297, in get_tag_list
    + f"""{list(all_db_tags.values())[0][0]} {type(list(all_db_tags.values())[0][0])}"""
IndexError: list index out of range
