from flask import request, jsonify, Response, Blueprint
from db_access import DBConnection

subscriptions_api = Blueprint("subscriptions_api", __name__)


@subscriptions_api.route("/subscriptions", methods=["GET"])
def get_subscriptions():
    db = DBConnection()
    db.cursor.execute("SELECT * from subscriptions")
    results = db.cursor.fetchall()
    db.close()
    return jsonify(results)


@subscriptions_api.route("/subscription/<TCKN>/<platformid>", methods=["POST"])
def edit_subscription(TCKN, platformid):
    json = request.json
    db = DBConnection()

    db.cursor.execute("SELECT COUNT(*) as count FROM person WHERE TCKN=(%(TCKN)s)",
                      {"TCKN": json["TCKN"]})
    person_result = db.cursor.fetchone()

    if person_result["count"] == 0:
        db.close()
        return Response("Girilen TCKN'ye ait kayıtlı kişi yoktur!", status=500)

    db.cursor.execute("SELECT COUNT(*) as count FROM platforms WHERE ID=(%(platformid)s)",
                      {"platformid": json["platformid"]})
    platform_result = db.cursor.fetchone()
    if platform_result["count"] == 0:
        db.close()
        return Response("Girilen platform id'ye karşılık gelen bir platform kaydı yoktur!", status=500)

    db.cursor.execute(
        "UPDATE subscriptions SET TCKN=(%(TCKN_NEW)s), platformid=(%(platformid_NEW)s), startdate=(%(startdate)s), enddate=(%(enddate)s) "
        "WHERE TCKN=(%(TCKN_OLD)s) AND platformid=(%(platformid_OLD)s)",
        {"TCKN_NEW": json["TCKN"], "platformid_NEW": json["platformid"], "startdate": json["startdate"],
         "enddate": json["enddate"], "TCKN_OLD": TCKN, "platformid_OLD": platformid})
    db.commit()
    db.cursor.execute("SELECT * FROM subscriptions WHERE TCKN=(%(TCKN)s) AND platformid=(%(platformid)s)",
                      {"TCKN": json["TCKN"], "platformid": json["platformid"]})
    edited = db.cursor.fetchone()
    db.close()
    return jsonify(edited)


@subscriptions_api.route("/subscription", methods=["PUT"])
def insert_subscription():
    json = request.json
    db = DBConnection()

    db.cursor.execute("SELECT COUNT(*) as count FROM person WHERE TCKN=(%(TCKN)s)",
                      {"TCKN": json["TCKN"]})
    person_result = db.cursor.fetchone()

    if person_result["count"] == 0:
        db.close()
        return Response("Girilen TCKN'ye ait kayıtlı kişi yoktur!", status=500)

    db.cursor.execute("SELECT COUNT(*) as count FROM platforms WHERE ID=(%(platformid)s)",
                      {"platformid": json["platformid"]})
    platform_result = db.cursor.fetchone()
    if platform_result["count"] == 0:
        db.close()
        return Response("Girilen platform id'ye karşılık gelen bir platform kaydı yoktur!", status=500)

    db.cursor.execute("INSERT INTO subscriptions (TCKN, platformid, startdate, enddate) VALUES ((%(TCKN)s), (%(platformid)s), (%(startdate)s), (%(enddate)s))",
                      {"TCKN": json["TCKN"], "platformid": json["platformid"], "startdate": json["startdate"], "enddate": json["enddate"]})
    db.commit()
    db.cursor.execute("SELECT * FROM subscriptions WHERE TCKN=(%(TCKN)s) AND platformid=(%(platformid)s)",
                      {"TCKN": json["TCKN"], "platformid": json["platformid"]})
    insterted = db.cursor.fetchone()
    db.close()
    return jsonify(insterted)


@subscriptions_api.route("/subscription/<TCKN>/<platformid>", methods=["DELETE"])
def delete_subscription(TCKN, platformid):
    db = DBConnection()
    db.cursor.execute("DELETE FROM subscriptions WHERE TCKN=(%(TCKN)s) AND platformid=(%(platformid)s)",
                      {"TCKN": TCKN, "platformid": platformid})
    db.commit()
    db.close()
    return ""
