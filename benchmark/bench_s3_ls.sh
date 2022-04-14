echo "`date`:  Getting image directories"
# How to trim:  https://stackoverflow.com/a/39527668/11262633
img_dirs=`aws s3 ls s3://multimedia-commons/data/images/  | xargs -L1 echo | cut -f2 -d" "`

echo "`date`:  Listing..."
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
    aws s3 ls $prefix --recursive
done