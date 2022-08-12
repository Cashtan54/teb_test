from django.db import models
from django.conf import settings
from pyrtable.record import BaseRecord
from pyrtable.fields import StringField, DateField, SingleSelectionField, \
        SingleRecordLinkField, MultipleRecordLinkField


class UserRecord(BaseRecord):
    class Meta:
        base_id = settings.AIRTABLE_ID
        table_id = 'User'

    @classmethod
    def get_api_key(cls):
        return settings.AIRTABLE_KEY

    tg_username = StringField('tg_username')
    tg_id = StringField('tg_username')
    tg_name = StringField('tg_username')

