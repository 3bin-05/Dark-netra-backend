from flask import Flask
from flask_cors import CORS
from routes.detection_routes import detection_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(detection_bp)

@app.route("/")
def home():
    return "Dark Netra Backend Running Successfully!"

if __name__ == "__main__":
    app.run()