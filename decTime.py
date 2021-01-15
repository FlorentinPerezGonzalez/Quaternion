import timeit, functools

def temporizador(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        stop = timeit.default_timer()
        print('Time:', stop - start)
        return result
    return wrapper

def temporizadorGetTime(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        stop = timeit.default_timer()
        return (stop - start)
    return wrapper