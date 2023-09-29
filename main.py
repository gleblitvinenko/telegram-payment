import asyncio
import os

from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

import env
import logging

from aiogram import Bot, Dispatcher, types, Router

from aiogram.types.message import ContentType


logging.basicConfig(level=logging.INFO)

bot = Bot(token=env.TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
router = Router()

PRICE = types.LabeledPrice(label="Payment", amount=100000)


@router.message(Command("payment"))
async def payment(message: types.Message):
    if env.PAYMENT_TOKEN.split(":")[1] == "TEST":
        await bot.send_message(message.chat.id, "Payment!")

    await bot.send_invoice(
        message.chat.id,
        title="Payment for...",
        description="Payment description",
        provider_token=env.PAYMENT_TOKEN,
        currency="uah",
        is_flexible=False,
        prices=[PRICE],
        start_parameter="payment",
        payload="test-invoice-payload"
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message()
async def successful_payment(message: types.Message):
    if message.content_type == ContentType.SUCCESSFUL_PAYMENT:
        await bot.send_message(message.chat.id, f"Payment for the amount {message.successful_payment.total_amount // 100} {message.successful_payment.currency} passed successfuly!")


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
