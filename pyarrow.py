import pyarrow.dataset as ds

def merge_with_history(
    df_new: pd.DataFrame, table_name: str, table_def: dict
) -> pd.DataFrame:
    full_table_name = f'{misc_utils.config["PREPROCESSED_TABLE_PREFIX"]}{table_name}'
    logger.info(f"Merging new data with existing data (if any) in {full_table_name}")

    if table_def.get("file_path_in_merge_columns", False):
        if FILE_PATH_COL_NAME not in table_def["merge_columns"]:
            table_def["merge_columns"] += [FILE_PATH_COL_NAME]
    merge_columns = table_def["merge_columns"]

    old_table_s3_path = "s3://abt-aa-aida2-202101002-nonprod/gpmo/ivmapi/data/prep/mb52/raw/"
    dataset = ds.dataset(old_table_s3_path, format="parquet")

    if dataset.count_rows() == 0:
        return df_new

    if table_def["merge"] == "keep_new":
        new_keys = set(df_new[merge_columns].itertuples(index=False, name=None))
        old_len = 0
        kept_batches = []
        for batch in dataset.to_batches(batch_size=200_000):
            batch_df = batch.to_pandas()
            old_len += len(batch_df)
            batch_keys = batch_df[merge_columns].itertuples(index=False, name=None)
            keep_mask = [k not in new_keys for k in batch_keys]
            kept = batch_df[keep_mask]
            if len(kept) > 0:
                kept_batches.append(kept)
            del batch_df, keep_mask, kept
            gc.collect()

        df_old_kept = (
            pd.concat(kept_batches, axis=0, ignore_index=True)
            if kept_batches
            else pd.DataFrame(columns=df_new.columns)
        )
        del kept_batches
        gc.collect()
        logger.info(f"Replacing {old_len - len(df_old_kept)} data points.")

        result = pd.concat(
            (df_old_kept, df_new), axis=0, join="outer", copy=False
        ).reset_index(drop=True)
        del df_old_kept, df_new
        gc.collect()
        return result

    else:
        old_keys = set()
        for batch in dataset.to_batches(columns=merge_columns, batch_size=200_000):
            batch_df = batch.to_pandas()
            old_keys.update(batch_df.itertuples(index=False, name=None))
            del batch_df
            gc.collect()

        new_len = len(df_new)
        new_key_tuples = df_new[merge_columns].itertuples(index=False, name=None)
        keep_mask = [k not in old_keys for k in new_key_tuples]
        df_new_kept = df_new[keep_mask]
        del keep_mask, old_keys
        gc.collect()
        logger.info(f"Replacing {new_len - len(df_new_kept)} data points.")

        df_old = read_existing_data_from_database(full_table_name)
        result = pd.concat(
            (df_old, df_new_kept), axis=0, join="outer", copy=False
        ).reset_index(drop=True)
        del df_old, df_new_kept
        gc.collect()
        return result