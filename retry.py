# Helper script with retry utility function

# set logging for `retry` channel
import logging
logger = logging.getLogger('retry')


# Define Exception class for retry
class RetryException(Exception):
    DESCRIPTION = "Exception ({}) raised after {} tries."

    def __init__(self, exception, max_retry):
        self.exception = exception
        self.max_retry = max_retry
        
    def __unicode__(self):
        return self.DESCRIPTION.format(self.exception, self.max_retry)
    
    def __str__(self):
        return self.__unicode__()

    
# Define retry utility function
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
        except Exception, e:
            logger.info('Failed to call {}, in retry({}/{})'.format(func.func,
                                                           retry, max_retry))
    else:
        raise RetryException(e, max_retry)
