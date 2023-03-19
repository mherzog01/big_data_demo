
# CLI Reference:  https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/start-job-run.html
# Argument format:  https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html

arguments="--enable-auto-scaling=true" \
arguments="$arguments,--enable-metrics=true" \
arguments="$arguments,--enable-spark-ui=true" \
arguments="$arguments,--spark-event-logs-path='s3://aws-glue-assets-883375387566-us-east-1/sparkHistoryLogs/'" \
arguments="$arguments,--enable-continuous-cloudwatch-log=true"

echo $arguments

aws glue start-job-run \
    --job-name read-sorel-binaries \
    --worker-type G.2X \
    --number-of-worker 5 \
    --arguments=$arguments
    
    