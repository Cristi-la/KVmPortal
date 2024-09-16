import threading

def debounce(wait_time):
    """
    Decorator that debounces a function so it is only called after wait_time seconds,
    but always with the latest arguments provided during that period. The timer
    does not reset; instead, the arguments are updated if the function is called again.
    """

    def decorator(function):
        def debounced(*args, **kwargs):
            # Update the latest arguments to be used when the timer expires
            debounced._latest_args = args
            debounced._latest_kwargs = kwargs

            # If there's no active timer, start a new one
            if debounced._timer is None:
                def call_function():
                    debounced._timer = None
                    # Execute the function with the latest arguments
                    return function(*debounced._latest_args, **debounced._latest_kwargs)

                debounced._timer = threading.Timer(wait_time, call_function)
                debounced._timer.start()

        # Initialize the timer and latest arguments storage
        debounced._timer = None
        debounced._latest_args = None
        debounced._latest_kwargs = None
        return debounced

    return decorator
