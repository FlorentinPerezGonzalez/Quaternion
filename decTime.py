import timeit, functools


# Decorator para medir el tiempo de ejecución de una función y hacer print al acabar
def temporizador(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        stop = timeit.default_timer()
        print('Time:', stop - start)
        return result
    return wrapper

# Decorator para medir el tiempo de ejecución de una función y modificar el return de la misma al valor en segundos
# del tiempo tardado
def temporizadorGetTime(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        stop = timeit.default_timer()
        return (stop - start)
    return wrapper