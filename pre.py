# -*- coding: utf-8 -*-
# %% jupyter={"source_hidden": true}
"""
Utilities to preprocess text data in columns like data from spreadsheet, .CSV
(or .xSV for any 'x' Separated Values), fixed width files, etc.


See
"""

# %%
import numpy as np
import pandas as pd

# Load main modules of our team library
# %%
# Copy some variables of our team library
from abt_epd_gpmo_aa import athena_utils, logger, misc_utils, preprocess_utils, s3_utils

# %% [raw]
#
FILE_PATH_COL_NAME = "_file_path"


# %%
def find_preproc_definitions(def_name: str) -> list:
    """Find toml/json definition files and return all filenames found"""

    logger.warning(
        "WARNING: find_preproc_definitions() - legacy -> use "
        + "preprocess_utils.find_preproc_definitions() instead!"
    )
    return preprocess_utils.find_preproc_definitions(def_name)


# %%
def read_preproc_definition(local_file: str) -> dict:
    """Read the definition file and return its contents as dict"""

    logger.warning(
        "WARNING: read_preproc_definition() - legacy -> use "
        + "misc_utils.find_read_single_file_definition() instead!"
    )
    return misc_utils.find_read_single_file_definition(local_file)


# %% [raw]
#


# %%
def get_data_paths(file_def: dict, new: bool) -> list:
    """Find S3 paths of original data files

    Arguments:
    - file_def : dict containing keys "datasource_name", "filename" with
        "filename" a 'full matching' regular expression (backwards compatible
        with just the full name normal string that it used to be)
    - new : boolean whether to pich data from the 'new' or from the 'processed' folder
    """

    logger.warning(
        "WARNING: get_data_paths() - legacy -> use "
        + "preprocess_utils.get_data_paths() instead!"
    )
    return preprocess_utils.get_data_paths(file_def, new)


# %% [raw]
#


# %%
def read_one_csv_file(path: str, file_def, columns_def: dict) -> pd.DataFrame:
    "Read CSV file, name all (selected) columns and regard every column as type str"

    # use default values, unless they are specified in the CSV file definition
    sep = file_def["sep"] if "sep" in file_def else None
    header = file_def["header"] if "header" in file_def else None
    skipinitialspace = (
        file_def["skipinitialspace"] if "skipinitialspace" in file_def else False
    )
    skiprows = file_def["skiprows"] if "skiprows" in file_def else None
    skipfooter = file_def["skipfooter"] if "skipfooter" in file_def else 0
    nrows = file_def["nrows"] if "nrows" in file_def else None
    skip_blank_lines = (
        file_def["skip_blank_lines"] if "skip_blank_lines" in file_def else True
    )
    compression = file_def["compression"] if "compression" in file_def else None
    lineterminator = (
        file_def["lineterminator"] if "lineterminator" in file_def else None
    )
    quotechar = file_def["quotechar"] if "quotechar" in file_def else '"'
    quoting = file_def["quoting"] if "quoting" in file_def else 0
    doublequote = file_def["doublequote"] if "doublequote" in file_def else True
    escapechar = file_def["escapechar"] if "escapechar" in file_def else None
    comment = file_def["comment"] if "comment" in file_def else None
    encoding = file_def["encoding"] if "encoding" in file_def else None
    # The following lines can be enabled when pandas 1.3.0 or higher is used
    # encoding_errors = (
    #     file_def["encoding_errors"] if "encoding_errors" in file_def else "strict"
    # )
    # on_bad_lines = file_def["on_bad_lines"] if "on_bad_lines" in file_def else "error"

    # Collect which columns to use and the column names
    col_ids = [col_def["id"] for col_def in columns_def]
    if (
        header == None
        and all(type(cid) == str for cid in col_ids)
        and all(cid.isdigit() for cid in col_ids)
    ):
        col_ids = [int(cid) for cid in col_ids]
    col_names = [col_def["name"] for col_def in columns_def]

    df = pd.read_csv(
        "s3://" + misc_utils.config["BUCKET_NAME"] + "/" + path,
        sep=sep,
        header=header,
        skipinitialspace=skipinitialspace,
        skiprows=skiprows,
        skipfooter=skipfooter,
        nrows=nrows,
        skip_blank_lines=skip_blank_lines,
        compression=compression,
        lineterminator=lineterminator,
        quotechar=quotechar,
        quoting=quoting,
        doublequote=doublequote,
        escapechar=escapechar,
        comment=comment,
        encoding=encoding,
        # encoding_errors=encoding_errors, # Only available from pandas version 1.3.0
        # on_bad_lines=on_bad_lines, # Only available from pandas version 1.3.0
        names=col_names,
        usecols=col_ids,
        dtype=str,
        keep_default_na=False,
    )

    return df


