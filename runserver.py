from app import app, db

with app.app_context():
    db.create_all()

if __name__=="__main__":
    port = app.config.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=True) # For vagrant pass-through
 
