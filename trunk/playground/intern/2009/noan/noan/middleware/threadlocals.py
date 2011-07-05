import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

def get_current_lang():
    lang = getattr(_thread_locals, 'lang', 'en-us')
    return lang.split('-')[0]

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.lang = getattr(request, 'LANGUAGE_CODE', 'en-us')
        _thread_locals.user = getattr(request, 'user', None)
