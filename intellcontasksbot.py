import telebot
import xml.dom.minidom
import pymysql
import os

bot = telebot.TeleBot("1458051153:AAGMyRA9ZC8iBDovsY7__ce5AhSiiaRHz3U")
fileName = ''
projectName = ''
admin = ''
con = pymysql.connect('localhost', 'root', '207546Str', 'intellcontasksbot')
cur = con.cursor()
cur.execute("SELECT * FROM users WHERE userLogin='intellcon'")
rows = cur.fetchall()
for row in rows:
    if row[1] == 'intellcon':
        admin = row[2]
        print(admin)
con.close()

getFileFlag = False

# реагирование на запросы пользователей
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global getFileFlag
    if message.text.lower() == "/start":
        con = pymysql.connect('localhost', 'root', '207546Str', 'intellcontasksbot')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE userTelId=" + str(message.from_user.id))
        rows = cur.fetchall()
        cur.close()
        for row in rows:
            bot.send_message(message.from_user.id, "Привет, " + row[1])

    if message.text.lower() == "новый проект":
        f = open("./template.xml", "rb")
        bot.send_document(message.chat.id, f)
        # нужно еще подумать над несколькими стандартными шаблонами на мебель и проектированием
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "и тебе привет")
    if message.text.lower() == "мой id":
        bot.send_message(message.from_user.id, message.from_user.id)
    if (message.text.lower() == "загрузка проекта") | (message.text.lower() == "загрузить проект"):
        if str(message.from_user.id) == admin:
            bot.send_message(message.from_user.id, 'Загрузите файл проекта')
            getFileFlag = True
            bot.register_next_step_handler(message, get_project)
    if (message.text.lower() == "обновление проекта") | (message.text.lower() == "обновить проект"):
        if str(message.from_user.id) == admin:
            bot.send_message(message.from_user.id, 'Загрузите файл проекта')
            getFileFlag = True
            bot.register_next_step_handler(message, update_project)
def get_project_name(message):
    global projectName
    global fileName
    projectName = message.text
    con = pymysql.connect('localhost', 'root', '207546Str', 'intellcontasksbot')
    cur = con.cursor()
    sql = "INSERT INTO projects (`projectName`, `projectFile`) VALUES ('" + projectName + "', '" + fileName + "')"
    print(sql)
    cur.execute(sql)
    con.commit()
    con.close()
    bot.send_message(message.from_user.id, 'Проект успешно добавлен');

@bot.message_handler(content_types=['document'])
def update_project(message):
    global getFileFlag
    global fileName
    print(getFileFlag)
    if getFileFlag == True:
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = './projects/' + message.document.file_name;
        # открываем файл для записи
        with open(src, 'wb') as new_file:
            # записываем данные в файл
            new_file.write(downloaded_file)
            new_file.close()
        getFileFlag = False
    else:
        bot.send_message(message.from_user.id, 'Что вы хотите сделать?')
def get_project(message):
    global getFileFlag
    global fileName
    print(getFileFlag)
    if getFileFlag == True:
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = './projects/' + message.document.file_name;

        # открываем файл для записи
        with open(src, 'wb') as new_file:
            # записываем данные в файл
            new_file.write(downloaded_file)
            new_file.close()
        getFileFlag = False
        fileName = message.document.file_name
        bot.send_message(message.from_user.id, 'Введите наименование проекта')
        bot.register_next_step_handler(message, get_project_name)
        
    else:
        bot.send_message(message.from_user.id, 'Что вы хотите сделать?')
#-----------------------------------------------------------------

bot.polling(none_stop=True, interval=0)