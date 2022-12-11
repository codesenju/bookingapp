import time
import redis
import socket
import requests
from flask import Flask
from flask import json
from flask import render_template
from werkzeug.exceptions import HTTPException
backend_svc_url = "http://moviev2.internal-bookingapp.com:5000/movie"
app = Flask(__name__)
cache = redis.Redis(host='redis.internal-bookingapp.com', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            print("Exception occured while connecting redis")
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/home')
def hit():
    count = get_hit_count()
    response = requests.get(backend_svc_url)
    return "<h2>ServiceA - Welcome Bookingapp Home Page - on node %s.<br \>Hit count = %i.<br \></h1>Response from movie.internal-bookingapp.com service: %s "  % (  socket.gethostbyname(socket.gethostname()), int(count), response.content)


@app.errorhandler(500)
def internal_server_error(e):
    return  "<h1>ServiceA - Welcome Bookingapp Home Page</h1>Oops backend services not available.<h3>HTTP ERROR CODE: 500</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
