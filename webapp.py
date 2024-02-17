import flask
import dashboard

app = flask.Flask(__name__)
@app.get("/")
def index():
    return dashboard.render_dashboard(flask.request)

if __name__ == "__main__":
    # Local development only
    # Run "python web_app.py" and open http://localhost:8080
    app.run(host="localhost", port=8080, debug=True)
