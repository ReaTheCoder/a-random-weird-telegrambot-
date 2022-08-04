#import nessecary modules  

from telegram import *
#-----------------------
from telegram.ext import *
#------------------------
import requests
#-----------------------
import logging
#-----------------------
import wikipedia
#-----------------------
from datetime import date
#-------------------------
import warnings
#-------------------------
from pytube import YouTube
#--------------------------
import youtube_dl
#-------------------------
import os
#------------------------
import re
#-------------------------
#from moviepy.editor import *


#receive the updates from Telegram and to deliver them to said dispatcher
updater = Updater(token="token" , use_context=True)
bot= Bot(token="token")

#interduce the dispatcher made by updater locally for quicker access
dispatcher = updater.dispatcher

#do basic configration for logging system
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#A context manager that copies and restores the warnings filter upon exiting the context.
warnings.catch_warnings()

#ignore the warnings
warnings.simplefilter("ignore")


#List of bot's functionalities
bot_funcs = ['MeMe','Joke', 'Fun Facts', 'Research', 'Spotify Downloader' , 'YouTube Downloader ' , "Help Me To Get Better" , "Help"]



#_________________________________[/start]___________________________________#

# /start funcion --------
def start(update : Update,context:CallbackContext) -> None:
    #get users first name
    user_first_name = bot.get_chat(update.effective_chat.id).first_name

    # list of start menu's buttons
    start_menu_buttons_list = []

    # a loop which create a button for each of bot's functionalities
    for each in bot_funcs:
        start_menu_buttons_list.append(InlineKeyboardButton(each, callback_data = each.replace(" ","") ))
  
    #it'll show the buttons on the screen 
    reply_markup=InlineKeyboardMarkup(build_menu(start_menu_buttons_list, n_cols=1 )) 

    #button's explanaions 
    update.message.reply_text(
        f"Hello {user_first_name}❤️\nLet's have fun together 🙃\nhelp me to make you smile by pressing buttons below ... ",
        reply_markup=reply_markup
    )
    return CLICKBTTON
    

