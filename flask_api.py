from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/', methods=['POST'])
def getSetCompare():
   data = request.json
   userid = data.get('user', None)
   sourceApp = data.get('sourceApp', None)
   targetApp = data.get('targetApp', None)
   return jsonify({"user": userid , "sourceApp": sourceApp, "targetApp": targetApp })

if __name__ == '__main__':
   app.run(port=5000)  # run app on port 8080 in debug mode
