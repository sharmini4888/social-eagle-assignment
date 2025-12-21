from flask import Flask, request, jsonify

app = Flask(__name__)

# GET API
@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "Hello from Python API!",
        "status": "success"
    })

# POST API
@app.route("/add", methods=["POST"])
def add_numbers():
    data = request.json
    a = data.get("a")
    b = data.get("b")

    result = a + b

    return jsonify({
        "a": a,
        "b": b,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)
