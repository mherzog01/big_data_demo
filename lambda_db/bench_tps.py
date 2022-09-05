import timeit
import time

NUM_ITER=100*60

def run_benchmark():
    for iter_num in range(NUM_ITER):
        #print(f'Iteration {iter_num}')
        pass
    print('Benchmark complete')

if __name__ == '__main__':
    timer = timeit.Timer(stmt=run_benchmark)
    exec_times = timer.repeat(5, number=1)
    print(f'Min time = {min(exec_times)}')
