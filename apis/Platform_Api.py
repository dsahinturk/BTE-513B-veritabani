from flask import request, jsonify, Response, Blueprint
from db_access import DBConnection

platform_api = Blueprint("platform_api", __name__)


@platform_api.route("/platforms", methods=["GET"])
def get_platforms():
    db = DBConnection()
    db.cursor.execute("SELECT * from platforms")
    results = db.cursor.fetchall()
    db.close()
    return jsonify(results)


@platform_api.route("/platform/<platform_id>", methods=["POST"])
def edit_platform(platform_id):
    json = request.json
    db = DBConnection()
    db.cursor.execute("UPDATE platforms SET name=(%(name)s), countrycode=(%(countrycode)s) WHERE id=(%(platform_id)s)",
                      {"platform_id": platform_id, "name": json["name"], "countrycode": json["countrycode"]})
    db.commit()
    db.cursor.execute("SELECT * FROM platforms WHERE id=(%(platform_id)s)", {"platform_id": platform_id})
    edited = db.cursor.fetchone()
    db.close()
    return jsonify(edited)


@platform_api.route("/platform", methods=["PUT"])
def insert_platform():
    json = request.json
    db = DBConnection()

    db.cursor.execute("INSERT INTO platforms (name, countrycode) VALUES ((%(name)s), (%(countrycode)s))",
                      {"name": json["name"], "countrycode": json["countrycode"]})
    db.commit()
    db.cursor.execute("SELECT * FROM platforms WHERE id=( SELECT MAX(id) FROM platforms )")
    insterted = db.cursor.fetchone()
    db.close()
    return jsonify(insterted)


@platform_api.route("/platform/<platformid>", methods=["DELETE"])
def delete_platform(platformid):
    db = DBConnection()
    db.cursor.execute("SELECT COUNT(*) as count FROM subscriptions WHERE platformid=(%(platformid)s)",
                      {"platformid": platformid})
    result = db.cursor.fetchone()
    if result["count"] != 0:
        db.close()
        return Response(
            "Bu platformu kullanan subscription kaydı olduğundan silinme işlemi başarısız",
            status=500
        )
    else:
        db.cursor.execute("DELETE FROM platforms WHERE ID=(%(ID)s)", {"ID": platformid})
        db.commit()
        db.close()
        return jsonify(result)
