from consts import TOKEN

import telebot

bot = telebot.TeleBot(TOKEN)

class group():
	def __init__(self, c_id):
		self.asker = None
		self.asked_word = None
		self.game_in_process = False
		self.game_iniciator = None
		self.chat_id = c_id
		self.to_end = 0
		self.leaderboard = {}
		self.voted = []


groups = {'-1001445415331':group('-1001445415331'),'-1001321532314':group('-1001321532314')}
questions = {}
ch = False


@bot.message_handler(commands=['init'], func=lambda message: not(str(message.chat.id) in groups))
def echo_all(message):
	chat_id = str(message.chat.id)
	groups.update({str(chat_id):group(str(chat_id))})
	bot.reply_to(message, "ПоЛуЧиЛоСь!")
	print(groups)
	ch = True



@bot.message_handler(commands=['start'], func=lambda message: message.chat.type == "private")
def oncommand(message):
	chat_id = message.text[7::]
	questions.update({message.from_user.id: chat_id})

@bot.message_handler(commands=['game'], func=lambda message: message.chat.type == "group" or message.chat.type == "supergroup")
def command_help(message):
	if str(message.chat.id) not in groups:
		groups.update({str(message.chat.id):group(str(message.chat.id))})
	markup = telebot.types.InlineKeyboardMarkup()
	itembtn = telebot.types.InlineKeyboardButton('Начать игру', callback_data=str(message.chat.id))
	markup.row(itembtn)
	bot.reply_to(message, "аооаоаоаоаа 🤧\nчтобы начать игру, нажми на кнопку и вВеДи ЗаГаДаНнОе СлОвО:", reply_markup=markup)

@bot.callback_query_handler(lambda query: True)
def process_callback_1(query):
	chat_id = query.data
	user_id = query.from_user.id
	if not(groups[chat_id].asker):
		bot.answer_callback_query(query.id, text="ТаК тОчНо", show_alert=True, url=f"t.me/dzhanki_bot?start={str(chat_id)}")
	else:
		bot.answer_callback_query(query.id, text="СлОвО уЖе ЗаГаДаНо 👺👺👺👺👺👺", show_alert=True)

@bot.message_handler(func=(lambda message: message.chat.type == "private" and message.from_user.id in questions))
def echo_all(message):
	if " " in message.text:
		bot.reply_to(message, "ОдНо СлОвО!!👺👺👺\nДавай еще раз!")
	else:
		if not(message.from_user.id in questions):
			bot.reply_to(message, "Ты Не нАчАл ИгРу!")
		else:
			groups[questions[message.from_user.id]].asked_word = message.text.lower()
			groups[questions[message.from_user.id]].asker = message.from_user.id
			groups[questions[message.from_user.id]].game_in_process = True
			groups[questions[message.from_user.id]].game_iniciator = message.from_user.first_name
			chat = groups[questions[message.from_user.id]]
			questions.clear()
			bot.reply_to(message, "ПрИнЯтО")
			bot.send_message(chat.chat_id, f'игра началась циу 🤙\n'+chat.game_iniciator+' загадал(а) слово из '+str(len(chat.asked_word))+' букв! 🥱\n'+('*')*len(chat.asked_word))
			print(str(chat.chat_id))

# @bot.message_handler(func=lambda message: True)
# def echo(message):
# 	chat_id = str(message.chat.id)
# 	groups.update({str(chat_id):group(str(chat_id))})


