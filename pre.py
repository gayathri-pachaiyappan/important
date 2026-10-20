#==================================================================================#
# Derived features for project "volumes" (line dydapi)
# Input : base PCS features from pcs_features.py  -> dydapi_feat_volumes_pcs_float
# Output: written by derived_features.py           -> dydapi_feat_volumes_derived_float
#
# Base features available per batch_id (all float, epoch seconds / seconds):
#   tabletting_batch_start_time, tabletting_batch_end_time, tabletting_batch_duration
#
# Features starting with "__tmp" are only used for intermediate steps and are NOT written.
#==================================================================================#

[[table_defs]]
table = "dydapi_feat_volumes_pcs_float"
columns = ["*"]
feature_column = "feature_name"
pivot_value_column = "value"
merge_column = ["batch_id"]

#----------------------------------------------------------------------------------
# Local time (Olst: Europe/Amsterdam, handles summer/winter time per batch)
#----------------------------------------------------------------------------------
[[derived_feature_definitions]]
feature_name_new = "__tmp_start_time_local_offset"
feature_source = ["tabletting_batch_start_time", "__const_s_Europe/Amsterdam"]
calculation = "utcoffset"

[[derived_feature_definitions]]
feature_name_new = "tabletting_batch_start_time_local"
feature_source = ["tabletting_batch_start_time", "__tmp_start_time_local_offset"]
calculation = "sum"

[[derived_feature_definitions]]
feature_name_new = "__tmp_end_time_local_offset"
feature_source = ["tabletting_batch_end_time", "__const_s_Europe/Amsterdam"]
calculation = "utcoffset"

[[derived_feature_definitions]]
feature_name_new = "tabletting_batch_end_time_local"
feature_source = ["tabletting_batch_end_time", "__tmp_end_time_local_offset"]
calculation = "sum"

#----------------------------------------------------------------------------------
# Production day (local midnight as epoch), handy to group volumes per day
#   day = start_local - (start_local modulo 86400)
#----------------------------------------------------------------------------------
[[derived_feature_definitions]]
feature_name_new = "__tmp_start_seconds_into_day"
feature_source = ["tabletting_batch_start_time_local", "__const_f_86400"]
calculation = "modulo"

[[derived_feature_definitions]]
feature_name_new = "tabletting_batch_start_day_local"
feature_source = ["tabletting_batch_start_time_local", "__tmp_start_seconds_into_day"]
calculation = "subtract"

#----------------------------------------------------------------------------------
# Duration in hours (base feature is in seconds)
#----------------------------------------------------------------------------------
[[derived_feature_definitions]]
feature_name_new = "tabletting_batch_duration_hours"
feature_source = ["tabletting_batch_duration", "__const_f_3600"]
calculation = "divide"
