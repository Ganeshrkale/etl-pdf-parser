from app import app
from waitress import serve

# Set-ExecutionPolicy Unrestricted -Scope Process

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5001)
    # app.run(host='0.0.0.0', port=5001, debug=True)