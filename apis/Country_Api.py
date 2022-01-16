from flask import request, jsonify, Response, Blueprint
from db_access import DBConnection

country_api = Blueprint("country_api", __name__)


@country_api.route("/countries", methods=["GET"])
def get_countries():
    db = DBConnection()
    db.cursor.execute("SELECT * from countries")
    results = db.cursor.fetchall()
    db.close()
    return jsonify(results)


@country_api.route("/country/<code>", methods=["POST"])
def edit_country(code):
    db = DBConnection()
    json = request.json
    db.cursor.execute("UPDATE countries SET name=(%(name)s), language=(%(language)s) WHERE code=(%(code)s)",
                      {"code": code, "name": json["name"], "language": json["language"]})
    db.commit()
    country = get_country(code, db, True)
    return jsonify(country)


@country_api.route("/country/<code>", methods=["DELETE"])
def delete_country(code):
    db = DBConnection()
    db.cursor.execute("SELECT COUNT(*) as count FROM platforms WHERE countrycode=(%(countrycode)s)",
                      {"countrycode": code})
    result = db.cursor.fetchone()
    if result["count"] != 0:
        db.close()
        return Response(
            "Bu country'i kullanan platform kaydı olduğundan silinme işlemi başarısız",
            status=500
        )
    else:
        db.cursor.execute("DELETE FROM countries WHERE code=(%(code)s)", {"code": code})
        db.commit()
        db.close()
        return jsonify(result)


@country_api.route("/country", methods=["PUT"])
def insert_country():
    json = request.json
    db = DBConnection()
    db.cursor.execute("INSERT INTO countries (code, name, language) VALUES ((%(code)s), (%(name)s), (%(language)s))",
                      {"code": json["code"], "name": json["name"], "language": json["language"]})
    db.commit()
    country = get_country(json["code"], db, True)
    return jsonify(country)


def get_country(code, db, close=False):
    db.cursor.execute("SELECT * from countries WHERE code=(%(code)s)", {"code": code})
    result = db.cursor.fetchone()
    if close is True:
        db.close()
    return result
