$work_dir = "c:/tmp/work1"
$log_file = "$work_dir/sorel_binaries_timing.log"

set-location $work_dir

get-date > $log_file
aws s3 ls s3://sorel-20m/09-DEC-2020/binaries/ > "$work_dir/sorel_binaries.txt"
get-date >> $log_file