# make columns based on how we declared 
def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    start_menu_buttons = [buttons[i:i + n_cols] for i in range(0 , len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return start_menu_buttons

"""
# Handle telegram commands 
start_command = CommandHandler("start" , start)

#register a handler
dispatcher.add_handler(start_command)
"""
#_________________________________[/help]___________________________________#

# /help funcion --------
def help (update,context):  
    bot.send_message( 
        chat_id=update.effective_chat.id ,
        text = f"I'm Here to help you 🤓\nHere is the list of my current command :\n\n\n /MeMe 😜\n\n/Joke 🤣\n\n/FunFacts 🙈\n\n/Research 🧑‍🏫\n\n/SpotifyDownloader 🎷\n\n/YouTubeDownloader 🎬\n\n/HelpMeToGetBetter 🤖")
# handle help command    
help_command = CommandHandler("help" , help)
# register command 
dispatcher.add_handler(help_command)


#____________________________ Queries ______________________________#

#when we click on buttons .....
def Click_Button(update, context):
    query = update.callback_query
    if query.data == "MeMe":
        MeMe(update,context)
    if query.data == "Joke":
        Joke(update,context)
    if query.data == "Research":
        bot.send_message(chat_id=update.effective_chat.id ,text='What do you want to know about ? 🔎\n try to be accurate with the keyword to get the best result 🤓\n\n (Type a keyword not an emoji , file or etc ... ) ')
        return ABOUT
   # return query.data

"""
#handle call back queries
query_handler = CallbackQueryHandler(Click_Button)
#register call back query handler
dispatcher.add_handler(query_handler)
"""
#______________________________[/MeMe]___________________________________#

#sends random MeMe...
def  MeMe(update,context):
    #MeMe API ...
    Meme_Link = url =requests.get("https://meme-api.herokuapp.com/gimme")
    Meme_Information = Meme_Link.json()
    #get meme link 
    Meme_URL = Meme_Information['url']
    #send Meme
    bot.send_photo(chat_id=update.effective_chat.id , photo = Meme_URL , caption = "I hope you like it ❣️\nIf you want to see more : /MeMe")

#handle /MeMe command
MeMe_sender=CommandHandler("MeMe" , MeMe)
#register command
dispatcher.add_handler(MeMe_sender)


#______________________________[/Joke]___________________________________#
def Joke(update,context):
    #Joke API 
    Joke_link = requests.get("https://api.chucknorris.io/jokes/random")
    #json encoded of the link
    Joke_information = Joke_link.json()
    #joke 
    Joke = Joke_information["value"]
    #send the joke 
    bot.send_message(chat_id=update.effective_chat.id , text = f"{Joke}😝 \n\n for more /Joke 😉")



# Handle /Joke command 
joke_command=CommandHandler("Joke" , Joke)
#register command
dispatcher.add_handler(joke_command)      




#_______________________________________[/Research]_______________________________#

#This function get the title and try to give a summary from wikipedia

def about(update:Update,context:CallbackContext) -> int:
    #it'll put your requested subjct in var keyword
    KeyWord=str(update.message.text).title()
    #try to give a summary about your requested subject
    try:
        page = wikipedia.page(KeyWord)
        if str(page.title) != KeyWord:
            bot.send_message(chat_id=update.effective_chat.id,text=f"Didn't find any page with title {KeyWord} but there was a page with a near title {page.title}")
            summary=page.summary
            bot.send_message(chat_id=update.effective_chat.id,text=summary)
        else:
            summary=page.summary
            bot.send_message(chat_id=update.effective_chat.id,text=summary)
        return quit(update,context)
    #if there was more than 1 available result it'll show the options     
    except wikipedia.exceptions.DisambiguationError as e :
        try:
            bot.send_sticker(chat_id=update.effective_chat.id , sticker="CAACAgQAAxkBAAIDd2BIhkzUFjO0luK9zWEMyxOThjTiAAIqAANFP9ECqTgcnm8ht2EeBA" )
            bot.send_message(chat_id=update.effective_chat.id,text=f"Oooops sorry !\ncan't find anything about Your requested subject....\nBut there are some close results :\n\n {e.options[0]}\n {e.options[1]}\n {e.options[2]}\n {e.options[3]}\n {e.options[4]}\n\n if you found your requested result feel free to use command : /Research again ...")
            return quit(update,context)
        except wikipedia.WikipediaException :
            bot.send_sticker(chat_id=update.effective_chat.id , sticker="CAACAgIAAxkBAAIDwGBIp9GCzWMeB5Cf6mv-ZQNlXXl5AAJyAAPBnGAM6XzSB3m7cZseBA" )
            bot.send_message(chat_id=update.effective_chat.id,text=f"Ooooops Sorry ! Something Went Wrong ... ")
            return quit(update,context)
    #if page didn't exist ...
    except wikipedia.exceptions.PageError :
        bot.send_sticker(chat_id=update.effective_chat.id , sticker="CAACAgIAAxkBAAIDqGBIpWgtpTcPkmqGAAHSA52aQfqjjgACcwADwZxgDAsjEJD-pZcnHgQ" )
        bot.send_message(chat_id=update.effective_chat.id,text=f"Ooooops Sorry ! There is no page with title : {KeyWord} ")
        return quit(update,context)
    #any other error ...
    except Exception:
        bot.send_sticker(chat_id=update.effective_chat.id , sticker = "CAACAgIAAxkBAAIDwGBIp9GCzWMeB5Cf6mv-ZQNlXXl5AAJyAAPBnGAM6XzSB3m7cZseBA")
        bot.send_message(chat_id=update.effective_chat.id,text=f"Ooooops Sorry! Something Went Wrong ... ")
        return quit(update,context)


#send a message and return the about function 
def ask_wikipedia(update: Update, context: CallbackContext) -> int :
    bot.send_message(chat_id=update.effective_chat.id ,text='What do you want to know about ? 🔎\n try to be accurate with the keyword to get the best result 🤓\n\n (Type a keyword not an emoji , file or etc ... ) ')
    return ABOUT

def quit(update, context):
    return ConversationHandler.END


CLICKBTTON,ABOUT = 0 , 1 

handle_converstation_using_command=ConversationHandler(
    entry_points=[CommandHandler('Research', ask_wikipedia)],
    states={
        ABOUT: [MessageHandler(Filters.text, callback=about)]
    },
    fallbacks=[CommandHandler('quit', quit)])

dispatcher.add_handler(handle_converstation_using_command)



handle_converstation_using_Button=ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CLICKBTTON: [CallbackQueryHandler(Click_Button)],
        ABOUT: [MessageHandler(Filters.text, callback=about)]

    },
    fallbacks=[CommandHandler('quit', quit)])

