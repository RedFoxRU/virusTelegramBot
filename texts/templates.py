from config import CHANNELLINK


QVIRUS = """От: {fullname}
Сообщение:

{message}


Наш канал: [ """+CHANNELLINK+' ]'

PROFILE = """💳 Профиль пользователя _{name}_ 💳
🦠 Инфицирован: {is_infect}
💉 Когда заразился: {infect_dt}
💰 Денег: {money} 💰

Ваши шансы заразиться: {chances}%
Ваши шансы мутировать: {chances_mute}%
"""
G_PROFILE = """Профиль чата {chat}

Нулевой пациент: {zero_pac}
Болеющих: {ifecteds}
Вакцина: {vaccine}
Разработка продлится еще: 

Казна: {money}

"""