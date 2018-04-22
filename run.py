from Block import Block, Blockchain
from flask import Flask, request, json, make_response, render_template

# start a flask instance
app = Flask(__name__)

# custom response headers to handle CORS
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5000/mine_block')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# create instance of the brand new blockchain
blockchain = Blockchain()

# POST route to this endpoint mines the block
@app.route("/mine_block", methods=["POST"])
def mine_block():
    params = request.values

    # print "params = " + str(params)

    previous_block = blockchain.get_latest_block()
    new_block = blockchain.generate_next_block(previous_block, params["data"])

    result = {}
    if blockchain.validate_block(new_block, previous_block):
        blockchain.add_block(new_block)
        print "Block added by node {}".format(params["id"])
        result["success"] = True
        result["msg"] = "Block added by client {}.".format(params["id"])
        result["timestamp"] = new_block.timestamp
        result["hash"] = new_block.hash
    else:
        result["success"] = False
        result["msg"] = "Validation failed."

    response = make_response(json.dumps(result))
    response.headers['content-type'] = 'application/json'

    return response

# GET route to this endpoint renders the index page
@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

# GET route to the following endpoints displays the specific files
@app.route("/js/mine.js", methods=["GET"])
def include_js():
    return render_template('/js/mine.js')

@app.route("/js/constants.js", methods=["GET"])
def constants():
    return render_template('/js/constants.js')

@app.route("/css/main.css", methods=["GET"])
def css():
    return render_template('/css/main.css')

# Run the server
app.run()
