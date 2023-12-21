import telebot
from extensions import Exchanger, ExchangerException
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def introduction(message: telebot.types.Message):
    text = 'Конвертер валют\nЧтобы начать работу, введите в следующем формате:\n\
<имя валюты> <в какую валюту> <количество валюты>\nПосмотреть список валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def exchanger(message: telebot.types.Message):
    try:
        value = message.text.split(' ')
        if len(value) != 3:
            raise ExchangerException('Неправильное количество параметров')
        quote, base, amount = value
        total_value = Exchanger.get_price(quote, base, amount)
    except ExchangerException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote.lower()}: {total_value} {base.lower()}'
        bot.send_message(message.chat.id, text)


bot.polling()
