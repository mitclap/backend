from app import app, db

with app.app_context():
    db.create_all()

if __name__=="__main__":
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)
    app.run(host='0.0.0.0', port=port, debug=debug) # For vagrant pass-through
