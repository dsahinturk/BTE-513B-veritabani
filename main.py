from flask import Flask, request, Response
from flask_cors import CORS
from db_access import DBConnection
from apis.Country_Api import country_api
from apis.People_Api import people_api
from apis.Platform_Api import platform_api
from apis.Subscriptions_Api import subscriptions_api


app = Flask(__name__)
CORS(app)
app.register_blueprint(country_api)
app.register_blueprint(people_api)
app.register_blueprint(platform_api)
app.register_blueprint(subscriptions_api)


@app.route("/login", methods=["POST"])
def login():
    db = DBConnection()
    json = request.json
    db.cursor.execute("SELECT * FROM credentials WHERE username=(%(username)s) AND password=(%(password)s)",
                      {"username": json["username"], "password": json["password"]})
    result = db.cursor.fetchone()
    if result is None:
        return Response("Kullanıcı adı veya şifre yanlış!", status=500)
    else:
        return Response("Giriş yapıldı", status=200)


app.run(host="127.0.0.1", port=5000)
