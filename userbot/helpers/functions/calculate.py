# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
import sys
from io import StringIO
from traceback import format_exc


async def calcc(cmd, event, text=None):
    wtf = f"print({cmd})"
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexecc(wtf, event)
    except Exception:
        exc = format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        return exc
    elif stderr:
        return stderr
    elif stdout:
        return stdout
    else:
        return text


async def aexecc(code, event):
    exec("async def __aexecc(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexecc"](event)
