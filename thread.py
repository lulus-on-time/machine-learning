from findmyself import app

# print(app.config)
def flask_context_thread(target):
    with app.app_context():
        target()