import sqlite3

from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from settings import DB_PATH

app = Flask(__name__)


class Connection:
    def __init__(self):
        self._connection: sqlite3.Connection | None = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PATH)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route("/phones/read")
def phones__read(phone=None, phones=None):
    with Connection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

    return '<br>'.join([f'{phone["phones_pk"]}: {phone["phoneID"]} - {phone["contactName"]} - {phone["phoneValue"]}'
                        for phone in phones])


@app.route("/phones/create")
@use_args({"phoneID": fields.Int(required=True), "contactName": fields.Str(required=True), "phoneValue": fields.Int(
    required=True)}, location="query")
def phones__create(args):
    with Connection() as connection:
        with connection:
            connection.execute(
                'INSERT INTO phones (phoneID, contactName, phoneValue) VALUES (:phoneID, :contactName, :phoneValue);',
                {"phoneID": args["phoneID"], "contactName": args["contactName"], "phoneValue": args["phoneValue"]},
            )

    return "Ok"


@app.route('/phones/update/<int:phones_pk>')
@use_args({"phoneValue": fields.Int(required=True)}, location="query")
def phones__update(args, phones_pk):
    with Connection() as connection:
        with connection:
            connection.execute(
                "UPDATE phones"
                "SET phoneValue=:phoneValue"
                "WHERE (phones_pk=:phones_pk);",
                {'phoneValue': args['phoneValue'], 'phones_pk': phones_pk},
            )

    return "Ok"


@app.route('/phones/delete/<int:phones_pk>')
def phones__delete(phones_pk):
    with Connection() as connection:
        with connection:
            connection.execute(
                "DELETE FROM phones WHERE (phones_pk=:phones_pk);",
                {"phones_pk": phones_pk, },
            )

    return "Ok"


if __name__ == '__main__':
    app.run()
