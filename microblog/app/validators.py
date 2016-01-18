from wtforms.validators import StopValidation
from app.models import User


class UniqueUsername(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            if self.message is None:
                message = field.gettext('Username must be unique.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)
