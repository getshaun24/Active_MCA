import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
import pymongo

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_mongo_db():
    """
    Configuration method to return db instance
    """

    db = getattr(g, "_mongo_db", None)

    if db is None:

        db = g._mongo_db = pymongo.MongoClient(current_app.config['MONGO_CLI'], tls=True)
       
    return db

def close_mongo_db(e=None):
    db = g.pop('_mongo_db', None)

    if db is not None:
        db.close()

# def init_db():
#     db = get_mongo_db()

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_mongo_db)

