"""
Step 1 of 2: build the PCS tag lookup CSV for dydro from the OSI-PI table.

    python init_jobs/create_lookup_csv.py

Writes init_jobs/<LOOKUP_TABLE_PREFIX>pcs_tags.csv  (dydro: dydro_lookup_pcs_tags.csv)
with columns: tag, tag_id, type, preferred_name, created_at

- tag            : a tag name as it can appear (cleaned name and original OSI-PI name)
- tag_id         : 64 bit id, hash of the cleaned name (same for all names of one tag)
- type           : s / i / f  (string / integer / float), newest OSI-PI value_type
- preferred_name : 1 for the cleaned name (what preprocessing joins on), 0 for aliases
- created_at     : epoch when this file was made

This is the dydro version of cada's create_lookup_csv_sitkpi.py "Part 2" (OSI-PI only;
cada's Part 1 uses Neustadt tag dumps that dydro does not have).
Step 2: python init_jobs/write_lookup_csv_to_athena_and_s3_parquet.py
"""

import os
import time

import pandas as pd

from abt_epd_gpmo_aa import logger, misc_utils

if not misc_utils.config["CONFIGURED"]:
    if not ("args" in vars() or "args" in globals()):
        args = misc_utils.get_options(default_project="dydro")
    misc_utils.set_global_config(
        project=args["project_name"],
        line=args["line_name"] if "line_name" in args else None,
    )

from abt_epd_gpmo_aa import athena_utils, preprocess_utils, tag_utils  # noqa: E402

# OSI-PI value_type -> our type code
TYPE_MAPPING = {
    "Float64": "f",
    "Float32": "f",
    "Float16": "f",
    "Int64": "i",
    "Int32": "i",
    "Int16": "i",
    "Digital": "i",
    "String": "s",
}


def signed_hash64(name: str) -> int:
    """hash64 as signed int64 (same values as cada's lookup, e.g. negative ids)"""
    v = preprocess_utils.hash64(name)
    return v - 2**64 if v >= 2**63 else v


def main() -> None:
    table = misc_utils.config["OSIPI_TABLE"]
    logger.info(f"Reading distinct tags and types from OSI-PI table {table}...")
    df = athena_utils.get_table_free_query(
        table=table,
        select='tagname AS tag_name, value_type, MAX(timestamp_utc) AS max_date',
        query="GROUP BY 1, 2",
        db_config_index="osipi",
    )
    logger.info(f"{len(df)} tag/type combinations found")

    # Keep the newest value_type per tag
    df = df.sort_values(by="max_date", ascending=False).drop_duplicates(subset="tag_name")
    df["type"] = df["value_type"].map(TYPE_MAPPING)
    unknown = df[df["type"].isna()]
    if len(unknown):
        logger.warning(
            f"Skipping {len(unknown)} tags with unknown value_type "
            f"{sorted(unknown['value_type'].dropna().unique().tolist())}: "
            f"{unknown['tag_name'].head(20).tolist()}"
        )
    df = df.dropna(subset=["tag_name", "type"]).reset_index(drop=True)

    # Cleaned name = what osipi_to_preprocessed puts in the 'tag' column (join key)
    df["preferred_name_name"] = df["tag_name"].apply(tag_utils.convert_tag_name)

    rows = pd.concat(
        [
            pd.DataFrame(
                {"tag": df["preferred_name_name"], "type": df["type"],
                 "preferred_name_name": df["preferred_name_name"], "preferred_name": 1}
            ),
            pd.DataFrame(
                {"tag": df["tag_name"], "type": df["type"],
                 "preferred_name_name": df["preferred_name_name"], "preferred_name": 0}
            ),
        ],
        ignore_index=True,
    )
    # preferred rows first, then drop duplicate names (e.g. original == cleaned)
    rows = rows.sort_values(by="preferred_name", ascending=False)
    rows = rows.drop_duplicates(subset="tag").reset_index(drop=True)

    # Two different OSI-PI tags that clean to the same name share one id: report it
    clash = df[df.duplicated(subset="preferred_name_name", keep=False)]
    if len(clash):
        logger.warning(
            f"{len(clash)} OSI-PI tags map to the same cleaned name (they share a tag_id):\n"
            f"{clash[['tag_name', 'preferred_name_name']].head(30)}"
        )

    rows["tag_id"] = [signed_hash64(n) for n in rows["preferred_name_name"]]
    rows["created_at"] = int(time.time())
    rows = rows[["tag", "tag_id", "type", "preferred_name", "created_at"]]
    rows = rows.sort_values(
        by=["tag_id", "preferred_name", "tag"], ascending=[True, False, True]
    ).reset_index(drop=True)

    out = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f"{misc_utils.config['LOOKUP_TABLE_PREFIX']}pcs_tags.csv",
    )
    rows.to_csv(out, index=False)
    logger.info(
        f"Wrote {len(rows)} rows ({rows['tag_id'].nunique()} tags, types "
        f"{rows.drop_duplicates('tag_id')['type'].value_counts().to_dict()}) to {out}"
    )


if __name__ == "__main__":
    main()
