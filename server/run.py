import logging
from app import create_app

app = create_app()


if __name__ == "__main__":
    #Users.insert_user({
    #    "username": "pascal",
    #    "email": "532484187@qq.com",
    #    "password": "6812345"
    #    })
    app.run(port=5000)
    
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)