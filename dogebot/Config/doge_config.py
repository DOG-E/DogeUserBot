# Credits to @sandy1709 (@mrconfused)
#
# Forked, developed and edited for @DogeUserbot
#
# config values will be loaded from here
import os

ENV = bool(os.environ.get("ENV", False))

if ENV:
    pass
elif os.path.exists("config.py"):
    pass
