import os


HOST = "0.0.0.0"

PORT = 80

DATABASE = {
    "users": {
        "engine": os.environ.get(
            "DB_ENGINE",
            "mysql+pymysql://root:12eogns!@@127.0.0.1:3306/users?charset=utf8mb4",
        ),
        "echo": os.environ.get("DB_ECHO", "False") == "True",
        "pool_size": 10,
        "pool_recycle": 3600,
        "max_overflow": 5,
    },
    "tests": {
        "engine": os.environ.get(
            "DB_ENGINE",
            "mysql+pymysql://root:12eogns!@@127.0.0.1:3306/users?charset=utf8mb4",
        ),
        "echo": os.environ.get("DB_ECHO", "False") == "True",
        "pool_size": 10,
        "pool_recycle": 3600,
        "max_overflow": 5,
    },
}