dispatcher.add_handler(handle_converstation_using_Button)


#__________________________________[/YouTubeDownloader]____________________________#

#This function ask for the link of the video and return the download function


def ask_for_link(update,context):
    bot.send_message(chat_id=update.effective_chat.id ,text="Please Paste the video link here ... ")
    return DOWNLOADER

def Downloader(update,context):
    
    
    try:
        link=str(update.message.text)
        context.user_data['link'] = link
        
         
        Video_Url = YouTube(link)
        Video= Video_Url.streams
        chooseRes = []
        for i in Video :
            chooseRes.append([str(i).split()[2][str(i).split()[2].index("=")+2:len(str(i).split()[2])-1] , str(i).split()[3][str(i).split()[3].index("=")+2:len(str(i).split()[3])-1]])
        print(chooseRes)
        
        # list of resolution menu's buttons
        res_menu_buttons_list = []

         # a loop which create a button for each of bot's functionalities
        for each in chooseRes:
            res_menu_buttons_list.append(InlineKeyboardButton(f"{each[0]}  ❤️  {each[1]}", callback_data = each[1] ))
       # print(res_menu_buttons_list)
    
        #it'll show the buttons on the screen 
        replyMarkup=InlineKeyboardMarkup(build_res_menu(res_menu_buttons_list, n_cols=2 )) 
        #button's explanaions 
        update.message.reply_text("Choose an Option from the menu below ... ",reply_markup=replyMarkup)
        return CLICK_FORMAT
        
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.effective_chat.id , text = "Oooops !!! Something Went Wrong ... \n\n ( Make sure that you wrote the link correctly )")
        quit(update,context)


# make columns based on how we declared 
def build_res_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    res_menu_buttons = [buttons[i:i + n_cols] for i in range(0 , len(buttons), n_cols)]
    if header_buttons:
        res_menu_buttons.insert(0, header_buttons)
    if footer_buttons:
        res_menu_buttons.append(footer_buttons)
    return res_menu_buttons

       # print(link)
       

def click_format(update,context):
        query = update.callback_query.data
        link = context.user_data['link']
        print(link,query)
        Video_Url= YouTube(link)
        
        Video = Video_Url.streams.filter(res=query).first()
        Video.download()
        

        format_vid=re.sub(Video.mime_type[:Video.mime_type.index("/")+1],"",Video.mime_type)  
        bot.send_message(chat_id=update.effective_chat.id , text = f"{Video.title} has Downloaded successfully ... ")
        bot.send_video(chat_id=update.effective_chat.id ,video=open(f"{Video.title}.{format_vid}" , 'rb'), supports_streaming=True)
      
        try:
            os.remove(f"{Video.title}.{format_vid}")
            print("removed")
        except:
            print("Can't remove")
            quit(update,context)
    
DOWNLOADER , CLICK_FORMAT = 0 ,1

YouTube_Downloader_converstation_handler=ConversationHandler(
    entry_points=[CommandHandler("YouTubeDownloader", ask_for_link)] , 
    states={
        DOWNLOADER :[MessageHandler(Filters.text , callback=Downloader )],
        CLICK_FORMAT : [CallbackQueryHandler(click_format)]
          
        },
    fallbacks=[CommandHandler("quit" , quit)]) 

dispatcher.add_handler(YouTube_Downloader_converstation_handler)






#start the bot
updater.start_polling()

# starting info 
logging.info("Bot is awake .... ")

#stop the bot with ctrl+C
updater.idle()
