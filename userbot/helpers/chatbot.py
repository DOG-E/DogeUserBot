from . import install_pip

try:
    from randomstuff import AsyncClient
except ModuleNotFoundError:
    install_pip("randomstuff.py")
    from randomstuff import AsyncClient

from ..Config import Config

rs_client = AsyncClient(api_key=Config.RANDOM_STUFF_API_KEY, version="4")
