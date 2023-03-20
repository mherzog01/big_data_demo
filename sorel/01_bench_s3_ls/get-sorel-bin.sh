work_dir=`pwd`
log_file="$work_dir/sorel_binaries_timing.log"

echo work_dir=$work_dir
echo log_file=$log_file

cd $work_dir

date > $log_file
aws s3 ls s3://sorel-20m/09-DEC-2020/binaries/ > "$work_dir/sorel_binaries.txt"
date >> $log_file