Setup
1.  Create MySql instance
2.  Create table in ddl
3.  Lambda function worker_db must have the pip file 
	- Same VPC as db
4.  Lambda function ```worker``` does 10 TPS
5.  S3 bucket https://s3.console.aws.amazon.com/s3/buckets/aws-scale-demo - zip file for deploying #3
6.  RDS/Lambda functions https://docs.aws.amazon.com/lambda/latest/dg/services-rds-tutorial.html

Pipeline
1.  Run bench_lambda_sqs_bat.py


Other config
- Create ~/.my.cnf with MySql connection info