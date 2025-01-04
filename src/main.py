from background import keep_alive
from config import BOT_TOKEN, API_ID, API_HASH, HF_KEY
from telethon.sync import TelegramClient, events, Button
import os

from models.transcriber import Transcriber
from models.summarizer import Summarizer
from utils import convert_to_audio

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
transcriber = Transcriber(hf_key=HF_KEY)
summarizer = Summarizer(hf_key=HF_KEY, model='mistralai/Mistral-Nemo-Instruct-2407')


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        'Привет! Я бот для суммаризации видео. Чтобы узнать как мной пользоваться отправьте команду /help.')


@bot.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.respond('Помощь')


@bot.on(events.NewMessage)
async def summarize_video(event):
    if event.video:
        try:
            await event.respond('Подождите, видео обрабатывается')

            if not os.path.exists(".temp"):
                os.mkdir('.temp')

            await event.download_media('.temp/to_transcribe.mp4')

            audio_path = convert_to_audio('.temp/to_transcribe.mp4')
            text = transcriber.transcribe(audio_path)['text']
            print(text)

            await event.respond(summarizer.summarize(text))

            os.remove('.temp/to_transcribe.mp4')
            os.remove(audio_path)
            os.rmdir('.temp')
        except Exception as ex:
            await event.respond('Что-то пошло не так...')
            os.remove('.temp/to_transcribe.mp4')
            os.remove(audio_path)
            os.rmdir('.temp')
            print(str(ex))


def main():
    bot.start()
    bot.run_until_disconnected()


if __name__ == '__main__':
    keep_alive()
    main()
