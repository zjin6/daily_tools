import functools
import datetime as dt
import time
# from jjmixtools import print_runtime

'''
Here are 2 runtime wrapers with examples.
1. print_runtime(func) in 0:00:00
2. timer(func) in 00 secs

'''


# check time comsumption
def print_runtime(func):
    """Print run time for func."""
    @functools.wraps(func)
    def wrapper(*arg, **kwarg):
        start = dt.datetime.now()
        result = func(*arg, **kwarg)
        end = dt.datetime.now()
        print('\n' + 'runtime = ' + str(end - start).split('.')[0])
        return result
    
    return wrapper


@print_runtime
def print_x(sec):
    print('sleep now')
    time.sleep(sec)
    print('sleep over')
    return sec + 10
    



def timer(func):
    """Print the runtime of the decorated function."""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])
        
        
        
        