from flask import current_app
from flask_login import UserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
                         BadSignature, SignatureExpired
from sqlalchemy_utils import ArrowType
import arrow
import uuid
import hashlib


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), index=True)
    password_hash = db.Column(db.String(128))
    registered_at = db.Column(ArrowType, default=arrow.utcnow)
    last_seen = db.Column(ArrowType, default=arrow.utcnow)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid but expired...
            current_app.logger.info('Expired token.')
            return None
        except BadSignature:
            # Invalid token!
            current_app.logger.info('Invalid token.')
            return None
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User: {} ({})>'.format(self.id, self.email)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
