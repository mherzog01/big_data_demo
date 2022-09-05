NUM_ITER=$1
for ((i=1;i<=$NUM_ITER;i++))
do
	python3 bench_lambda.py > output$i.log 2>&1 & 
	echo "Launched instance $i"
done
