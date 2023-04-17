from flask import jsonify


def model_to_dict(model):
    '''
    Converts an SQLAlchemy Model object to a dictionary.
    '''
    if not model:
        return None

    columns = list(model.__table__.columns.keys())
    map = {}
    try:
        for field in columns:
            map[field] = getattr(model, field)
        return map
    except Exception as e:
        return str(e)


class Response:
    def __init__(
            self,
            success: bool = True,
            message: str = None,
            status_code: int = 406
    ):
        self.success = success
        self.message = message
        self.status_code = status_code

    def respond(self):
        data = dict(
            success=self.success,
            message=self.message
        )
        status = 200 if self.success and self.status_code == 406 else self.status_code
        return jsonify(data), status
