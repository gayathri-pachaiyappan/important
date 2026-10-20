"""
Step 2 of 2: upload the lookup CSV made by create_lookup_csv.py.

    python init_jobs/write_lookup_csv_to_athena_and_s3_parquet.py

Reads  init_jobs/<LOOKUP_TABLE_PREFIX>pcs_tags.csv  (dydro: dydro_lookup_pcs_tags.csv)
Writes
- Athena table  <LOOKUP_TABLE_PREFIX>pcs_tags  (data in <LOOKUP_S3_PATH>pcs_tags/)
- S3 file       <S3_LOOKUP_PREFIX>pcs_tags.parquet   <- this is what the jobs read

(dydro version of cada's script: finds the CSV next to this script instead of in the
current folder, and defaults to project dydro instead of 'raw' / line 'sitkpi')
"""

import os

import pandas as pd

from abt_epd_gpmo_aa import logger, misc_utils

if not misc_utils.config["CONFIGURED"]:
    if not ("args" in vars() or "args" in globals()):
        args = misc_utils.get_options(default_project="dydro")
    misc_utils.set_global_config(
        project=args["project_name"],
        line=args["line_name"] if "line_name" in args else None,
    )

from abt_epd_gpmo_aa import athena_utils, s3_utils  # noqa: E402

cfg = misc_utils.config
CSV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), f"{cfg['LOOKUP_TABLE_PREFIX']}pcs_tags.csv"
)
ATHENA_TABLE_NAME = f"{cfg['LOOKUP_TABLE_PREFIX']}pcs_tags"
ATHENA_S3_FOLDER = f"{cfg['LOOKUP_S3_PATH']}pcs_tags"
S3_PARQUET_PREFIX = cfg["S3_LOOKUP_PREFIX"]
S3_FILE_NAME = "pcs_tags.parquet"


def main() -> None:
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"{CSV_FILE} not found. Create it first: python init_jobs/create_lookup_csv.py"
        )
    df = pd.read_csv(CSV_FILE, dtype={"tag": str, "type": str})
    df["tag_id"] = df["tag_id"].astype("int64")
    logger.info(f"Read {len(df)} rows from {CSV_FILE}")

    logger.info(f"Writing Athena table {cfg['DATABASES']['default']['DATABASE']}.{ATHENA_TABLE_NAME}...")
    athena_utils.overwrite_table(df=df.copy(), table=ATHENA_TABLE_NAME, s3_folder=ATHENA_S3_FOLDER)

    logger.info(f"Writing s3://{cfg['BUCKET_NAME']}/{S3_PARQUET_PREFIX}{S3_FILE_NAME}...")
    s3_utils.df_to_s3_as_parquet(
        df=df, bucket=cfg["BUCKET_NAME"], prefix=S3_PARQUET_PREFIX, filename=S3_FILE_NAME
    )
    logger.info("Lookup written to Athena and S3.")


if __name__ == "__main__":
    main()
