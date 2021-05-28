import multiprocessing


loglevel = 'debug'
capture_output = True
bind = "0.0.0.0:80"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
# daemon = True

# preload_app = True
workers = multiprocessing.cpu_count() + 1
worker_class = 'gevent'

timeout = 120

keepalive = 20
