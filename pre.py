2026-10-20 14:27:52,335 INFO     [               pcs_features.py:22] args:
{'project_name': 'volumes', 'line_name': 'dydapi'}
2026-10-20 14:27:52,335 INFO     [                 misc_utils.py:689] get_base_config - searching for: dydapi/line_constants.toml
2026-10-20 14:27:52,336 INFO     [                 misc_utils.py:696] get_base_config - found path to file line_constants: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/line_constants.toml
2026-10-20 14:27:52,339 INFO     [                 misc_utils.py:796] get_config - found path to file project_config: /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/project_config.toml
2026-10-20 14:27:52,340 INFO     [               pcs_features.py:70] Version of abt_epd_gpmo_aa: 1.3.4
2026-10-20 14:27:52,605 INFO     [                credentials.py:1278] Found credentials in shared credentials file: ~/.aws/credentials
2026-10-20 14:27:52,940 INFO     [                  tag_utils.py:90] Initialising tag_utils...
2026-10-20 14:27:52,940 INFO     [                  tag_utils.py:125] Getting list of all PCS tags from database.
2026-10-20 14:27:53,343 INFO     [                  tag_utils.py:127] Scanning 3 tables for tags.
['dydro_prep_pcs_float', 'dydro_prep_pcs_int', 'dydro_prep_pcs_string']
2026-10-20 14:28:09,271 INFO     [                  tag_utils.py:134] Found tag types: ['float', 'int', 'string']
2026-10-20 14:28:09,273 INFO     [                  tag_utils.py:204] Ready init tag_utils.
2026-10-20 14:28:09,275 INFO     [               pcs_features.py:76] Start processing PCS features for new batches.
2026-10-20 14:28:09,276 INFO     [                 misc_utils.py:390] Searching for volumes, found /home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/.
2026-10-20 14:28:09,276 INFO     [                 misc_utils.py:417] Found project files  matching pcs_feature_definition_*: ['/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_batch_time_refinements.toml', '/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_feature_groups.toml']
2026-10-20 14:28:09,276 INFO     [                 misc_utils.py:499] Reading definitions from:
/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_batch_time_refinements.toml
2026-10-20 14:28:09,277 INFO     [                 misc_utils.py:499] Reading definitions from:
/home/pachagx/SageMaker/pachagx/abt-aa-olst-dydro-20261001-pipelines-nonprod/abt_epd_gpmo_aa_nlwhor/dydapi/volumes/pcs_feature_definition_feature_groups.toml
2026-10-20 14:28:14,189 INFO     [               athena_utils.py:484] From table 'dydro_prep_pcs_float' deleting partitions: [['19176'], ['19177']]
2026-10-20 14:28:14,190 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydro/data/prep/pcs/float/partition_id=19176...
2026-10-20 14:28:18,573 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydro/data/prep/pcs/float/partition_id=19176.
2026-10-20 14:28:18,624 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydro/data/prep/pcs/float/partition_id=19177...
2026-10-20 14:28:18,680 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydro/data/prep/pcs/float/partition_id=19177.
2026-10-20 14:28:19,039 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 14:28:19,094 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 14:28:19,094 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 14:28:23,549 INFO     [                  tag_utils.py:335] Preprocessed PCS data is available fromepoch 1639658294.59
2026-10-20 14:28:27,912 INFO     [                  tag_utils.py:330] Preprocessed PCS data is available up to epoch 1656805977.49
2026-10-20 14:28:33,670 ERROR    [               athena_utils.py:582] SQL_statement: 
            SELECT DISTINCT t1.batch_id AS batch_id,
                t1.feature_name AS feature_name,
                t1.epoch AS epoch
            FROM "abt_aa_weesp_dydro_20261001_nonprod"."dydro_prep_pcs_float" AS t1
            INNER JOIN
                (SELECT feature_name,
                     max(epoch) AS m_epoch
                FROM "abt_aa_weesp_dydro_20261001_nonprod"."dydro_prep_pcs_float"
                GROUP BY  feature_name) AS t2
                ON t2.feature_name = t1.feature_name
                    AND t1.epoch=t2.m_epoch
            
