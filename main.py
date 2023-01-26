import telebot
import os

bot = telebot.TeleBot(os.environ["NM80_CLOUD_BOT_API"])

def get_list():
    list = []
    i = 0
    with open("list") as file:
        for line in file:
            line = line.rstrip('\n')
            i += 1
            new_id = line.split()[0]
            if new_id == line:
                new_summary = "empty"
            else:
                new_summary = line.split(' ', 1)[1]
            list.append([new_id, new_summary])
    return list

@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, "welcome to nm80 cloud bot")
    print(get_list())

@bot.message_handler(commands= ['add'])
def add(message):
    if message.reply_to_message != None:
        replied_message_id = message.reply_to_message.message_id
        exists = False
        for item in get_list():
            if str(replied_message_id) == item[0]:
                exists = True
                break
        if not exists:
            bot.reply_to(message, "message " + str(replied_message_id) + " added to cloud.")
            file = open("list","a+")
            file.write(str(message.reply_to_message.message_id))
            file.write("\n")
            file.close()
        else:
            bot.send_message(message.chat.id, "message " + str(replied_message_id) + " already exists in cloud.")
    else:
        bot.reply_to(message, "no reference for /add command")

# another method for /get command which I prefered not to use
#@bot.message_handler(regexp="^/get\s\d+$") #should be improved. currently user should check for right syntax.
#def get(message):
#    words = message.text.split()
#    id = words[-1]
#    print("got it")
#    bot.forward_message(chat_id = message.chat.id, from_chat_id = message.chat.id, message_id = int(id))

@bot.message_handler(regexp="^/\d+$")
def get_by_index(message):
    index = int(message.text[1:])
    id = get_list()[index - 1][0]
    bot.send_message(message.chat.id, "message with  \"index /" + str(index) + "\"  &  \"id " + str(id) + "\"  :")
#    bot.forward_message(chat_id = message.chat.id, from_chat_id = message.chat.id, message_id = id)
    bot.copy_message(chat_id = message.chat.id, from_chat_id = message.chat.id, message_id = id)

@bot.message_handler(commands = ['list'])
def list_command(message):
    list = get_list()
    contents_message = "here are the contents of your cloud:\n\n"
    i = 0
    for item in list:
        i += 1
        contents_message += "/" + str(i) + "  " + item[0] + "\n"
    bot.send_message(message.chat.id, contents_message)

bot.infinity_polling()