@bot.message_handler(func=lambda message: (message.chat.type == "group" or message.chat.type == "supergroup"))
def echo_to_message(message):
	print("there")
	if str(message.chat.id) not in groups:
		groups.update({str(message.chat.id):group(str(message.chat.id))})
	
	if (groups[str(message.chat.id)].game_in_process):
		chat = groups[str(message.chat.id)]
		if chat.asked_word in message.text.lower():
			if message.from_user.id == chat.asker:
				bot.reply_to(message, f"👺👺👺ЗаЧеМ пРоБоЛтАлСя?!?!?!👺👺👺\nТеперь никто ничего не получит, умник...\nСлово было: {chat.asked_word}...")
				groups[str(message.chat.id)].asked_word = None
				groups[str(message.chat.id)].game_in_process = False
				groups[str(message.chat.id)].game_iniciator = None
				groups[str(message.chat.id)].to_end = 0
				groups[str(message.chat.id)].asker = None
			else:
				bot.reply_to(message, f"{message.from_user.first_name} отгадал слово!!! горжусь тобой, умничка 🤧❤️\nТебе +1 балл.\nСлово было: {chat.asked_word}.")
				if str(message.from_user.first_name) in groups[str(message.chat.id)].leaderboard:
					pass
				else:
					groups[str(message.chat.id)].leaderboard.update({str(message.from_user.first_name):0})
				groups[str(message.chat.id)].leaderboard[str(message.from_user.first_name)] += 1
				groups[str(message.chat.id)].asked_word = None
				groups[str(message.chat.id)].game_in_process = False
				groups[str(message.chat.id)].game_iniciator = None
				groups[str(message.chat.id)].to_end = 0
				groups[str(message.chat.id)].asker = None
		if "/end" in message.text:
			if str(message.from_user.id) == str(groups[str(message.chat.id)].asker):
				
				
				bot.reply_to(message, f"ну вот... {groups[str(message.chat.id)].game_iniciator} остановил игру... 🥀🕯 здоровья погибшим 😔👍\nСлово было: {groups[str(message.chat.id)].asked_word}.")
				groups[str(message.chat.id)].asker = None
				groups[str(message.chat.id)].game_iniciator = None
				groups[str(message.chat.id)].asked_word = None
				groups[str(message.chat.id)].game_in_process = False
				
				groups[str(message.chat.id)].to_end = 0
			else:
				if str(message.from_user.id) in groups[str(message.chat.id)].voted:
					bot.reply_to(message, f"хорош пух на себя накидывать, голосовал уже 👺👺👺👺👺👺👺👺👺")
				else:
					groups[str(message.chat.id)].to_end += 1
					bot.reply_to(message, f"ты проголосовал за отмену игры( Осталось {str(3 - groups[str(message.chat.id)].to_end)}")
					groups[str(message.chat.id)].voted.append(str(message.from_user.id))
				
				if groups[str(message.chat.id)].to_end == 3:
					bot.reply_to(message, f"ну вот... игра остановлена... 🥀🕯\nСлово было: {groups[str(message.chat.id)].asked_word}.")
					groups[str(message.chat.id)].asked_word = None
					groups[str(message.chat.id)].game_in_process = False
					groups[str(message.chat.id)].game_iniciator = None
					groups[str(message.chat.id)].to_end = 0
					groups[str(message.chat.id)].asker = None
					groups[str(message.chat.id)].voted.clear()
	

		


@bot.message_handler(commands=['end'])
def answer_to_end(message):
	if str(message.chat.id) not in groups:
		groups.update({str(message.chat.id):group(str(message.chat.id))})
	if str(message.from_user.id) == groups[str(message.chat.id)].asker:
		groups[str(message.chat.id)].asked_word = None
		groups[str(message.chat.id)].game_in_process = False
		groups[str(message.chat.id)].game_iniciator = None
		groups[str(message.chat.id)].to_end = 0
		groups[str(message.chat.id)].asker = None
		bot.reply_to(message, f"ну вот... {groups[str(message.chat.id)].asker} остановил игру... 🥀🕯 здоровья погибшим 😔👍\nСлово было: {groups[str(message.chat.id)].asked_word}.")
	else:
		groups[str(message.chat.id)].to_end += 1
		bot.reply_to(message, f"ты проголосовал за отмену игры( Осталось {str(groups[str(message.chat.id)].to_end-1)}")
		if groups[str(message.chat.id)].to_end == 3:
			bot.reply_to(message, f"ну вот... игра остановлена... 🥀🕯\nСлово было: {groups[str(message.chat.id)].asked_word}.")
			groups[str(message.chat.id)].asked_word = None
			groups[str(message.chat.id)].game_in_process = False
			groups[str(message.chat.id)].game_iniciator = None
			groups[str(message.chat.id)].to_end = 0
			groups[str(message.chat.id)].asker = None
			
@bot.message_handler(commands=['leaderboard'], func=lambda message: message.chat.type == "group" or message.chat.type == "supergroup")
def answ_to_lead(message):
	if str(message.chat.id) not in groups:
		groups.update({str(message.chat.id):group(str(message.chat.id))})
	mess = "ВоТ жЕ оНи:\n"
	for lead in groups[str(message.chat.id)].leaderboard.keys():
		mess += f"{lead} - {groups[str(message.chat.id)].leaderboard[lead]} баллов\n"

	bot.send_message(str(message.chat.id), mess)




bot.polling(none_stop=True)