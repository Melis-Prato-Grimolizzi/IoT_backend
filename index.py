from flask import Flask
import _routes

app = Flask(__name__)
app.register_blueprint(_routes.users)

@app.route("/")
def root():
  return "Non c'è niente qui"

if __name__ == "__main__":
    app.run()
