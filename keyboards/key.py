ADDRESS = 605850528
job = None  # тут хранится текущая работа, которую надо удалить из планировщика, прежде чем начать новую
scheduler_g = None
bot_g = None
con = None
cur = None

chet = 0
perec = 0

morning_key = ["Напоминаю, надо кушать! Мяу", "Чтобы убивать людей, надо зарядиться энергией, покушай по возможности",
               "Снова утро, снова я\nПокушай как проснёшься, Лиса", "Солнце встало,\nПоесть пора настала"]

waiting_key = ['Хорошо, засекаю и', 'Здорово!', '*звуки заводящегося(не сексуально) будильника*',
               'Постановка на боевое дежурство.', "Хитро улыбнулся,", "Туц-туц-тудуц,"]

nignt_key = ["Добрых снов =)", "Засыпай...", "Тёплых и милых снов", "Спокойной ночи)", "До связи утром)\nДоброй ночи"]