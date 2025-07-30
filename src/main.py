import os
import logging

from background import keep_alive
from config import BOT_TOKEN, API_ID, API_HASH, HF_KEY
from telethon.sync import TelegramClient, events, Button
from models.transcriber import Transcriber
from models.summarizer import Summarizer
from utils import convert_to_audio

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
transcriber = Transcriber(hf_key=HF_KEY)
summarizer = Summarizer(hf_key=HF_KEY)


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        'Привет! Я бот для выделения ключевых моментов из видео. Чтобы узнать как мной пользоваться отправьте команду /help.')


@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond(
        'Чтобы выделить ключевые моменты из видео, просто отправь его мне и я все сделаю.\n\nМеня захостили на бесплатном сервере, поэтому иногда что-то может пойти не так, но ты всегда можешь прислать видео еще раз.')


@bot.on(events.NewMessage)
async def summarize_from_youtube(event):
    pass

@bot.on(events.NewMessage)
async def summarize_video(event):
    if event.video:
        try:
            await event.respond('Подождите, видео обрабатывается...')

            if not os.path.exists(".temp"):
                os.mkdir('.temp')

            await event.download_media('.temp/to_transcribe.mp4')
        except Exception as ex:
            await event.respond('Не удалось обработать видео. Попробуйте еще раз.')
            os.remove('.temp/to_transcribe.mp4')
            os.rmdir('.temp')
            logging.exception(str(ex))

        try:
            audio_path = convert_to_audio('.temp/to_transcribe.mp4')
            text = transcriber.transcribe(audio_path)['text']
            await event.respond(summarizer.summarize(text))
            os.remove('.temp/to_transcribe.mp4')
            os.remove(audio_path)
            os.rmdir('.temp')
        except Exception as ex:
            await event.respond('Не удалось выполнить суммаризацию. Попробуйте еще раз.')
            os.remove('.temp/to_transcribe.mp4')
            os.remove(audio_path)
            os.rmdir('.temp')
            logging.exception(str(ex))

def main():
    bot.start()
    bot.run_until_disconnected()


if __name__ == '__main__':
    keep_alive()
    main()