2026-10-20 14:28:33,670 ERROR    [               athena_utils.py:583] ERROR: SQL Query FAILED: COLUMN_NOT_FOUND: line 13:6: Column 'feature_name' cannot be resolved or requester is not authorized to access requested resources. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/f52b0601-3099-4db7-9090-214f9bfd5c06' before retrying. Athena will not delete data in your account.
2026-10-20 14:28:33,670 WARNING  [    pcs_basic_feature_utils.py:165] WARNING: get_last_datapoints FAILED: COLUMN_NOT_FOUND: line 13:6: Column 'feature_name' cannot be resolved or requester is not authorized to access requested resources. You may need to manually clean the data at location 's3://abt-aa-weesp-dydro-20261001-nonprod/athenaresults/tables/f52b0601-3099-4db7-9090-214f9bfd5c06' before retrying. Athena will not delete data inyour account.
2026-10-20 14:28:33,671 INFO     [               pcs_features.py:110] Start processing for the next few days of data...
2026-10-20 14:28:33,672 INFO     [    pcs_basic_feature_utils.py:221] Adding new features: ['tabletting_batch_start_time', 'tabletting_batch_end_time', 'tabletting_batch_duration']
2026-10-20 14:28:33,672 INFO     [               pcs_features.py:145] filling cache for time range: (1639658294.59, 1643978294.59) (50.0 days)
2026-10-20 14:28:33,673 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 14:28:33,953 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 14:28:33,953 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 14:28:34,073 INFO     [                  tag_utils.py:379] Adding to cache data type: string
2026-10-20 14:28:39,280 INFO     [                  tag_utils.py:379] Adding to cache data type: int
2026-10-20 14:28:44,078 INFO     [                  tag_utils.py:461] All data loaded in cache.
2026-10-20 14:28:44,078 INFO     [               pcs_features.py:159] calculating features
2026-10-20 14:28:44,079 INFO     [    pcs_basic_feature_utils.py:433] Batch time refinement definition: Tabletting_batch
2026-10-20 14:28:44,096 WARNING  [                  tag_utils.py:598] WARNING: get_all_batch_id_time_ranges -df_batches is empty: (0, 4), Index(['tag', 'batch_id', 'start_time', 'end_time'], dtype='object')
2026-10-20 14:28:44,098 WARNING  [    pcs_basic_feature_utils.py:524] No new PCS features.
2026-10-20 14:28:44,098 INFO     [               pcs_features.py:110] Start processing for the next few days of data...
2026-10-20 14:28:44,098 INFO     [    pcs_basic_feature_utils.py:221] Adding new features: ['tabletting_batch_start_time', 'tabletting_batch_end_time', 'tabletting_batch_duration']
2026-10-20 14:28:44,098 INFO     [               pcs_features.py:145] filling cache for time range: (1643114294.59, 1651060785.9780505) (91.97327995428884 days)
2026-10-20 14:28:44,099 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 14:28:48,440 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 14:28:48,440 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 14:28:48,568 INFO     [                  tag_utils.py:379] Adding to cache data type: string
2026-10-20 14:28:53,311 INFO     [                  tag_utils.py:379] Adding to cache data type: int
2026-10-20 14:28:58,428 INFO     [                  tag_utils.py:461] All data loaded in cache.
2026-10-20 14:28:58,428 INFO     [               pcs_features.py:159] calculating features
2026-10-20 14:28:58,429 INFO     [    pcs_basic_feature_utils.py:433] Batch time refinement definition: Tabletting_batch
2026-10-20 14:28:58,442 WARNING  [                  tag_utils.py:598] WARNING: get_all_batch_id_time_ranges -df_batches is empty: (0, 4), Index(['tag', 'batch_id', 'start_time', 'end_time'], dtype='object')
2026-10-20 14:28:58,444 WARNING  [    pcs_basic_feature_utils.py:524] No new PCS features.
2026-10-20 14:28:58,444 INFO     [               pcs_features.py:110] Start processing for the next few days of data...
2026-10-20 14:28:58,444 INFO     [    pcs_basic_feature_utils.py:221] Adding new features: ['tabletting_batch_start_time', 'tabletting_batch_end_time', 'tabletting_batch_duration']
2026-10-20 14:28:58,445 INFO     [    pcs_basic_feature_utils.py:338] Limiting cache_to to available PCS data: 1656805977.49.
2026-10-20 14:28:58,445 INFO     [               pcs_features.py:145] filling cache for time range: (1650196785.9780505, 1656805977.49) (76.49527212904559 days)
2026-10-20 14:28:58,445 INFO     [                   s3_utils.py:63] Finding files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet...
2026-10-20 14:28:58,674 INFO     [                   s3_utils.py:70] Found 1 files in s3://abt-aa-weesp-dydro-20261001-nonprod/gpmo/dydapi/files/lookup/pcs_tags.parquet.
2026-10-20 14:28:58,674 INFO     [       preprocess_pcs_utils.py:321] Reading the lookup table on S3...
2026-10-20 14:28:58,798 INFO     [                  tag_utils.py:379] Adding to cache data type: string
2026-10-20 14:29:06,311 INFO     [                  tag_utils.py:379] Adding to cache data type: int
2026-10-20 14:29:10,619 WARNING  [                  tag_utils.py:420] add_to_cache - add the last 'next value' as normal value for each tag; fake next time, value NA.
2026-10-20 14:29:10,620 INFO     [                  tag_utils.py:425] Doing this for 2. On large cache may take a few seconds per tag.
2026-10-20 14:29:10,622 INFO     [                  tag_utils.py:448] add_to_cache - Adding 0 extra datapoints.
2026-10-20 14:29:10,622 INFO     [                  tag_utils.py:461] All data loaded in cache.
2026-10-20 14:29:10,622 INFO     [               pcs_features.py:159] calculating features
2026-10-20 14:29:10,623 INFO     [    pcs_basic_feature_utils.py:433] Batch time refinement definition: Tabletting_batch
2026-10-20 14:29:10,638 WARNING  [                  tag_utils.py:598] WARNING: get_all_batch_id_time_ranges -df_batches is empty: (0, 4), Index(['tag', 'batch_id', 'start_time', 'end_time'], dtype='object')
2026-10-20 14:29:10,639 WARNING  [    pcs_basic_feature_utils.py:524] No new PCS features.
2026-10-20 14:29:10,639 INFO     [               pcs_features.py:180] PCS features ready!
