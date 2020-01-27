import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(off_time, secs_left, time_delay, message_id):
    bot.create_timer(int(time_delay), bot.update_message, chat_ID, message_id,
    render_progressbar(off_time, secs_left))


def reply(time_data):
    off_time = parse(time_data)
    bot.send_message(chat_ID, f"Таймер запущен на {off_time} секунд")
    message_id = bot.send_message(chat_ID, render_progressbar(off_time, off_time))
    message_id = str(message_id)


    for i in range(off_time):
        if i != 0:
            notify_progress(off_time, off_time - i, i, message_id)
        else:
            continue

    bot.create_timer(off_time, bot.send_message, chat_ID, "\nВремя вышло!")


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("TOKEN")
    chat_ID = os.getenv("CHAT_ID")

    bot = ptbot.Bot(token)
    bot.send_message(chat_ID, "На сколько запустить таймер?")
    bot.wait_for_msg(reply)