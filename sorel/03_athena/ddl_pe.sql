CREATE EXTERNAL TABLE IF NOT EXISTS `SOREL`.`PE_BIN` (
  `path` string,
  `modificationtime` timestamp,
  `length` bigint
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://sorel-20m-demo/output/'
TBLPROPERTIES ('classification' = 'parquet');