# %%
def read_s3_file(path: str, file_def: dict) -> list:
    """Reads a text file from S3, applies character encoding and line breaks and returns list of string lines"""

    file_data = s3_utils.get_file_data(path)  # get bytes

    encoding = file_def["encoding"] if "encoding" in file_def else "utf-8"
    encoding_errors = (
        file_def["encoding_errors"] if "encoding_errors" in file_def else "strict"
    )
    newline = file_def["newline"] if "newline" in file_def else "\n"

    return file_data.decode(encoding=encoding, errors=encoding_errors).split(newline)


# %%
def read_one_text_file(path: str, file_def, columns_def: dict) -> pd.DataFrame:
    "Read text file, name all (selected) columns and regard every column as type str"

    data_lines = read_s3_file(path, file_def)

    # use default values, unless they are specified in the CSV file definition
    line_start = file_def["line_start"] if "line_start" in file_def else r"^"
    line_end = file_def["line_end"] if "line_end" in file_def else r"$"

    line_regex = (
        line_start + "".join([col_def["data"] for col_def in columns_def]) + line_end
    )
    # logger.info(f"DEBUG: line_regex: {line_regex}")
    col_names = [col_def["name"] for col_def in columns_def]

    logger.info(f"Extracting data from {len(data_lines)} lines...")
    df = (
        pd.Series(data_lines)
        .str.extractall(line_regex)
        .reset_index(drop=True)
        .astype("string")
    )
    df.columns = col_names
    logger.info(f"DataFrame extracted from text input has shape: {df.shape}")
    return df


# %%
def read_one_excel_sheet(path: str, file_def, sheet_def: dict) -> pd.DataFrame:
    """Read one sheet (defined by sheet_def) from spreadsheet file (defined by file_def)"""

    col_ids = [col_def["id"] for col_def in sheet_def["columns_data"]]
    col_ids = ",".join(col_ids)
    col_names = [col_def["name"] for col_def in sheet_def["columns_data"]]

    # Get defaults or specified values for optional settings
    header = sheet_def["header"] if "header" in sheet_def else None
    skiprows = sheet_def["skiprows"] if "skiprows" in sheet_def else None
    nrows = sheet_def["nrows"] if "nrows" in sheet_def else None
    skipfooter = sheet_def["skipfooter"] if "skipfooter" in sheet_def else 0

    logger.debug(f"\n-columns: {col_ids}\n-names: {col_names}")

    df = pd.read_excel(
        f"""s3://{misc_utils.config["BUCKET_NAME"]}/{path}""",  # File is read straight from the bucket
        sheet_name=sheet_def["sheet_name"],
        header=header,
        names=col_names,
        usecols=col_ids,
        dtype=str,
        skiprows=skiprows,
        nrows=nrows,
        skipfooter=skipfooter,
    )

    return df


# %% [raw]
#


# %%
def convert_string_to_string(v: pd.Series) -> pd.Series:
    """Returns same, for convenience of having a conversion function"""

    return v.astype("string")


# %%
def convert_string_to_float(v: pd.Series, err_mode: str = "coerce") -> pd.Series:
    """Convert valid values to floats>

    Remarks
    - Handling of invalid values in 'v' depends on 'err_mode'
    - err_mode 'coerce' results in 'NaN' values to be returned for invalid strings
    - Use err_mode 'raise' to raise an exception on invalid values in 'v'
    """

    values = pd.to_numeric(v, errors=err_mode).astype("float64", errors="raise")
    return values


# %%
def convert_string_to_int(v: pd.Series) -> pd.Series:
    """Convert valid values to int, sets invalid values to <largest negative>

    Remarks
    - valid numbers ending in a '.' will be converted with the dot stripped off
    - invalid values are replaced by the largest negative value for np.int64 (our 'NaN')
    """

    # Prepare value series with our integer 'NaN' indicator (largest negative value)
    values = pd.Series(np.iinfo(np.int64).min, index=v.index)
    # Find all valid integer values in v
    val_ints = v.str.match(r"^[-+]?[0-9]+\.?$", na=False)
    # Convert all valid integer values found
    values[val_ints] = (
        v.loc[val_ints].str.replace(r"\.$", "", regex=True).astype(np.int64)
    )
    return values


