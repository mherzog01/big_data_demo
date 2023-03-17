$work_dir="`pwd`"
$data_dir="$work_dir/data"
$log_file="$data_dir/cp-sorel.log"

echo "Working directory = $work_dir"
echo "Data directory = $data_dir"
if [ -e $data_dir ]
then
    rm -r $data_dir
fi
mkdir $data_dir
cd $work_dir

date > $log_file
aws s3 cp s3://sorel-20m/09-DEC-2020/binaries $data_dir --recursive
date >> $log_file