from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dify API configuration
DIFY_API_BASE = "http://localhost:5001"  # Your local Dify instance

# Read the HTML file content
def load_html_template():
    """Load the HTML chatbot file"""
    try:
        with open('travelbot.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return """
        <h1>Error: HTML file not found</h1>
        <p>Please make sure 'travelbot.html' is in the same directory as app.py</p>
        <p>Current directory: {}</p>
        """.format(os.getcwd())

@app.route('/')
def index():
    """Serve the main chatbot page"""
    html_content = load_html_template()
    return render_template_string(html_content)

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    """Proxy endpoint for Dify chat API to handle CORS"""
    try:
        # Get data from frontend
        data = request.get_json()
        # Forward request to Dify
        response = requests.post(
            f"{DIFY_API_BASE}/v1/chat-messages",
            headers={
                'Authorization': request.headers.get('Authorization'),
                'Content-Type': 'application/json'
            },
            json=data,
            timeout=30
        )

        # Return Dify's response
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to connect to Dify',
            'message': str(e)
        }), 500

@app.route('/api/suggestions/<message_id>')
def suggestions_proxy(message_id):
    """Proxy endpoint for Dify suggestions API"""
    try:
        # Get user parameter from query string
        user = request.args.get('user', 'user-123')

        # Forward request to Dify
        response = requests.get(
            f"{DIFY_API_BASE}/v1/messages/{message_id}/suggested",
            headers={
                'Authorization': request.headers.get('Authorization'),
                'Content-Type': 'application/json'
            },
            params={'user': user},
            timeout=30
        )

        # Return Dify's response
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Failed to get suggestions from Dify',
            'message': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test connection to Dify
        response = requests.get(f"{DIFY_API_BASE}/health", timeout=5)
        dify_status = "connected" if response.status_code == 200 else "disconnected"
    except:
        dify_status = "disconnected"
    
    return jsonify({
        'flask_server': 'running',
        'dify_connection': dify_status,
        'dify_url': DIFY_API_BASE
    })

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("📁 Current directory:", os.getcwd())
    print("🌐 Server will be available at: http://localhost:4000")
    print("🔗 Dify API URL:", DIFY_API_BASE)
    print("💡 Make sure your Dify instance is running on localhost:5001")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',  # Allow access from other devices on network
        port=4000,       # Use port 1000 to avoid conflicts
        debug=True       # Enable auto-reload during development
    )