# %%
def convert_string_to_epoch(
    v: pd.Series,
    format_str: str,
    time_zone: str,
    err_mode="coerce",
    ambiguous: str = "infer",
) -> pd.Series:
    """Convert valid values to Unix/POSIX epoch, the number of seconds since 1-1-1970) 00:00:00 UTC

    Remarks
    - epoch ignores leap seconds, so everyday starts at an exact multiple of 86400 (=24*60*60)
    - epoch is in floating point format to allow for fractions of a second
    - invalid values are replaced by the floating point representation for NaN

    - Handling of invalid values in 'v' depends on 'err_mode'
    - err_mode 'coerce' results in 'NaN' values to be returned for invalid strings
    - Use err_mode 'raise' to raise an exception on invalid values in 'v'

    - In case format_str does NOT contain time zone information (%Z or %z), then
      time_zone should indicate the time zone all data is in
    - In case format_str CONTAINS time zone information (%Z or %z), then the
      parameter 'time_zone' MUST be set to "UTC"

    - The 'ambiguous' parameter handles ambiguous times during DST transitions:
      - 'infer': Infers DST transition hours based on order (default).
      - 'NaT': Returns NaT for ambiguous times.
      - 'raise': Raises AmbiguousTimeError for ambiguous times.

    See also:
        import zoneinfo
        zoneinfo.available_timezones()
    """

    # Do basic conversion to datetime type
    # If format_str contains time zone info, convert to UTC at this stage to facilitate
    # multiple time zones (like +01:00 AND +02:00 during DST)
    values = pd.to_datetime(
        v, format=format_str, errors=err_mode, utc=True
    ).dt.tz_localize(None)
    # Process time zone (in case format_str did not contain time zone info)
    # Don't worry about NaT, as they just result in NaN in the end
    # Note NaT can occur for non-exiting times, for example during the jump at DST switch
    values = (
        values.dt.tz_localize(time_zone, ambiguous=ambiguous, nonexistent="NaT")
        .dt.tz_convert("UTC")
        .dt.tz_localize(None)
    )

    # This converts to epoch in float
    values = (values - pd.Timestamp("1970-01-01")) / pd.Timedelta("1s")
    return values


# %% [raw]
#


# %%
def convert_to_string(df: pd.DataFrame, columns_def: dict) -> pd.DataFrame:

    col_definitions = [c_d for c_d in columns_def if c_d["type"] == "s"]
    df_ret = pd.DataFrame()
    for c_d in col_definitions:
        n = c_d["name"]
        # With duplicated names in the definition this will be a DataFrame instead of Series.
        if type(df[n]) != pd.core.series.Series:
            logger.info(
                f"DEBUG: name: {n}\ntype df[n]: {type(df[n])}\ncolumns: {df.columns}"
            )
            logger.info(f"DEBUG: df.iloc[:1,:][{n}]:\n{df.iloc[:1,:][n]}")
        df_ret[n] = df[n].str.strip().copy()
        if "prereplace" in c_d:
            for r in c_d["prereplace"]:
                df_ret[n] = df_ret[n].str.replace(r[0], r[1], regex=True)
    return df_ret


# %%
def convert_to_float(df: pd.DataFrame, columns_def: dict) -> pd.DataFrame:

    col_definitions = [c_d for c_d in columns_def if c_d["type"] == "f"]
    df_ret = pd.DataFrame()
    for c_d in col_definitions:
        n = c_d["name"]
        # With duplicated names in the definition this will be a DataFrame instead of Series.
        if type(df[n]) != pd.core.series.Series:
            logger.info(
                f"DEBUG: name: {n}\ntype df[n]: {type(df[n])}\ncolumns: {df.columns}"
            )
            logger.info(f"DEBUG: df.iloc[:1,:][{n}]:\n{df.iloc[:1,:][n]}")
        df_ret[n] = df[n].str.strip().copy()
        if "prereplace" in c_d:
            for r in c_d["prereplace"]:
                df_ret[n] = df_ret[n].str.replace(r[0], r[1], regex=True)
        # Keep the option to specify 'raise' which might help creating the column definition
        err_mode = c_d["errors"] if "errors" in c_d else "coerce"

        try:
            df_ret[n] = convert_string_to_float(df_ret[n], err_mode)
        except Exception as err:
            logger.error(f"ERROR converting column {n}")
            logger.error(err)
            raise err
    return df_ret


