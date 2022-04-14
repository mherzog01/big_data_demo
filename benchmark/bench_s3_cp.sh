# 00* - 1,501 - 174 MB
# 0* - 387,261
#
# TODO
# 1.  Combine with bench_s3_ls.sh
# 2.  Optionally delete 'data' dir
# 3.  If img_dirs is set from the calling script, use it instead of getting the list of dirs
# 4.  Give number of dirs found
# 5.  Display time required to run
#aws s3 cp s3://multimedia-commons/data/images data --exclude "*" --include "00*/**/*.jpg" --recursive

echo "`date`:  Getting image directories"
# How to trim:  https://stackoverflow.com/a/39527668/11262633
img_dirs=`aws s3 ls s3://multimedia-commons/data/images/  | xargs -L1 echo | cut -f2 -d" "`

echo "`date`:  Copying..."
for img_dir in $img_dirs
do
    #echo $img_dir
    # https://stackoverflow.com/questions/2172352/in-bash-how-can-i-check-if-a-string-begins-with-some-value
    if [[ ! "$img_dir" =~ 00./ ]]
    then
        continue
    fi
    prefix="s3://multimedia-commons/data/images/${img_dir}"
    #echo "Listing $prefix"
    aws s3 cp $prefix data --recursive
done
echo "`date`:  Process complete"