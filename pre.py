#============================================REFINEMENTS DEFINITION=======================================#

#----- Tabletting process ----#

[[batch_time_refinements]]
refinement_name = "Tabletting_batch"
batch_tag = "CB_sBatchName"
# value looks like "1101287-525893" (7 digits - 6 digits); batch id = the 6-digit number
# "-+" also accepts typos with a double dash ("1101287--525855")
regexp = '^\d{7}-+(\d{6})$'

[[batch_time_refinements.start_refinements]]
tag = "rtp_iproductionstatus"
cmp_op = "=="
cmp_val = 22
start = true
ignore_missing = false

[[batch_time_refinements.end_refinements]]
tag = "rtp_iproductionstatus"
cmp_op = "=="
cmp_val = 22
start = false
ignore_missing = false
