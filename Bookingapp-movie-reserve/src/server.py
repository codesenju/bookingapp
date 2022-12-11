import time
import socket
from flask import Flask

app = Flask(__name__)

@app.route('/movie-reserve')
def reserve():
    return "<p>Movie tickets reserved - on node %s.</p>" % ( socket.gethostbyname(socket.gethostname()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    
    