# %%
def convert_to_int(df: pd.DataFrame, columns_def: dict) -> pd.DataFrame:

    col_definitions = [c_d for c_d in columns_def if c_d["type"] == "i"]
    df_ret = pd.DataFrame()
    for c_d in col_definitions:
        n = c_d["name"]
        # With duplicated names in the definition this will be a DataFrame instead of Series.
        if type(df[n]) != pd.core.series.Series:
            logger.info(
                f"DEBUG: name: {n}\ntype df[n]: {type(df[n])}\ncolumns: {df.columns}"
            )
            logger.info(f"DEBUG: df.iloc[:1,:][{n}]:\n{df.iloc[:1,:][n]}")
        df_ret[n] = df[n].str.strip().copy()
        if "prereplace" in c_d:
            for r in c_d["prereplace"]:
                df_ret[n] = df_ret[n].str.replace(r[0], r[1], regex=True)
        try:
            df_ret[n] = convert_string_to_int(df_ret[n])
        except Exception as err:
            logger.error(f"ERROR converting column {n} to integer")
            logger.error(err)
            raise err
    return df_ret


# %%
def convert_to_datetime(df: pd.DataFrame, columns_def: dict) -> pd.DataFrame:

    col_definitions = [c_d for c_d in columns_def if c_d["type"] == "d"]
    df_ret = pd.DataFrame()
    for c_d in col_definitions:
        n = c_d["name"]
        # With duplicated names in the definition this will be a DataFrame instead of Series.
        if type(df[n]) != pd.core.series.Series:
            logger.info(
                f"DEBUG: name: {n}\ntype df[n]: {type(df[n])}\ncolumns: {df.columns}"
            )
            logger.info(f"DEBUG: df.iloc[:1,:][{n}]:\n{df.iloc[:1,:][n]}")
        df_ret[n] = df[n].str.strip().copy()
        if "prereplace" in c_d:
            for r in c_d["prereplace"]:
                df_ret[n] = df_ret[n].str.replace(r[0], r[1], regex=True)
        # Keep the option to specify 'raise' which might help creating the column definition
        err_mode = c_d.get("errors", "coerce")
        ambiguous = c_d.get("ambiguous", "infer")
        try:
            df_ret[n] = convert_string_to_epoch(
                df_ret[n],
                format_str=c_d["format"],
                time_zone=c_d["tz"],
                err_mode=err_mode,
                ambiguous=ambiguous,
            )
        except Exception as err:
            logger.error(f"ERROR converting column {n}")
            logger.error(err)
            raise err
    return df_ret


# %%
def convert_data(df: pd.DataFrame, columns_def: dict) -> pd.DataFrame:

    return pd.concat(
        (
            convert_to_string(df, columns_def),
            convert_to_float(df, columns_def),
            convert_to_int(df, columns_def),
            convert_to_datetime(df, columns_def),
        ),
        axis=1,
        join="outer",
        ignore_index=False,
    )


# %% [raw]
#


# %%
def clean_data(df: pd.DataFrame, columns_def: dict) -> pd.DataFrame:

    df_ret = df.dropna(
        axis=0,
        how="any",
        subset=[k["name"] for k in columns_def if "no_na" in k and k["no_na"] == True],
    ).copy()
    drop_na_int_columns = [
        k["name"]
        for k in columns_def
        if "no_na" in k and k["no_na"] == True and k["type"] == "i"
    ]
    if len(drop_na_int_columns):
        df_ret = df_ret.drop(
            index=df_ret[
                (df_ret[drop_na_int_columns] == np.iinfo(np.int64).min).any(axis=1)
            ].index,
        ).copy()
    return df_ret


