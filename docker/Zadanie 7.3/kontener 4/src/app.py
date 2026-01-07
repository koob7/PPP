from flask import Flask

server = Flask(__name__)


@server.route("/", methods=["POST", "GET"])
def hello():
    return "Hello kontener 4"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
