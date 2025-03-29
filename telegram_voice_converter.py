import telebot
from pydub import AudioSegment
import os

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)
TEMP_DIR = r'D:\CV\temp files'
os.makedirs(TEMP_DIR, exist_ok=True)

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    try:
        #
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        input_path = os.path.join(TEMP_DIR, f"{message.audio.file_id}.mp3")
        output_path = os.path.join(TEMP_DIR, f"{message.audio.file_id}.ogg")

       
        with open(input_path, 'wb') as file:
            file.write(downloaded_file)

       
        sound = AudioSegment.from_file(input_path)
        sound.export(output_path, format="ogg", codec="libopus")

        
        with open(output_path, 'rb') as voice:
            bot.send_voice(message.chat.id, voice)
        os.remove(input_path)
        os.remove(output_path)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me an MP3 file, and I'll convert it into a voice message!")


print("Bot is running...")
bot.infinity_polling()
