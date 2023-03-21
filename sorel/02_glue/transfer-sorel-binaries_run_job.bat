aws --region us-east-1 --profile personal glue start-job-run --job-name transfer-sorel-binaries --worker-type G.1X --number-of-worker 5 --arguments="--enable-auto-scaling=true,--enable-metrics=true,--enable-spark-ui=true,--spark-event-logs-path='s3://aws-glue-assets-883375387566-us-east-1/sparkHistoryLogs/',--enable-continuous-cloudwatch-log=true,--filter_chars=%1"