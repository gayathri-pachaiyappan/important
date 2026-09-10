import awswrangler as wr
import uuid

def merge_with_history(
    df_new: pd.DataFrame, table_name: str, table_def: dict
) -> pd.DataFrame:
    full_table_name = f'{misc_utils.config["PREPROCESSED_TABLE_PREFIX"]}{table_name}'
    logger.info(f"Merging new data with existing data (if any) in {full_table_name}")

    if table_def.get("file_path_in_merge_columns", False):
        if FILE_PATH_COL_NAME not in table_def["merge_columns"]:
            table_def["merge_columns"] += [FILE_PATH_COL_NAME]
    merge_columns = table_def["merge_columns"]

    # reuse the job's existing bucket + prefix (same ones passed as
    # --bucket_name / --s3_glue_prefix), instead of a separate staging bucket
    bucket_name = misc_utils.config["bucket_name"]
    s3_glue_prefix = misc_utils.config["s3_glue_prefix"]
    database = misc_utils.config["ATHENA_DATABASE"]  # adjust to whatever key read_existing_data_from_database already uses

    tmp_table = f"tmp_merge_keys_{uuid.uuid4().hex[:8]}"
    tmp_s3_path = f"s3://{bucket_name}/{s3_glue_prefix}tmp/{tmp_table}/"

    # 1. write only the merge keys from df_new to a small temp table,
    #    under the existing bucket's tmp/ prefix
    wr.s3.to_parquet(
        df=df_new[merge_columns].drop_duplicates(),
        path=tmp_s3_path,
        dataset=True,
        database=database,
        table=tmp_table,
    )

    try:
        if table_def["merge"] == "keep_new":
            join_cond = " AND ".join(f'o."{c}" = n."{c}"' for c in merge_columns)
            null_check = f'n."{merge_columns[0]}" IS NULL'

            query = f"""
                SELECT o.*
                FROM {full_table_name} o
                LEFT JOIN {tmp_table} n
                  ON {join_cond}
                WHERE {null_check}
            """
            df_old_kept = wr.athena.read_sql_query(sql=query, database=database)
            logger.info(f"Kept {len(df_old_kept)} existing rows not present in new data.")

            result = pd.concat(
                (df_old_kept, df_new), axis=0, join="outer", copy=False
            ).reset_index(drop=True)
            del df_old_kept, df_new
            gc.collect()
            return result

        else:
            # keep_old: keep df_new rows whose keys are NOT already in the old table
            join_cond = " AND ".join(f'o."{c}" = n."{c}"' for c in merge_columns)
            query = f"""
                SELECT n.*
                FROM {tmp_table} n
                LEFT JOIN {full_table_name} o
                  ON {join_cond}
                WHERE o."{merge_columns[0]}" IS NULL
            """
            df_new_unmatched = wr.athena.read_sql_query(sql=query, database=database)
            logger.info(f"Adding {len(df_new_unmatched)} new data points.")

            # semi-join df_new locally against the small unmatched-keys result
            keep_mask = pd.MultiIndex.from_frame(df_new[merge_columns]).isin(
                pd.MultiIndex.from_frame(df_new_unmatched[merge_columns])
            )
            df_new_kept = df_new[keep_mask]
            del keep_mask, df_new_unmatched
            gc.collect()

            df_old = read_existing_data_from_database(full_table_name)
            result = pd.concat(
                (df_old, df_new_kept), axis=0, join="outer", copy=False
            ).reset_index(drop=True)
            del df_old, df_new_kept
            gc.collect()
            return result
    finally:
        # clean up the temp table + its S3 data regardless of outcome
        wr.catalog.delete_table_if_exists(database=database, table=tmp_table)
        wr.s3.delete_objects(tmp_s3_path)