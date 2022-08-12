from django.conf import settings
from aiogram import Bot, Dispatcher, executor, types
from django.core.signing import Signer

from .models import UserRecord

bot = Bot(token=settings.TG_TOKEN)
dp = Dispatcher(bot)


def save_object(user_object):
    user_object.save()


async def get_user_object(user):
    user_in_base = list(UserRecord.objects.filter(tg_id=user.id))
    if user_in_base:
        return next(iter(user_in_base))


async def create_user_object(user):
    signer = Signer(salt='airtable')
    key = signer.sign(user.username)
    user_inst = UserRecord(
        tg_username=user.username,
        tg_id=str(user.id),
        tg_name=user.first_name,
        signer=key,
    )
    save_object(user_inst)
    return user_inst


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
    await message.answer(f'Password is successfully updated\n'
                         f'If you want to change it just write new one')
    user = await get_user_object(message.from_user)
    user.password = message.text
    save_object(user)


def start_bot():
    executor.start_polling(dp, skip_updates=True)
