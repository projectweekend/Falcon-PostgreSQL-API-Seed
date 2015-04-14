from app import db


def open_cursor_hook(req, res, resource, params):
    resource.db = db
    resource.cursor = db.cursor()


def close_cursor_hook(req, res, resource):
    resource.cursor.close()
