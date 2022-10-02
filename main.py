# -*- coding: utf-8 -*-

import mechanize
import bs4
import telebot
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я можу надіслати тобі розклад занять Волинського національного університету імені Лесі Українки.\nПросто напишіть назву своєї групи нижче👇")

@bot.message_handler(content_types=["text"])
def text(message):

    browser = mechanize.Browser()
    browser.open(URL)

    browser.select_form(name="setVedP")
    browser["group"] = message.text
    response = browser.submit()

    html_raw = response.read().decode(DECODE_TYPE)

    soup = bs4.BeautifulSoup(html_raw, "lxml")
    if soup.find("div", {"class": "alert alert-info"}):
        bot.send_message(message.chat.id, "За вашим запитом записів не знайдено")
    else:
        nl = "\n"
        h4 = soup.find("h4", {"class": "hidden-xs"})
        rows = soup.find_all("div", {"class": "col-md-6"})
        msg = f"<b>{h4.text}</b>{nl}"
        for row in rows:
            if not row.h4 is None:
                data = []
                table = row.find("table")
                trows = table.find_all('tr')
                for trow in trows:
                    cols = trow.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])
                for nd, d in enumerate(data):
                    d[0] += "."
                    d[1] = d[1][:5] + " - " + d[1][5:]
                    data[nd][0] = d[0]
                    data[nd][1] = d[1]

                msg = f"{msg}{nl}<b>{row.h4.text}</b>{nl}{nl}{nl.join([' '.join(d) for d in data])}{nl}"
        bot.send_message(message.chat.id, msg, parse_mode="html")

bot.infinity_polling()