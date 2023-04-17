import traceback
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from typing import Any, List
from datetime import datetime
import uuid


# setup db
db = SQLAlchemy()


class ModelMixin(object):
    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    row_deleted = db.Column(db.Boolean, default=False, nullable=False)
    sn = db.Column(db.Integer, db.Identity(start=1, cycle=True), index=True)

    @classmethod
    def delete_many_by_id(cls, ids: List[str] = []):
        query = db.session.query(cls).filter(cls.id.in_(ids))
        rows = query.all()
        for row in rows:
            row.row_deleted = True
            row.deleted_at = datetime.utcnow()
        db.session.add_all(rows)
        db.session.commit()

    @classmethod
    def fetch_by_id(cls, id: str = None):
        query = db.session.query(cls).filter_by(id=id)
        return query.one_or_none()

    @classmethod
    def delete_by_id(cls, id: str = None):
        query = db.session.query(cls).filter_by(id=id)
        row = query.one_or_none()
        row.row_deleted = True
        row.deleted_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def id_exists(cls, id: str = None):
        query = db.session.query(cls.id).filter_by(id=id)
        return query.one_or_none() is not None

    def update(self, data: dict[str, Any] = None, unallowed_fields: List[str] = []):
        '''
        Updates a model. \n
        `data`: A dictionary `dict[str, Any]` of the data to update with.\n
        `unallowed_fields`: A list `List[str]` of fields to preclude from the update operation.
        '''
        if not data:
            raise Exception(
                'ModelMixin.update() requires an argument for `data`')

        try:
            unallowed_fields = unallowed_fields + ['id']
            for field in data.keys():
                if field not in unallowed_fields:
                    setattr(self, field, data.get(field))

            db.session.add(self)
            db.session.commit()

            return True, self
        except Exception as e:
            print(e)
            return False, str(e)


def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile("settings.py")

    # apply overrides for tests
    app.config.update(config_overrides)

    # initialize db
    db.init_app(app)
    # migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    # import blueprints
    from app.routes import root
    from app.user.endpoints import user_endpoints
    from app.tasks.endpoints import task_endpoints

    # register blueprints
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(user_endpoints, url_prefix='/user')
    app.register_blueprint(task_endpoints, url_prefix='/task')

    # @app.errorhandler(500)
    # def error_500_server(e):
    #     return render_template('500.html'), 500
    #
    # @app.errorhandler(404)
    # def page_not_found(e):
    #     return render_template('404.html'), 400
    #
    # @app.errorhandler(Exception)
    # def _unhandled_exception(exception):
    #     app.logger.error("server._unhandled_exception: %s, traceback: %s",
    #                      exception,
    #                      traceback.extract_tb(exception.__traceback__),
    #     )
    #     return {"message": "something went wrong"}, 500

    return app
