from application import ModelMixin, db
from datetime import datetime


class User(ModelMixin, db.Model):
    __tablename__ = 'User'

    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, unique=False)
    # 0 = New User || 1 = Old User
    new_user = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, username=None, password=None, new_user=0):
        self.username = username
        self.password = password
        self.new_user = new_user

    @classmethod
    def register(cls, data: dict = None):
        if not data:
            raise Exception('User.register() requires an argument for `data`')

        # validations
        required_fields = ['username', 'password']
        for field in required_fields:
            if field not in data.keys():
                return False, f"{field} is a required field"

        try:
            # does trigger with this name already exists
            user = cls.query.filter_by(
                username=data.get('username'),
            ).one_or_none()

            if user:
                return False, "A user with this username already exists. Try again with a different username."

            user = User(**data)
            db.session.add(user)
            db.session.flush()
            db.session.commit()

            return True, user
        except Exception as e:
            print(str(e))
            return False, str(e)

    def update(self, data: dict = None):
        if not data:
            raise Exception('User.update() requires an argument for `data`')

        try:
            unallowed_fields = ['id']
            for field in data.keys():
                if field not in unallowed_fields:
                    setattr(self, field, data.get(field))

            db.session.add(self)
            db.session.commit()

            return True, self
        except Exception as e:
            print(str(e))
            return False, str(e)
