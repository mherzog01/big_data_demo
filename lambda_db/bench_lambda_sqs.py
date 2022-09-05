import timeit
import time
import json
import boto3

#NUM_ITER=100*60
NUM_ITER=20*60

client = boto3.client('sqs')

def run_benchmark():
    queue_url = 'q-std-bench-lambda'
    for iter_num in range(NUM_ITER):
        response = client.send_message(
                          QueueUrl=queue_url,
                          MessageBody=json.dumps({'worker_num': iter_num})
                                 )     
        #print(response.keys())
        print(f'Iteration {iter_num}.  MessageId={response["MessageId"]}')
    print('Benchmark complete')

if __name__ == '__main__':
    timer = timeit.Timer(stmt=run_benchmark)
    exec_times = timer.repeat(1, number=1)
    print(f'Min time = {min(exec_times)}')
