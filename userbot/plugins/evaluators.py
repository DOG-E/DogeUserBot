from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE
from io import StringIO
from os import geteuid
from traceback import format_exc
import sys

from . import BOTLOG, BOTLOG_CHATID, _format, doge, edl, eor

plugin_category = "tool"


@doge.bot_cmd(
    pattern="exec(?:\s|$)([\s\S]*)",
    command=("exec", plugin_category),
    info={
        "header": "To Execute terminal commands in a subprocess.",
        "usage": "{tr}exec <command>",
        "examples": "{tr}exec doge stringsetup.py",
    },
)
async def _(event):
    "To Execute terminal commands in a subprocess."
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await edl(event, "`What should i execute?..`")
    dogevent = await eor(event, "`Executing.....`")
    process = await create_subprocess_shell(
        cmd, stdout=PIPE, stderr=PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
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
        linktext=f"**•  Exec: **\n```{cmd}``` \n\n**•  Result : **\n",
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
        "header": "To Execute python script/statements in a subprocess.",
        "usage": "{tr}eval <command>",
        "examples": "{tr}eval print('DogeUserBot')",
    },
)
async def _(event):
    "To Execute python script/statements in a subprocess."
    cmd = "".join(event.message.message.split(maxsplit=1)[1:])
    if not cmd:
        return await edl(event, "`What should i run ?..`")
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
        f"**•  Eval : **\n```{cmd}``` \n\n**•  Result : **\n```{evaluation}``` \n"
    )
    await eor(
        dogevent,
        text=final_output,
        aslink=True,
        linktext=f"**•  Eval : **\n```{cmd}``` \n\n**•  Result : **\n",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "eval command " + cmd + " was executed sucessfully.",
        )


async def aexec(code, smessatatus):
    message = event = smessatatus
    p = lambda _x: print(_format.yaml_format(_x))
    reply = await event.get_reply_message()
    exec(
        "async def __aexec(message, event , reply, client, p, chat): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](
        message, event, reply, message.client, p, message.chat_id
    )
