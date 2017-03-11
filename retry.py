# Define retry util function


class RetryException(Exception):
    pass


def retry(func, max_retry=10):
    """
    @param func: The function that needs to be retry
                 (to pass function with arguments use partial object)
    @param max_retry: Maximum retry of `func` function, default is `10`
    @return: result of func
    @raise: RetryException if retries exceeded than max_retry
    """
    for retry in range(1, max_retry + 1):
        try:
            return func()
        except Exception:
            print ('Failed to call {}, in retry({}/{})'.format(func, retry, max_retry))
    else:
        raise RetryException(max_retry)
