$work_dir = "c:/tmp/work1"
$data_dir = "$work_dir/data"
$log_file = "$work_dir/cp-sorel.log"

write-output "Working directory = $work_dir"
write-output "Data directory = $data_dir"
if (test-path $data_dir){remove-item -recurse $data_dir}
mkdir $data_dir
set-location $work_dir

get-date > $log_file
aws s3 cp s3://sorel-20m/09-DEC-2020/binaries $data_dir --recursive
get-date >> $log_file