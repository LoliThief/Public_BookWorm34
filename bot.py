#Standart libraries
import os
from random import choice

#Our files
import Base
import Data
from config import TOKEN
import GoogleSheetExtracter
import pdfreader

# PIP libraries
import telebot

owner_id = 713697602
save_pdf = False
number_of_books = 10
fast_mode = False
send_actions = False

bot = telebot.TeleBot(TOKEN)

skills = []

def is_admin(username):
    for admin in Data.super_usernames:
        if(username == admin):
            return True
    return False

def f(message, num=10):
    a = 1; b = 1
    if(num > 25):
        bot.send_message(message.chat.id, f'<b> arg is too big : (, enjoy first 50!'f' </b>', parse_mode="html")
    for i in range(min(num, 50)):
        bot.send_message(message.chat.id, f'<b> {a} </b>', parse_mode="html")
        c = a + b; a = b; b = c

@bot.message_handler(commands=['start', 'f', 'help', 'gt', 'set', 'ping', 'my_id', 'joke', 'report_sample'])
def start(message):
    mtext = message.text.split()

    print(f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Asked me for {mtext[0]}!")

    global send_actions
    if(send_actions == True):
        bot.send_message(owner_id, f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Asked me for {mtext[0]}!")

    if (mtext[0] == '/f'):
        try:
            f(message, int(mtext[1]))
        except:
            f(message, 15)
    if (mtext[0] == "/start"):
        buttons = telebot.types.InlineKeyboardMarkup()
        #btn0 = telebot.types.InlineKeyboardButton(text='Our Documentation', url='https://bit.ly/Infomatrix2022BookWorm34_doc')
        btn0 = telebot.types.InlineKeyboardButton(text='→ You can find out more about  CliftonStrength34 here ←', url='https://www.gallup.com/cliftonstrengths/en/253715/34-cliftonstrengths-themes.aspx')
        buttons.add(btn0)
        bot.send_message(message.chat.id, Data.Welcome_message, reply_markup=buttons)
    if (mtext[0] == "/my_id"):
        bot.send_message(message.chat.id, message.chat.id)

    if (mtext[0] == "/report_sample"):
        with open("sample.pdf", 'rb') as report_sample:
            bot.send_document(message.chat.id, report_sample)

    if (mtext[0] == "/help"):
        buttons = telebot.types.InlineKeyboardMarkup()
        #btn0 = telebot.types.InlineKeyboardButton(text='Our Documentation', url='https://bit.ly/Infomatrix2022BookWorm34_doc')
        btn0 = telebot.types.InlineKeyboardButton(text='→ You can find out more about  CliftonStrength34 here ←', url='https://www.gallup.com/cliftonstrengths/en/253715/34-cliftonstrengths-themes.aspx')
        buttons.add(btn0)
        joke = ""

        if(len(mtext) >= 2):
            if(mtext[1] == '-c' or mtext[1] == '--commands' or mtext[1] == '-a' or mtext[1] == '--all'):
                joke = "\n\nAdditional commands:\n/f - Fibonacci numbers[1; 50]\n/my_id - sends user id\n/ping - average ping\n/joke - coolest joke in the whole world!"
        bot.send_message(message.chat.id, Data.Help_message + joke, reply_markup=buttons)

    if (mtext[0] == "/ping"):
        bot.reply_to(message, "pong")
    if (mtext[0] == "/joke"):
        buttons = telebot.types.InlineKeyboardMarkup()
        btn0 = telebot.types.InlineKeyboardButton(text='Click here!', url='https://bit.ly/moralnight1705')
        buttons.add(btn0)
        bot.send_message(message.chat.id, "The joke", reply_markup=buttons)
    try:
        if (mtext[0] == '/set'):
            if (is_admin(message.chat.username) == False):
                bot.send_message(message.chat.id, 'Access Denied')
            elif (mtext[1] == 'save_pdf'):
                try:
                    global save_pdf
                    save_pdf = bool(int(mtext[2]))
                except:
                    save_pdf = False
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {save_pdf}')
            elif (mtext[1] == 'fast_mode'):
                try:
                    global fast_mode
                    fast_mode = bool(int(mtext[2]))
                except:
                    fast_mode = False
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {fast_mode}')
            elif (mtext[1] == 'number_of_books'):
                try:
                    global number_of_books
                    number_of_books = int(mtext[2])
                except:
                    number_of_books = 10
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {number_of_books}')
            elif (mtext[1] == 'send_actions'):
                try:
                    send_actions = bool(int(mtext[2]))
                except:
                    send_actions = False
                else:
                    bot.send_message(message.chat.id, f'Значение {mtext[1]}, успешно изменено на {send_actions}')
            elif (mtext[1] == '--help' or mtext[1] == '-h'):
                bot.send_message(message.chat.id, 'Parameters of "/set" \nsave_pdf\t[1, 0]\nnumber_of_books\t[0, 100]\nfast_mode\t[1, 0]\nsend_actions\t[1, 0]\n')
            else:
                bot.send_message(message.chat.id, 'unknown parameter of "/set, try --help" ')
    except:
        bot.send_message(message.chat.id, "Invalid syntax of /set, try --help")
    try:
        if (mtext[0] == "/gt"):
            bot.send_message(message.chat.id, GoogleSheetExtracter.get_value(int(mtext[1]), int(mtext[2])))
    except:
        bot.send_message(message.chat.id, "You are out of range")


@bot.message_handler(content_types=['document'])
def handle_files(message):
    # try:
    chat_id = message.chat.id

    print(message.chat.username, "Sended me file")

    global send_actions
    if (send_actions == True):
        bot.send_message(owner_id, f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Sended me file!")

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # src = 'C:/Users/пользователь/PycharmProjects/jhkhklj/' + message.document.file_name
    src = message.document.file_name

    nfile = message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    inf = pdfreader.take_info_from_pdf(nfile)
    # inf[0] => skills list or PDF error report
    # inf[1] => User's name from CS34 report or details of the error

    if(inf[0] == "invalid PDF"):
        bot.reply_to(message, "Sent PDF file are invalid: ")#"Расходимся пацаны c PDF файлом что то не то!"
        if(inf[1] == "unknown file type"):
            bot.reply_to(message, "Unknown file type, did you send the PDF file?")#"что с файлом? Это точно PDF?"
        elif(inf[1] == "unknown symbols"):
            bot.reply_to(message, "File contains unreadable characters, check whether the file is a CliftonStrength34 report.")#"что с файлом? В нем или в его названии странные символы это точно GALLUP?"
        elif (inf[1] == "unreadable"):
            bot.reply_to(message, "Unreadable file, is it a CliftonStrength34 report?")#ошибка которая не должна выпадать по идее
        else:# (inf[1] == "skills_error" or inf[1] == "not_a_GALLUP"):
            bot.reply_to(message, "This file is not a CliftonStrength34 report!")
        try:
            os.remove(nfile)
            os.remove("first_page.pdf")
        except:
            pass
        return

    skills = inf[0]

    if(save_pdf == True):
        with open(nfile, "rb") as pdf_file:
            bot.send_document(owner_id, pdf_file, f"User with ID:{message.chat.id}, and username: @{message.chat.username}. Sended this file!")

    resp = ""
    cnt = 1
    for i in skills:
        resp += (str(cnt) + ". " + i + "\n")
        cnt += 1

    ans = Base.get_books(nfile, skills)
    cnt = 1

    bot.reply_to(message, f"Here are a couple of books,  picked for {inf[1]}, that will be useful or interesting to you.")

    for i in ans:
        #message2 += (str(cnt + 1) + ") " + i.author + ": " + i.title + "\t" + str(i.rating) + "\n")

        buttons = telebot.types.InlineKeyboardMarkup()
        if(i.link != "no_link"):
            btn = telebot.types.InlineKeyboardButton(text='More about this book', url=i.link)
            buttons.add(btn)

        m_text = (str(cnt) + ") " + i.author + ": \n" + i.title + "\n")

        try:
            if(fast_mode == True):
                asdfdsa += "sadf"
            try:
                image = open(f"images/{i.title}.jpg", "rb")
            except:
                image = open(f"images/{i.title}.png", "rb")
            finally:
                bot.send_photo(message.chat.id, image, m_text, reply_markup=buttons)
        except:
            bot.send_message(message.chat.id, m_text, reply_markup=buttons)

        #message2 += (str(cnt + 1) + ") " + i.author + ": " + i.title + "\n")
        global number_of_books
        if (cnt == number_of_books):
            break
        cnt += 1
    #bot.send_message(message.chat.id, "asdf")


    buttons = telebot.types.InlineKeyboardMarkup()
    btn0 = telebot.types.InlineKeyboardButton(text='Bookworm34 feedback form', url='https://forms.gle/VgmfvNHq9ekeZpxB8')
    buttons.add(btn0)
    bot.send_message(message.chat.id, "Once you have read one of the books, you can leave a feedback here. This will help us improve our bot", reply_markup=buttons)


    try:
        os.remove(nfile)
        os.remove("first_page.pdf")
    except:
        pass
    nfile = ""

    """
    except Exception as e:
        bot.reply_to(message, e)
        o.remove(nfile)
        #s.remove("first_page.pdf")
        nfile = ""
    """


@bot.message_handler()
def sft(message):
    print(f"User's ID:{message.chat.id}, and username: @{message.chat.username} sended me just text!")

    global send_actions
    if (send_actions == True):
        bot.send_message(owner_id,
            f'User with ID:{message.chat.id}, and username: @{message.chat.username}. sended me "{message.text}"')

    if (message.chat.username == 'zxc_L1za'):
        bot.send_message(message.chat.id, f"{choice(Data.salemdesu)} Master <3")
    elif (message.chat.username == 'AmirKunuspekov'):
        bot.send_message(message.chat.id, f"{choice(Data.salemdesu)} Amir san : )")
    else:
        bot.send_message(message.chat.id, f"{choice(Data.salemdesu)}. \nAre you new here? try /help")

    """
    https://bit.ly/Infomatrix2022BookWorm34_doc
    buttons = telebot.types.InlineKeyboardMarkup()
    btn0 = telebot.types.InlineKeyboardButton(text='Харкач', url='https://2ch.hk')
    btn1 = telebot.types.InlineKeyboardButton(text='CF', url='https://codeforces.com')
    buttons.add(btn0)
    buttons.add(btn1)
    image = open("images/testt2.jpg", "rb")
    bot.send_photo(message.chat.id, image,"какой то  текст для теста" , reply_markup=buttons)
    """

GoogleSheetExtracter.initiate()
print("GoogleShit Database Ready!")

bot.polling(none_stop=True)