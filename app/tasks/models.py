from application import ModelMixin, db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class Task(ModelMixin, db.Model):
    __tablename__ = 'Task'

    # user_id = db.Column(UUID(as_db.ForeignKey('User.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('User.id'))
    task_title = db.Column(db.String(64), nullable=False, unique=False)
    task_description = db.Column(db.Text, nullable=True, unique=False)
    # 0 = on Doing || 1 = Done !
    status = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id=None, task_title=None, task_description=None, status=0):
        self.user_id = user_id
        self.task_title = task_title
        self.task_description = task_description
        self.status = status

    @classmethod
    def register(cls, data: dict = None):
        if not data:
            raise Exception('Task.register() requires an argument for `data`')

        # validations
        required_fields = ['task_title']
        for field in required_fields:
            if field not in data.keys():
                return False, f"{field} is a required field"

        try:
            # does trigger with this name already exists
            task = cls.query.filter_by(
                task_title=data.get('task_title'),
            ).one_or_none()

            if task:
                return False, "A task with this name already exists. Try again with a different name."

            user = Task(**data)
            db.session.add(user)
            db.session.flush()
            db.session.commit()

            return True, user
        except Exception as e:
            print(str(e))
            return False, str(e)

    def update(self, data: dict = None):
        if not data:
            raise Exception('Task.update() requires an argument for `data`')

        try:
            unallowed_fields = ['id', 'user_id']
            for field in data.keys():
                if field not in unallowed_fields:
                    setattr(self, field, data.get(field))

            db.session.add(self)
            db.session.commit()

            return True, self
        except Exception as e:
            print(str(e))
            return False, str(e)
