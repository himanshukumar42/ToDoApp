from application import create_app
from application import db

print("Creating Database")
app = create_app()
with app.app_context():
    print("Reached here")
    db.create_all()
print("Done")
