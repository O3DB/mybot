import os
import ptbot
import local_setting as setting
from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(time_timer, secs_left, stop_secs, message_id):
    bot.create_timer(int(stop_secs), bot.update_message, chat_ID, message_id, render_progressbar(time_timer, secs_left))


def reply(text):
    time_timer = parse(text)
    new_text = "Таймер запущен на {} секунд"
    bot.send_message(chat_ID, new_text.format(str(time_timer)))
    message_id = bot.send_message(chat_ID, render_progressbar(time_timer, time_timer))
    message_id = str(message_id)


    for i in range(time_timer):
        if i != 0:
            notify_progress(time_timer, time_timer - i, i, message_id)
        else:
            continue

    bot.create_timer(time_timer, bot.send_message, chat_ID, "\nВремя вышло!")


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("TOKEN")
    chat_ID = os.getenv("CHAT_ID")

    bot = ptbot.Bot(token)
    bot.send_message(chat_ID, "На сколько запустить таймер?")
    bot.wait_for_msg(reply)