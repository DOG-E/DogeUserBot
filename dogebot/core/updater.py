# Credits to @sandy1709 (@mrconfused)
#
# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Forked, developed and edited for @DogeUserbot
#
import asyncio
import os
import sys

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from telethon import Button

from .. import UPSTREAM_REPO_URL, dogeversion
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from . import *

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>🐶 Doge UserBot {dogeversion} updates for <a href={UPSTREAM_REPO_URL}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"🐶 Doge UserBot {dogeversion} updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b><a href={UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    else:
        return ch_log, tldr_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join(
                [sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", reqs]
            ),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def updater(event):
    off_repo = UPSTREAM_REPO_URL
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(
            f"`Oops.. Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n\n`directory {error} is not found`"
        )
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(
            f"`Oops.. Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n\n`Early failure!\n{error}`"
        )
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("DOGE", origin.refs.DOGE)
        repo.heads.DOGE.set_tracking_branch(origin.refs.DOGE)
        repo.heads.DOGE.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if changelog:
        msg = True
    else:
        msg = False
    return msg


async def dev_doge(var):
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            var,
            "Set the required var in Heroku to function this normally `HEROKU_API_KEY`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            var,
            "Set the required var in Heroku to function this normally `HEROKU_APP_NAME`.",
        )
    heroku_var = app.config()
    await edit_or_reply(var, f"`Changing stabledoge to devdoge wait for 2-3 minutes.`")
    heroku_var["UPSTREAM_REPO"] = "https://github.com/TeleDoge/DogeUserBot"


@callbacq("updatenow")
@check_owner
async def update(eve):
    repo = Repo()
    ac_br = repo.active_branch
    ups_rem = repo.remote("upstream")
    if Config.HEROKU_API_KEY:
        import heroku3

        try:
            heroku = heroku3.from_key(Config.HEROKU_API_KEY)
            heroku_app = None
            heroku_applications = heroku.apps()
        except BaseException:
            return await eve.edit("`Wrong HEROKU_API.`")
        for app in heroku_applications:
            if app.name == Config.HEROKU_APP_NAME:
                heroku_app = app
        if not heroku_app:
            await eve.edit("`Wrong HEROKU_APP_NAME.`")
            repo.__del__()
            return
        await eve.edit(
            "`Userbot dyno build in progress, please wait for it to complete.`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Config.HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            await eve.edit(f"`Here is the error log:\n{error}`")
            repo.__del__()
            return
        await eve.edit("`Successfully Updated!\nRestarting, please wait...`")
    else:
        await eve.edit(
            "`Userbot dyno build in progress, please wait for it to complete.`"
        )
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await eve.edit(
            "`Successfully Updated!\nBot is restarting... Wait for a second!`"
        )
        os.execl(sys.executable, sys.executable, "-m", "dogebot")


@callbacq("changes")
@check_owner
async def changes(okk):
    repo = Repo.init()
    ac_br = repo.active_branch
    changelog, tl_chnglog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    changelog_str = changelog + f"\n\nClick the below button to update!"
    if len(changelog_str) > 1024:
        await okk.edit("`Changelog is too big, view the file to see it.`")
        file = open(f"DogeUserBot_changelog.txt", "w+")
        file.write(tl_chnglog)
        file.close()
        await okk.edit(
            "Click the below button to update.",
            file="DogeUserBot_changelog.txt",
            buttons=Button.inline("Update Now", data="updatenow"),
        )
        os.remove(f"DogeUserBot_changelog.txt")
        return
    else:
        await okk.edit(
            changelog_str,
            buttons=Button.inline("Update Now", data="updatenow"),
            parse_mode="html",
        )
