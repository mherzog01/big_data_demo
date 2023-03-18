bucket={$1-sorel-20m-demo}
shift
key=$1
aws --profile personal s3api get-object --bucket $bucket --key data/meta_sha256.txt --range bytes=0-10000 output.txt