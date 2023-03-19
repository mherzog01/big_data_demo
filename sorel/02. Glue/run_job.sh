# Format of user parameters are:
#       --parameter=value
#
# CLI Reference:  https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/start-job-run.html
# Argument format:  https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
#
# TODO Parse args and remove hardcoded values.  
#           --worker-type 
#           --number-of-worker 
# TODO Allow for other system params?  Allow for overrides of existing system params (e.g. auto-scaling)

arguments="--enable-auto-scaling=true" \
arguments="$arguments,--enable-metrics=true" \
arguments="$arguments,--enable-spark-ui=true" \
arguments="$arguments,--spark-event-logs-path='s3://aws-glue-assets-883375387566-us-east-1/sparkHistoryLogs/'" \
arguments="$arguments,--enable-continuous-cloudwatch-log=true"

job_name=$1
shift

user_args="$@"

echo "System arguments:"
echo $arguments

echo 
echo "User arguments"
echo $user_args

all_args=$arguments
if [ "$user_args" ]
then
    all_args="$all_args,$user_args"
fi

aws glue start-job-run \
    --job-name "$job_name" \
    --worker-type G.1X \
    --number-of-worker 5 \
    --arguments="$all_args"
    
    