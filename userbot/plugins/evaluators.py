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
from os import geteuid
from traceback import format_exc

from . import BOTLOG, BOTLOG_CHATID, _dogeutils, _format, doge, edl, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="exec(?:\s|$)([\s\S]*)",
    command=("exec", plugin_category),
    info={
        "h": "To Execute terminal commands in a subprocess.",
        "u": "{tr}exec <command>",
        "e": "{tr}exec python3 stringsetup.py",
    },
)
async def _(event):
    "To Execute terminal commands in a subprocess."
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await edl(event, "`What should I execute?..`")
    dogevent = await eor(event, "`Executing.....`")
    out, err = await _dogeutils.cmdrun(cmd)
    result = str(out) + str(err)
    doguser = await event.client.get_me()
    curruser = doguser.username or "DogeUserBot"
    uid = geteuid()
    if uid == 0:
        cresult = f"```{curruser}:~#``` ```{cmd}```\n```{result}```"
    else:
        cresult = f"```{curruser}:~$``` ```{cmd}```\n```{result}```"
    await eor(
        dogevent,
        text=cresult,
        aslink=True,
        linktext=f"**•  Exec:** \n```{cmd}``` \n\n**•  Result:** \n",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "Terminal command " + cmd + " was executed sucessfully.",
        )


@doge.bot_cmd(
    pattern="eval(?:\s|$)([\s\S]*)",
    command=("eval", plugin_category),
    info={
        "h": "To Execute python script/statements in a subprocess.",
        "u": "{tr}eval <command>",
        "e": "{tr}eval print('DogeUserBot')",
    },
)
async def _(event):
    "To Execute python script/statements in a subprocess."
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await edl(event, "`What should I run ?..`")
    cmd = (
        cmd.replace("sendmessage", "send_message")
        .replace("sendfile", "send_file")
        .replace("editmessage", "edit_message")
    )
    dogevent = await eor(event, "`Running...`")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, event)
    except Exception:
        exc = format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = (
        f"**•  Eval:** \n```{cmd}``` \n\n**•  Result:** \n```{evaluation}``` \n"
    )
    await eor(
        dogevent,
        text=final_output,
        aslink=True,
        linktext=f"**•  Eval:** \n```{cmd}``` \n\n**•  Result:** \n",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "eval command " + cmd + " was executed sucessfully.",
        )


async def aexec(code, smessatatus):
    message = event = smessatatus

    def p(_x):
        return print(_format.yaml_format(_x))

    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, event, reply, client, p, chat): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )
