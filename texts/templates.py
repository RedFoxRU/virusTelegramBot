from config import CHANNELLINK


QVIRUS = """От: {fullname}
Сообщение:

{message}


Наш канал: [ """+CHANNELLINK+' ]'

PROFILE = """Профиль пользователя {name}
Инфицирован: {is_infect}
Когда заразился: {infect_dt}
Денег: {money} 💰
"""