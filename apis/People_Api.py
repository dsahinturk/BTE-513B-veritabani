from flask import request, jsonify, Response, Blueprint
from db_access import DBConnection

people_api = Blueprint("people_api", __name__)


@people_api.route("/people", methods=["GET"])
def get_people():
    db = DBConnection()
    db.cursor.execute("SELECT * from person")
    results = db.cursor.fetchall()
    db.close()
    return jsonify(results)


@people_api.route("/person/<TCKN>", methods=["POST"])
def edit_person(TCKN):
    json = request.json
    db = DBConnection()
    db.cursor.execute("UPDATE person SET TCKN=(%(TCKN_NEW)s), name=(%(name)s), surname=(%(surname)s) WHERE TCKN=(%(TCKN_OLD)s)",
                      {"TCKN_NEW": json["TCKN"], "TCKN_OLD": TCKN, "name": json["name"], "surname": json["surname"]})
    db.commit()
    db.cursor.execute("SELECT * FROM person WHERE TCKN=(%(TCKN_NEW)s)", {"TCKN_NEW": json["TCKN"]})
    edited = db.cursor.fetchone()
    db.close()
    return jsonify(edited)


@people_api.route("/person/<TCKN>", methods=["DELETE"])
def delete_person(TCKN):
    db = DBConnection()
    db.cursor.execute("SELECT COUNT(*) as count FROM subscriptions WHERE TCKN=(%(TCKN)s)",
                      {"TCKN": TCKN})
    result = db.cursor.fetchone()
    if result["count"] != 0:
        db.close()
        return Response(
            "Bu kişiyi kullanan subscription kaydı olduğundan silinme işlemi başarısız",
            status=500
        )
    else:
        db.cursor.execute("DELETE FROM person WHERE TCKN=(%(TCKN)s)", {"TCKN": TCKN})
        db.commit()
        db.close()
        return jsonify(result)


@people_api.route("/person", methods=["PUT"])
def insert_person():
    json = request.json
    db = DBConnection()
    db.cursor.execute("INSERT INTO person (TCKN, name, surname) VALUES ((%(TCKN)s), (%(name)s), (%(surname)s))",
                      {"TCKN": json["TCKN"], "name": json["name"], "surname": json["surname"]})
    db.commit()
    db.cursor.execute("SELECT * FROM person WHERE TCKN=(%(TCKN)s)", {"TCKN": json["TCKN"]})
    insterted = db.cursor.fetchone()
    db.close()
    return jsonify(insterted)
