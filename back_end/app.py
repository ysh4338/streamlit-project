from flask import Flask
from login import login_blueprint
from get_destination import get_destinations_blueprint
from add_destination import add_destination_blueprint
from delete_destination import delete_destination_blueprint
from update_destination import update_destination_blueprint

app = Flask(__name__)
app.register_blueprint(login_blueprint)
app.register_blueprint(get_destinations_blueprint)
app.register_blueprint(add_destination_blueprint)
app.register_blueprint(delete_destination_blueprint)
app.register_blueprint(update_destination_blueprint)

if __name__ == '__main__':
    app.run(debug=True)