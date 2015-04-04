from app import app, socketio, db

with app.app_context():
    db.create_all()

if __name__=="__main__":
    port = app.config.get('PORT', 5000)
    socketio.run(app, host='0.0.0.0', port=port) # For vagrant pass-through
