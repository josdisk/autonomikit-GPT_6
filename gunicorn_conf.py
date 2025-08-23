import multiprocessing as mp, os

bind = "0.0.0.0:8000"
workers = int(os.getenv("WORKERS", (mp.cpu_count() * 2) + 1))
threads = int(os.getenv("THREADS", "2"))
keepalive = int(os.getenv("KEEPALIVE", "75"))
worker_class = "uvicorn.workers.UvicornWorker"
timeout = int(os.getenv("TIMEOUT", "120"))
graceful_timeout = int(os.getenv("GRACEFUL_TIMEOUT", "30"))
loglevel = os.getenv("LOGLEVEL", "info")
