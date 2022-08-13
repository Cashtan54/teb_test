from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from tg_auth.models import UserAirtable, User


class Command(BaseCommand):
    help = 'Fill db with airtable data'

    def handle(self, *args, **options):
        User.objects.all().delete()
        airtable_users = UserAirtable.objects.all()
        for user in airtable_users:
            password = make_password(user.password)
            User.objects.create(username=user.tg_username, password=password)
        print('All users added to db')
