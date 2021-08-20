from sys import exit

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from ..Config import Config
from .client import DogeUserBotClient

__version__ = "0.9"
loop = None


if Config.STRING_SESSION:
    session = StringSession(str(Config.STRING_SESSION))
else:
    session = "DogeUserBot"


try:
    doge = DogeUserBotClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"STRING_SESSION - {e}")
    exit()


doge.tgbot = tgbot = DogeUserBotClient(
    session="DogeTgBot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.BOT_TOKEN)
