# -*- coding: utf-8 -*-
from aiogram import types

from .kernel import BotanistDispatcher

from .docxer import ReportData, docxer
from .translator import translator
from .searcher import searcher
from .catter import catter
from .musician import musician


# front-controller:
def init_handlers(dispatcher: BotanistDispatcher) -> None:
    def format_hint(format: str) -> str:
        return \
            '<b>Формат команды:</b>\n' \
            f'<code>{format}</code>'


    @dispatcher.message_handler(commands=['start'])
    async def _(msg: types.Message) -> None:
        await msg.answer(\
            'Botanist работает исправно.\n' \
            'Нажмите на <b>Меню</b> для просмотра команд.'
        )


    @dispatcher.message_handler(commands=['report'])
    async def _(msg: types.Message) -> None:
        rc = list(map( # report context
            str.strip, msg.get_args().split(',')
        ))

        try:
            report_data = ReportData(
                discipline=f'{rc[0][0].upper()}{rc[0][1:]}',
                topic=f'{rc[1][0].upper()}{rc[1][1:]}',
                student=rc[2].title(),
                teacher=rc[3].title()
            )

            await docxer.send_report(msg, report_data)
        except IndexError:
            await msg.reply(format_hint('/report дисциплина, тема, студент, препод'))
        except Exception as unhandled_error:
            print(f'[unhandled_error][report]: {unhandled_error}')

            await msg.reply('Реферат не удался 🤒')


    @dispatcher.message_handler(commands=['translate'])
    async def _(msg: types.Message) -> None:
        text = msg.get_args().strip()

        if not text:
            await msg.reply(format_hint('/translate текст'))
            return

        try:
            await msg.reply(translator.translate(text))
        except Exception as unhandled_error:
            print(f'[unhandled_error][translate]: {unhandled_error}')

            await msg.reply('Перевод не удался 🤯')


    @dispatcher.message_handler(commands=['wiki'])
    async def _(msg: types.Message) -> None:
        topic = msg.get_args().strip()

        if not topic:
            await msg.reply(format_hint('/wiki тема'))
            return

        try:
            await msg.reply(searcher.surf(topic, True))
        except Exception as unhandled_error:
            print(f'[unhandled_error][wiki]: {unhandled_error}')

            await msg.reply('Почему-то не смог найти 🥲')


    @dispatcher.message_handler(commands=['cat'])
    async def _(msg: types.Message) -> None:
        try:
            await catter.send_random_cat_img(msg)
        except Exception as unhandled_error:
            print(f'[unhandled_error][cat]: {unhandled_error}')

            await msg.reply('Не удалось отправить котика 😿')


    @dispatcher.message_handler(commands=['music'])
    async def _(msg: types.Message) -> None:
        try:
            await musician.send_random_music(msg)
        except Exception as unhandled_error:
            print(f'[unhandled_error][music]: {unhandled_error}')

            await msg.reply('Музыки не будет 😓')
