from django.conf import settings
from django.contrib.auth.models import AbstractUser
from pyrtable.record import BaseRecord
from pyrtable.fields import StringField, BooleanField


class User(AbstractUser):
    pass


class UserAirtable(BaseRecord):
    class Meta:
        base_id = settings.AIRTABLE_ID
        table_id = 'User'

    @classmethod
    def get_api_key(cls):
        return settings.AIRTABLE_KEY

    tg_username = StringField('tg_username')
    tg_id = StringField('tg_id')
    tg_name = StringField('tg_name')
    password = StringField('password')
    signer = StringField('signer')
