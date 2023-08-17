from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/receive_array', methods=['POST'])
def receive_array():
    data = request.json
    array_3d = np.array(data['array_3d'])
    print(array_3d)

    return 'Array received and processed successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
