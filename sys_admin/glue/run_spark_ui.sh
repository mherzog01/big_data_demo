# Per https://github.com/aws-samples/aws-glue-samples/tree/master/utilities/Spark_UI/
export LOG_DIR="s3a://aws-glue-assets-883375387566-us-east-1/sparkHistoryLogs"
PROFILE_NAME="default"
docker run -itd -v ~/.aws:/root/.aws -e AWS_PROFILE=$PROFILE_NAME -e SPARK_HISTORY_OPTS="$SPARK_HISTORY_OPTS -Dspark.history.fs.logDirectory=$LOG_DIR  -Dspark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.DefaultAWSCredentialsProviderChain" -p 18080:18080 glue/sparkui:latest "/opt/spark/bin/spark-class org.apache.spark.deploy.history.HistoryServer"

echo "1.  Forward port 18080"
echo "2.  Go to http://localhost:18080"
