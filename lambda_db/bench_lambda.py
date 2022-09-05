import timeit
import time
import json
import boto3

#NUM_ITER=100*60
NUM_ITER=5000

client = boto3.client('lambda')

def run_benchmark():
    for iter_num in range(NUM_ITER):
        response = client.invoke(
                          FunctionName='worker',
                          InvocationType='Event',
                          #InvocationType='RequestResponse',
                          Payload=json.dumps({'worker_num': iter_num})
                                 )     
        print(f'Iteration {iter_num}.  Status={response["StatusCode"]}')
    print('Benchmark complete')

if __name__ == '__main__':
    timer = timeit.Timer(stmt=run_benchmark)
    exec_times = timer.repeat(1, number=1)
    print(f'Min time = {min(exec_times)}')