def add_file_path_col(
    df: pd.DataFrame, file_def: dict, table_def: dict
) -> pd.DataFrame:
    """
    Add a _file_path column when table_def.get("add_file_path") is True.

    Parameters:
    - df: DataFrame to update.
    - file_def: dict containing "file_path".
    - table_def: dict; if add_file_path is truthy the column is added.

    Returns the (possibly modified) DataFrame. Logs a warning if the column is overwritten.
    """
    if table_def.get("add_file_path", False):
        if FILE_PATH_COL_NAME in df.columns:
            logger.warning(
                f"WARNING: add_file_path() - column '{FILE_PATH_COL_NAME}' already exists, overwriting it!"
            )
        df[FILE_PATH_COL_NAME] = file_def["file_path"]
    return df


# %% [raw]
#


# %%
def read_existing_data_from_database(full_table_name: str) -> pd.DataFrame:
    """Check if table exists and return all data in a DataFrame if so."""

    if full_table_name in athena_utils.get_tables():
        return athena_utils.get_all_table_data(full_table_name)
    else:
        return pd.DataFrame()


# %%
def merge_with_history(
    df_new: pd.DataFrame, table_name: str, table_def: dict
) -> pd.DataFrame:
    """uses "merge" and "merge_column" from table_def"""

    full_table_name = f'{misc_utils.config["PREPROCESSED_TABLE_PREFIX"]}{table_name}'
    logger.info(f"Merging new data with existing data (if any) in {full_table_name}")
    df_old = read_existing_data_from_database(full_table_name)
    if table_def.get("file_path_in_merge_columns", False):
        if FILE_PATH_COL_NAME not in table_def["merge_columns"]:
            table_def["merge_columns"] += [FILE_PATH_COL_NAME]
    if df_old.shape[0] == 0:
        return df_new
    if table_def["merge"] == "keep_new":
        old_len = len(df_old)
        df_old = df_old.merge(
            df_new[table_def["merge_columns"]],
            how="left",
            on=table_def["merge_columns"],
            indicator="_OLD_ONY_",
        )
        df_old = df_old[df_old["_OLD_ONY_"] == "left_only"].drop(columns=["_OLD_ONY_"])
        logger.info(f"Replacing {old_len - len(df_old)} data points.")
        return pd.concat(
            (df_old, df_new),
            axis=0,
            join="outer",
        ).reset_index(drop=True)
    else:
        # table_def["merge"] == "keep_old"
        new_len = len(df_new)
        df_new = df_new.merge(
            df_old[table_def["merge_columns"]],
            how="left",
            on=table_def["merge_columns"],
            indicator="_NEW_ONY_",
        )
        df_new = df_new[df_new["_NEW_ONY_"] == "left_only"].drop(columns=["_NEW_ONY_"])
        logger.info(f"Replacing {new_len - len(df_new)} data points.")
        return pd.concat(
            (df_old, df_new),
            axis=0,
            join="outer",
        ).reset_index(drop=True)


# %% [raw]
#


# %%
def write_data(df: pd.DataFrame, table_name: str, s3_folder: str) -> None:
    """
    Write one table, overwriting existing (assumes full table data to be in df)
    misc_utils.config["PREPROCESSED_TABLE_PREFIX"] is prepended to table_name
    misc_utils.config["PREPROCESSED_S3_PATH"] is prepended to s3_folder
    """

    full_table_name = f'{misc_utils.config["PREPROCESSED_TABLE_PREFIX"]}{table_name}'
    full_s3_folder = f'{misc_utils.config["PREPROCESSED_S3_PATH"]}{s3_folder}/'

    if not df.empty:
        logger.info(f"Writing {table_name} ...")
        athena_utils.overwrite_table(
            df,
            table=full_table_name,
            s3_folder=full_s3_folder,
        )
        logger.info(
            f"Written {len(df)} rows and {len(df.columns)} columns to {table_name}."
        )
    else:
        logger.warning(f"write_data(): No data for {table_name}.")


# %% [raw]
#


# %%
def default_processing(
    df: pd.DataFrame, file_def, columns_def, table_def: dict
) -> None:

    df = convert_data(df, columns_def)
    df_clean = clean_data(df, columns_def)
    df_clean = add_file_path_col(df_clean, file_def, table_def)

    table_name = file_def["datasource_name"] + "_" + table_def["table_name"]
    df_clean = merge_with_history(
        df_clean,
        table_name,
        table_def,
    )

    # Function write_data() takes care of everything to be added in front of s3_folder
    s3_folder = file_def["datasource_name"] + "/" + table_def["s3_folder"]
    write_data(df_clean, table_name, s3_folder)


# %% [raw]
#
