import requests 
  
def exception_handler(func):
    """
    Decorator used to handle exceptions thrown while sending HTTP requests
    """
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
          description_buffer = str(e.response.json()) + "\n" + str(e)
          return False, description_buffer
    return inner_function