# Config values will be loaded from here

from os import environ as ose, path as osp

ENV = bool(ose.get("ENV", False))


if ENV:
    from sample_config import Config  # noqa

elif osp.exists("config.py"):
    from config import Development as Config  # noqa
