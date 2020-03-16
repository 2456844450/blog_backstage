

from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean

from werkzeug.security import generate_password_hash , check_password_hash
class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)

    type = Column(Integer, default=2)
    avatar = Column(String(100))
    name = Column(String(30), nullable=False)

    _password = Column('password', String(100), nullable=False)

    launched = Column(Boolean, default=False)

    state = Column(Integer, default=1)

    roles = Column(String(100), default='user')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)