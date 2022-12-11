# bookingapp-moviev2
import time
import redis
import socket
import requests
from flask import Flask
movie_reserve_url = "http://movie-reserve.internal-bookingapp.com:5000/movie-reserve"
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


@app.route('/movie')
def hit():
    count = get_hit_count()
    response = requests.get(movie_reserve_url)
    return "<html><h2>ServiceBv2 -  Movie Booking Page Version 2.0  - on node %s.<br \>Hit count = %i.</h2><br \>Response from movie-reserve.internal-bookingapp.com service: %s "  % (  socket.gethostbyname(socket.gethostname()), int(count), response.content)

@app.errorhandler(500)
def internal_server_error(e):
    return  "<h2>Movie Booking Page Version 2.0</h2>Oops backend service '" + movie_reserve_url + "' not available.<h5>HTTP ERROR CODE: 500</h5>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
