import telebot
import random
import schedule, time
from multiprocessing.context import Process
from telebot import types
from os import listdir
bot = telebot.TeleBot("API")
path = "D:/Python/Files/Bot/photo/"

facts_list = []
krehtelki_list = []
nicely_list = []
komment = []

user_id1 = ""
user_id2 = ""

joinedFile = open ("D:/Python/Files/Bot/userid.txt", "r") 
joinedUsers = set ()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

files = listdir("D:\Python\Files\Bot\photo")

def send_message():
    with open("D:/Python/Files/Bot/yearkomment.txt", encoding='utf-8') as file_komment:
        for string_komment in file_komment:
            komment.append(string_komment)
            
    # for user in joinedUsers:
    bot.send_message(user_id1, random.choice(komment))
    bot.send_message(user_id2, random.choice(komment))
        
schedule.every().day.at("12:00").do(send_message)
 
class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
 
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()

@bot.message_handler(commands=['start'])
def welcome(message):
#setNewUsers 
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open ("D:/Python/Files/Bot/userid.txt", "a") 
        joinedFile.write(str(message.chat.id) + "\n")
        joinedUsers.add(message.chat.id)
# Keybord
    if message.chat.id == user_id1 or message.chat.id == user_id2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        key_photo = types.KeyboardButton("Фото")
        key_krehtelki = types.KeyboardButton("Крехтелки")
        key_nicely = types.KeyboardButton("Милости")
        key_facts =  types.KeyboardButton("По факту")
        markup.add(key_photo, key_krehtelki, key_nicely, key_facts)

        bot.send_message(message.chat.id, "Приветики:3", parse_mode = 'html', reply_markup = markup)
    
@bot.message_handler(content_types=['text'])
def mes(message):
    if message.chat.id == user_id1 or message.chat.id == user_id2:
        if message.chat.type == 'private':
            if message.text == 'Фото':
                bot.send_photo(message.chat.id, open("".join([path, random.choice(files)]), 'rb'))

            elif message.text == 'Крехтелки':
                with open("D:/Python/Files/Bot/krehtelki.txt", encoding='utf-8') as file_krehtelki:
                    for string_krehtelki in file_krehtelki:
                        krehtelki_list.append(string_krehtelki)
                bot.send_message(message.chat.id, random.choice(krehtelki_list))
                
            elif message.text == 'Милости':
                with open("D:/Python/Files/Bot/nicely.txt", encoding='utf-8') as file_nicely:
                    for string_nicely in file_nicely:
                        nicely_list.append(string_nicely)
                bot.send_message(message.chat.id, random.choice(nicely_list))

            elif message.text == 'По факту':
                with open("D:/Python/Files/Bot/facts.txt", encoding='utf-8') as file_facts:
                    for string_facts in file_facts:
                        facts_list.append(string_facts)
                bot.send_message(message.chat.id, random.choice(facts_list))

if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass
 