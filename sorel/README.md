# SOREL 20 Million

GitHub:  https://github.com/sophos/SOREL-20M

Data:  s3://sorel-20m/09-DEC-2020

## Notes
* aws s3 --profile personal ls "s3://sorel-20m-demo/data/meta_sha256.txt" has ~13 MM rows
* Each row in `aws s3 ls` is ~97 bytes

### Improving Throughput 

My question:
https://stackoverflow.com/questions/75759423/high-volume-read-of-many-keys-in-an-s3-bucket
* Filtering with a prefix does not work:
    aws s3 cp s3://sorel-20m/09-DEC-2020/binaries/ . --recursive --dryrun --exclude '*' --include 'Z*'

  - Use pagination?
        >   https://stackoverflow.com/questions/39458814/counting-keys-in-an-s3-bucket
        > https://stackoverflow.com/questions/35442383/filter-a-glob-like-regex-pattern-in-boto3