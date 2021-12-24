import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, messagehandler
import logging
import schedule

# Auth token
TOKEN = open("authkey", 'r').readline() #str(os.environ['TOKEN_KEY'])

bot = telegram.Bot(token=TOKEN)
#updates = bot.get_updates()
#print(updates[0]['message']['forward_from']['id']); exit()

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# =========================================================================================================
# Non-API functions
# =========================================================================================================
def get_message(text):
    text_lower = text.lower()
    first_index = text_lower.split().index('send')
    second_index = text_lower.split().index('to')
    msg = " ".join([word.strip('"').strip("'") for word in text.split()[first_index+1:second_index]])
    return msg

#def get_user(text):


def get_send_time(text):
    text_lower = text.lower()
    time_index = text_lower.split().index('at') + 1
    tm = text.split()[time_index]
    return tm



# =========================================================================================================


# A function to process a specific type of update:
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""Hi! I'm a bot designed to help you schedule telegram messages.\n
        To send a message at time '12:34' to user 'John', tell me to do so in this form:\n\n 
        send 'I love you!' to John at 12:34\n\nTalk to me!""")

# A function called every time the Bot receives a Telegram message that contains the /start command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)



def schedule_message(update, context):
    # Grab required text elements
    msg = get_message(update.message.text)
    tm = get_send_time(update.message.text)

    # update of the person to send message to
    # we forward any message from this user to the bot first so that we can get user info for the bot
    usr = bot.get_updates()[0]['message']['forward_from']['id']
    #usr = 404768059
    #context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    context.bot.send_message(chat_id=usr, text=msg)
    #bot.sendMessage(chat_id=usr, text=msg)

# A function called every time the Bot receives a Telegram message that contains the /schedule_message command
scheduleMessage_handler = CommandHandler('schedule_message', schedule_message)
dispatcher.add_handler(scheduleMessage_handler)


# For commands that the bot doesn't understand:
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



# starting the bot
updater.start_polling()
