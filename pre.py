poetry run python /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/glue_jobs/pcs_features.py --project_name volumes --line dydapi
2026-10-20 15:02:40,493 INFO     [               pcs_features.py:22] args:
{'project_name': 'volumes', 'line_name': 'dydapi'}
2026-10-20 15:02:40,493 INFO     [                 misc_utils.py:689] get_base_config - searching for: dydapi/line_constants.toml
2026-10-20 15:02:40,495 INFO     [                 misc_utils.py:696] get_base_config - found path to file line_constants: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/line_constants.toml
2026-10-20 15:02:40,496 INFO     [                 misc_utils.py:796] get_config - found path to file project_config: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/project_config.toml
2026-10-20 15:02:40,498 INFO     [               pcs_features.py:70] Version of abt_epd_gpmo_aa: 1.3.4
2026-10-20 15:02:40,907 INFO     [                credentials.py:1278] Found credentials in shared credentials file: ~/.aws/credentials
2026-10-20 15:02:41,395 INFO     [                  tag_utils.py:90] Initialising tag_utils...
2026-10-20 15:02:41,395 INFO     [                  tag_utils.py:125] Getting list of all PCS tags from database.
2026-10-20 15:02:41,824 INFO     [                  tag_utils.py:127] Scanning 3 tables for tags.
['dydro_prep_pcs_float', 'dydro_prep_pcs_int', 'dydro_prep_pcs_string']
2026-10-20 15:02:58,978 INFO     [                  tag_utils.py:134] Found tag types: ['float', 'int', 'string']
2026-10-20 15:02:58,980 INFO     [                  tag_utils.py:204] Ready init tag_utils.
2026-10-20 15:02:58,981 INFO     [               pcs_features.py:76] Start processing PCS features for new batches.
2026-10-20 15:02:58,981 INFO     [                 misc_utils.py:390] Searching for volumes, found /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/.
2026-10-20 15:02:58,981 INFO     [                 misc_utils.py:417] Found project files  matching pcs_feature_definition_*: ['/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_batch_time_refinements.toml', '/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_feature_groups.toml']
2026-10-20 15:02:58,981 INFO     [                 misc_utils.py:499] Reading definitions from:
/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_batch_time_refinements.toml
2026-10-20 15:02:58,982 INFO     [                 misc_utils.py:499] Reading definitions from:
/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_feature_groups.toml
2026-10-20 15:03:00,422 ERROR    [               athena_utils.py:270] SQL_statement: 
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
    
            
2026-10-20 15:03:00,422 ERROR    [               athena_utils.py:271] ERROR: SQL Query FAILED: TABLE_NOT_FOUND:line 9:3: Table 'awsdatacatalog.abt_aa_weesp_dydro_20261001_nonprod.dydapi_feat_volumes_pcs_float' does not exist. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/9edc55cd-1608-47c4-8253-49413a133105' before retrying. Athena will not delete data in your account.
2026-10-20 15:03:00,422 WARNING  [    pcs_basic_feature_utils.py:148] WARNING: Remove last two partitions FAILED: TABLE_NOT_FOUND: line 9:3: Table 'awsdatacatalog.abt_aa_weesp_dydro_20261001_nonprod.dydapi_feat_volumes_pcs_float' does not exist. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/9edc55cd-1608-47c4-8253-49413a133105' before retrying. Athena will not delete data in your account.
2026-10-20 15:03:00,422 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 15:03:00,651 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 15:03:00,651 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 15:03:09,211 INFO     [                  tag_utils.py:335] Preprocessed PCS data is available from epoch 1639658294.59
2026-10-20 15:03:14,518 INFO     [                  tag_utils.py:330] Preprocessed PCS data is available up to epoch 1656805977.49
2026-10-20 15:03:14,802 INFO     [               pcs_features.py:110] Start processing for the next few days ofdata...
2026-10-20 15:03:14,802 INFO     [    pcs_basic_feature_utils.py:221] Adding new features: ['tabletting_batch_start_time', 'tabletting_batch_end_time', 'tabletting_batch_duration']
2026-10-20 15:03:14,802 INFO     [               pcs_features.py:145] filling cache for time range: (1639658294.59, 1643978294.59) (50.0 days)
2026-10-20 15:03:14,803 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 15:03:15,021 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 15:03:15,021 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 15:03:15,166 INFO     [                  tag_utils.py:379] Adding to cache data type: string
2026-10-20 15:03:25,187 INFO     [                  tag_utils.py:379] Adding to cache data type: int
2026-10-20 15:03:30,819 INFO     [                  tag_utils.py:461] All data loaded in cache.
2026-10-20 15:03:30,819 INFO     [               pcs_features.py:159] calculating features
2026-10-20 15:03:30,820 INFO     [    pcs_basic_feature_utils.py:433] Batch time refinement definition: Tabletting_batch
2026-10-20 15:03:30,848 WARNING  [                  tag_utils.py:598] WARNING: get_all_batch_id_time_ranges - df_batches is empty: (0, 4), Index(['tag', 'batch_id', 'start_time', 'end_time'], dtype='object')
2026-10-20 15:03:30,852 WARNING  [    pcs_basic_feature_utils.py:524] No new PCS features.
2026-10-20 15:03:30,852 INFO     [               pcs_features.py:110] Start processing for the next few days ofdata...
2026-10-20 15:03:30,852 INFO     [    pcs_basic_feature_utils.py:221] Adding new features: ['tabletting_batch_start_time', 'tabletting_batch_end_time', 'tabletting_batch_duration']
2026-10-20 15:03:30,852 INFO     [    pcs_basic_feature_utils.py:338] Limiting cache_to to available PCS data: 1656805977.49.
2026-10-20 15:03:30,852 INFO     [               pcs_features.py:145] filling cache for time range: (1643114294.59, 1656805977.49) (158.46855208333443 days)
2026-10-20 15:03:30,853 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 15:03:31,079 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 15:03:31,079 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 15:03:31,208 INFO     [                  tag_utils.py:379] Adding to cache data type: string
2026-10-20 15:03:39,322 INFO     [                  tag_utils.py:379] Adding to cache data type: int
2026-10-20 15:03:45,156 WARNING  [                  tag_utils.py:420] add_to_cache - add the last 'next value' as normal value for each tag; fake next time, value NA.
2026-10-20 15:03:45,157 INFO     [                  tag_utils.py:425] Doing this for 2. On large cache may takea few seconds per tag.
2026-10-20 15:03:45,159 INFO     [                  tag_utils.py:448] add_to_cache - Adding 0 extra datapoints.
2026-10-20 15:03:45,159 INFO     [                  tag_utils.py:461] All data loaded in cache.
2026-10-20 15:03:45,159 INFO     [               pcs_features.py:159] calculating features
2026-10-20 15:03:45,160 INFO     [    pcs_basic_feature_utils.py:433] Batch time refinement definition: Tabletting_batch
2026-10-20 15:03:45,182 WARNING  [                  tag_utils.py:598] WARNING: get_all_batch_id_time_ranges - df_batches is empty: (0, 4), Index(['tag', 'batch_id', 'start_time', 'end_time'], dtype='object')
2026-10-20 15:03:45,184 WARNING  [    pcs_basic_feature_utils.py:524] No new PCS features.
2026-10-20 15:03:45,184 INFO     [               pcs_features.py:180] PCS features ready!
(cada) pachagx@APLTiHSOfxk5ELd:~/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod$ 
