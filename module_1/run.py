from flask import Flask
from pages.home import home_bp
from pages.contact import contact_bp
from pages.projects import projects_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(contact_bp, url_prefix="/contact")
app.register_blueprint(projects_bp, url_prefix="/projects")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)