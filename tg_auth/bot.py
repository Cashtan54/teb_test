from django.conf import settings
from aiogram import Bot, Dispatcher, executor, types
from django.contrib.auth.hashers import check_password
from django.core.signing import Signer
from .models import UserAirtable, User
from asgiref.sync import sync_to_async

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher(bot)


def save_object(user_object):
    user_object.save()


async def get_user_object(user):
    user_in_base = list(UserAirtable.objects.filter(tg_id=user.id))
    if user_in_base:
        return user_in_base[0]


async def create_user_object(user):
    signer = Signer(salt='airtable')
    key = signer.sign(user.username)
    user_inst = UserAirtable(
        tg_username=user.username,
        tg_id=str(user.id),
        tg_name=user.first_name,
        signer=key,
    )
    save_object(user_inst)
    return user_inst


@sync_to_async
def change_password(user):
    django_user = User.objects.get(username=user.tg_username)
    django_user.set_password(user.password)
    django_user.save()
    print(check_password(user.password, django_user.password))
    return django_user


@dp.message_handler(commands="start")
async def start(message: types.Message):
    user = message.from_user
    await message.answer(f'Hello, {user.first_name}!\n'
                         f'Please, set your password')
    user_in_base = await get_user_object(user)
    if user_in_base:
        pass
    else:
        await create_user_object(user)


@dp.message_handler(content_types=['text'])
async def set_password(message: types.Message):
    await message.answer('Password is successfully updated\n'
                         'If you want to change it just write new one')
    user = await get_user_object(message.from_user)
    user.password = message.text
    save_object(user)
    await change_password(user)


def start_bot():
    executor.start_polling(dp, skip_updates=True)
