import telepot
from telepot.loop import MessageLoop
from time import sleep
import sqlite3 as db
import random


token = '500572767:AAFy7YAizO6zJMNCUL8lsI0fNX-j2n2_Bn0'
bot = telepot.Bot(token)

def user_token():
    charachters = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    token_length = 5

    token_of_user = ''.join(random.sample(charachters, token_length))

    return token_of_user


def handle(msg):
    cmd = msg['text']
    chatid = msg['chat']['id']
    username = msg['chat']['username']

    invitedurl = "t.me/linychargerbot?start={}".format(chatid)
    peopleinvited = 0


    is_invite = True
    start = list()
    if cmd.startswith('/start'):

        command = cmd.split(' ')
        print(command)

        if len(command) > 1:
            is_invite = True
            start.append(int(command[1]))
            print(len(start))
            bot.sendMessage(chatid,"به ربات عضوبگیر شارژ بده خوش اومدی\nشما توسط {} دعوت شده‌اید\nبرای اینکه بتونی دوستات رو بتونی به این ربات دعوت کنی اول باید در سیستم ما ثبت بشی\n/register\nو بعد از اون از دستور /link استفاده کن".format(start))
        else:
            is_invite = False
            bot.sendMessage(chatid, "به ربات عضوبگیر شارژ بده خوش اومدی\nبرای اینکه بتونی دوستات رو بتونی به این ربات دعوت کنی اول باید در سیستم ما ثبت بشی\n/register\nو بعد از اون از دستور /link استفاده کن")
        print(is_invite)

    if cmd == '/link':
        con = db.connect('charger.db')
        cur = con.cursor()
        cur.execute("select chatid from users where chatid = {}".format(chatid))
        status = cur.fetchall()
        if len(status) > 0:
            user = bot.getChatMember("@testcharger", chatid)
            user_status = ['restricted', 'left', 'kicked']
            condition = True

            for us in user_status:
                condition = user['status'] == us
                if condition is True:
                    break
            if condition:
                bot.sendMessage(chatid, "شما عضو کانال @testcharger نیستید\nبعد از اینکه در کانال ما عضو شدی دوباره دستور /link رو وارد کن")
            else:
                bot.sendMessage(chatid, "لینک دعوت شما: {}".format(invitedurl))
                if is_invite:
                    print(len(start))
                    user_inviter_id = start
                    print(user_inviter_id)
                    if len(start) > 0:
                        cur.execute('select peopleinvited from users where chatid = {}'.format(user_inviter_id))
                        people = cur.fetchone()
                        print(people)
                        number_people = people[0] + 1
                        print(number_people)
                        cur.execute("update users set peopleinvited = {} where chatid  = {}".format(number_people,user_inviter_id))
                        con.commit()
                        cur.execute('select peopleinvited from users where chatid = {}'.format(user_inviter_id))
                        is_five = cur.fetchone()
                        if is_five[0] % 5 == 0:
                            token_of_user = user_token()
                            bot.sendMessage(start,"تعداد افراد دعوت شده شما به ۵ نفر رسید\nکد تایید اعتبار شما: {} است\nلطفا این کد را به @liniolon پیام دهید تا بعد از بررسی های لازم شارژ خود را دریافت کنید".format(token_of_user))
                            cur.execute("insert into token (token, chatid) values ('{}', {})".format(token_of_user, start))
                            con.commit()
                        else:
                            bot.sendMessage(start, "تعداد نفرات دعوت شما : {}".format(is_five))

                        con.close()
                    else:
                        pass

                else:
                    pass
        else:
            bot.sendMessage(chatid, "شما در سیستم ما ثبت نشده‌اید برای دریافت لینک اختصاصی خود دستور /register را وارد کنید")
        con.close()

    if cmd == '/register':
        con = db.connect('charger.db')
        cur = con.cursor()
        cur.execute("select chatid from users where chatid = {}".format(chatid))
        check_registration = cur.fetchone()
        if len(check_registration) > 0:
            bot.sendMessage(chatid, "شما قبلا در سیستم ما ثبت شده‌اید، نباز به ثبت نام مجدد ندارید\nلینک دعوت شما: {}".format(invitedurl))
        else:
            cur.execute("insert into users (username, chatid, inviteurl, peopleinvited) values ('{}', {}, '{}', '{}')".format(username, chatid, invitedurl, peopleinvited))
            con.commit()
            con.close()
            bot.sendMessage(chatid,"شما با موفقیت در سیستم ما ثبت شدید\nحالا دستور /link را جهت دریافت لینک دعوت اختصاصی خود وارد کنید")


MessageLoop(bot, handle).run_as_thread()
print("Listeing ...")

while 1:
    sleep(10)