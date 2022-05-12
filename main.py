import telebot
from telebot import types
import psycopg2
import datetime
token="5133274591:AAEwjRLxRHZqOsCoCTc1jcAosO6K5Dod2UE"
bot = telebot.TeleBot(token)
conn=psycopg2.connect(database="service_db",
                      user="postgres",
                      password="12345",
                      host="localhost",
                      port="5432")
cursor=conn.cursor()        
@bot.message_handler(commands=['start'])
def start(message):
    keyboard=types.ReplyKeyboardMarkup(True,False)
    keyboard.add ("Понедельник","Вторник","Среда","Четверг","Пятница","На текущую неделю","На следующую неделю","/week","/server","/help")
    bot.send_message(message.chat.id,' Привет! Хотите узнать расписание?', reply_markup=keyboard)

def repeat(message):
    keyboard=types.ReplyKeyboardMarkup(True,False)
    keyboard.add ("Понедельник","Вторник","Среда","Четверг","Пятница","На текущую неделю","На следующую неделю","/week","/server","/help")
    bot.send_message(message.chat.id,' Что-то еще?', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,' Я умею писать расписание')

@bot.message_handler(commands=['week'])
def week(message):
    num=int(datetime.datetime.now().strftime("%V"))
    if num%2==0:
        bot.send_message(message.chat.id,'Сейчас неделя чётная')
    else:
        bot.send_message(message.chat.id,'Сейчас неделя нечётная')

@bot.message_handler(commands=['server'])
def server(message):
    bot.send_message(message.chat.id,' Вам сюда http://server.odessa.ua/raspisanie-zanyatij/')
   
def print__(records,message):  
    day=""
    for i in range(len(records)):
        if day != records[i][4]:
            bot.send_message(message.chat.id,' {}'.format(records[i][4]))
            bot.send_message(message.chat.id,' ___________')
            day=records[i][4]
        bot.send_message(message.chat.id," <{}><{}><{}><{}>".format(records[i][7],records[i][2],records[i][3],records[i][9]))
def get(day,num):
    if day !="":
        cursor.execute("""select DISTINCT  * from service.timetable inner join service.subject on service.timetable.subject_id
    = service.subject.id inner join service.teacher on service.subject.id = service.teacher.subject_id  where day = '{}'
    and chet = '{}' order by start_time""".format(day,num%2==0))
        return list(cursor.fetchall())
    else:
        cursor.execute("""select DISTINCT  *,CASE WHEN day ='Понедельник' THEN 1 WHEN day ='Вторник' THEN 2
WHEN day ='Среда' THEN 3 WHEN day ='Четверг' THEN 4 WHEN day ='Пятница' THEN 5 ELSE 0 END AS n_day from service.timetable
inner join service.subject on service.timetable.subject_id= service.subject.id inner join service.teacher on service.subject.id
= service.teacher.subject_id  where chet = '{}' order by n_day,start_time""".format(num%2==0))
        return list(cursor.fetchall())
        
@bot.message_handler(content_types=['text'])
def answer(message):
    num=int(datetime.datetime.now().strftime("%V"))    
    if message.text.lower()=="понедельник":
        print__(get("Понедельник",num),message)
    elif message.text.lower()=="вторник":
        print__(get("Вторник",num),message)
    elif message.text.lower()=="среда":
        print__(get("Среда",num),message)
    elif message.text.lower()=="четверг":
        print__(get("Четверг",num),message)
    elif message.text.lower()=="вторник":
        print__(get("Вторник",num),message)
    elif message.text.lower()=="среда":
        print__(get("Среда",num),message)
    elif message.text.lower()=="четверг":
        print__(get("Четверг",num),message)
    elif message.text.lower()=="пятница":
        print__(get("Пятница",num),message)
    elif message.text.lower()=="на текущую неделю":
        bot.send_message(message.chat.id,' На текущую неделю')
        print__(get("",num),message)
    elif message.text.lower()=="на следующую неделю":
        bot.send_message(message.chat.id,' На следующую неделю')
        print__(get("",num+1),message)
    else:
        bot.send_message(message.chat.id,' Я вас не понял')
    repeat(message)
bot.infinity_polling()
