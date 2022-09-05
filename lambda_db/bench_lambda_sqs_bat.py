import timeit
import time
import json
import boto3

NUM_ITER=100*60*2
#NUM_ITER=20*60

BATCH_SIZE=10

client = boto3.client('sqs')

def run_benchmark():
    queue_url = 'q-std-bench-lambda'
    iter_num = 0
    while iter_num < NUM_ITER:
        entries=[{'Id':str(iter_num + i), 
                  'MessageBody':json.dumps({'worker_num': iter_num + i})
                  } for i in range(1,BATCH_SIZE + 1)
                ]
        iter_num += BATCH_SIZE
        response = client.send_message_batch(
                          QueueUrl=queue_url,
                          Entries=entries
                                 )     
        #print(response.keys())
        num_success = len(response.get("Successful",[]))
        num_failed = len(response.get("Failed",[]))
        print(f'Iteration {iter_num}.  # success={num_success} # fail={num_failed}')
    print('Benchmark complete')

if __name__ == '__main__':
    timer = timeit.Timer(stmt=run_benchmark)
    exec_times = timer.repeat(1, number=1)
    print(f'Min time = {min(exec_times)}')
