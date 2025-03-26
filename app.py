# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from controller import process_data
import logging
from http import HTTPStatus
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['POST'])
async def handle_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "Invalid request",
                "message": "No data provided"
            }), HTTPStatus.BAD_REQUEST
            
        # Log incoming requests
       # logger.info(f"Received request with data: {data}")
        
        # Process the data asynchronously
        result = await process_data(data)
        return jsonify(result), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": "Processing error",
            "message": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)
