from application import app, socketio

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)

