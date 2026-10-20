"""
Utility script for easy generation of TOML PCS tag types, based on OSI-PI types.
If there's data available from the PCS itself, that should be used preferably.
"""

import os

import tomli_w

# # Dict to be written as TOML file

definition = {}


# + active=""
#
# -

import pandas as pd

# Import and copy some variables of our team library
from abt_epd_gpmo_aa import misc_utils  # provides misc_utils.config, but still empty
from abt_epd_gpmo_aa import logger

# +
# Get and set config, so other modules can use it in their initialisation

# In Glue jobs 'args' get set in main script by "glue_boilerplate_configs.py"
# If that is not the case, get the data from the command line or set the default
if not ("args" in vars() or "args" in globals()):
    args = misc_utils.get_options(default_project="dydro")

logger.info(f"args:\n{args}")
misc_utils.set_global_config(
    project=args["project_name"],
    line=args["line_name"] if "line_name" in args else None,
)
# -
# Now misc_utils.config is set, load other modules of our team library
import abt_epd_gpmo_aa

logger.info(f"Version of abt_epd_gpmo_aa: {abt_epd_gpmo_aa.__version__}")
from abt_epd_gpmo_aa import athena_utils, tag_utils
logger.info(f"OSI-PI database: {misc_utils.config['DATABASES']['osipi']}")
print("pandas version:", pd.__version__)  # Just use pd to satisfy pyflakes
df_db = athena_utils.get_table_free_query(
    table=misc_utils.config["OSIPI_TABLE"],
    select=r'''DISTINCT "tagname" AS "tag_name", "value_type", to_unixtime(MAX("timestamp_utc")) AS "max_epoch"''',
    query=r'''GROUP BY "tagname", "value_type"''',
    db_config_index="osipi",
)

misc_utils.show_df(df_db)

df = df_db.copy()

unique_types = df["value_type"].unique()
print(unique_types)

type_to_remove = unique_types[0]  # Select Int16
df["tag_name"][df["value_type"] == type_to_remove]

df[
    df["tag_name"].isin(df["tag_name"][df["value_type"] == type_to_remove].tolist())
].sort_values(by=["tag_name", "value_type"])

df[
    df["tag_name"].isin(df["tag_name"][df["value_type"] == type_to_remove].tolist())
].sort_values(by=["tag_name", "value_type"])["value_type"].unique()

# + active=""
# df = df[df["value_type"] != type_to_remove]
# -

df["tag_name"][df["value_type"].isna()]

df = df.dropna(axis="index", how="any").reset_index(drop=True).copy()

df = df.sort_values(by=["tag_name"])

df["nice_name"] = df["tag_name"].apply(tag_utils.convert_tag_name)

misc_utils.show_df(df)

df_out = df

df_out["type"] = df_out["value_type"].map(
    {
        "Float64": "F",
        "Float32": "F",
        "String": "S",
        "Int64": "I",
        "Int32": "I",
        "Int16": "I",
    }
)

misc_utils.show_df(df_out)

df_out = df_out.sort_values(by=["nice_name", "max_epoch"], ignore_index=True).copy()

misc_utils.show_df(df_out[df_out.duplicated(subset="nice_name", keep=False)])

df_out = df_out.drop_duplicates(
    subset="nice_name", keep="last", ignore_index=True
).copy()

df_out[["nice_name", "value_type"]][df_out["type"].isna()]

df_out = df_out.dropna(axis="index", how="any").reset_index(drop=True)

df_out[["nice_name", "value_type"]][df_out["type"].isna()]

s = df_out["type"]
s.index = df_out["tag_name"]

definition = s.to_dict()


# # Write dict to TOML file

# Write next to project_config.toml, so it is uploaded to Glue with the project config
out_path = os.path.join(
    os.path.dirname(misc_utils.config["USED_CONFIG_FILE"]), "pcs_tag_types.toml"
)
logger.info(f"Writing {len(definition)} tag types to {out_path}")
with open(out_path, mode="wb") as fp:
    tomli_w.dump(definition, fp)
