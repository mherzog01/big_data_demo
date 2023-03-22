rm *.log
python transfer_sorel_bin_no_spark.py 00 > 00.log 2>&1 &
python transfer_sorel_bin_no_spark.py 01 > 01.log 2>&1 &
python transfer_sorel_bin_no_spark.py 02 > 02.log 2>&1 &
python transfer_sorel_bin_no_spark.py 03 > 03.log 2>&1 &
python transfer_sorel_bin_no_spark.py 04 > 04.log 2>&1 &
