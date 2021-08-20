from asyncio import create_subprocess_shell
from asyncio.exceptions import CancelledError
from asyncio.subprocess import PIPE
from os import path as osp
from os import remove
from sys import executable

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from heroku3 import from_key
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from . import (
    HEROKU_APP,
    UPSTREAM_REPO_URL,
    Config,
    delgvar,
    doge,
    edl,
    eor,
    logging,
    tr,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = from_key(Config.HEROKU_API_KEY)
UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH
disable_warnings(InsecureRequestWarning)
requirements_path = osp.join(
    osp.dirname(osp.dirname(osp.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("`Changelog is too big, view the file to see it.`")
        with open("@DogeUserBot.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "@DogeUserBot.txt",
            reply_to=event.id,
        )
        remove("@DogeUserBot.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await create_subprocess_shell(
            " ".join([executable, "-m", "pip", "install", "-r", reqs]),
            stdout=PIPE,
            stderr=PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def pull(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    dogevent = await event.edit(
        "`Successfully Updated!\n" "Bot is restarting... Wait for a minute!`"
    )
    await event.client.reload(dogevent)


async def push(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("`Please set up`  **HEROKU_API_KEY**  ` Var...`")
    heroku = from_key(HEROKU_API_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "`Please set up the` **HEROKU_APP_NAME** `Var`"
            " to be able to deploy your doge...`"
        )
        repo.__del__()
        return
    for app in heroku_applications:
        if app.name == HEROKU_APP_NAME:
            heroku_app = app
            break
    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "`Invalid Heroku credentials for deploying Doge dyno.`"
        )
        return repo.__del__()
    dogevent = await event.edit(
        "`Doge dyno build in progress, please wait until the process finishes it usually takes 4 to 5 minutes .`"
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [dogevent.chat_id, dogevent.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", "https://api:" + HEROKU_API_KEY + "@"
    )
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Error log:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edl(
            event, "`Build failed! ❌\n" "Cancelled or there were some errors...`"
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Here is the error log:**\n`{error}`")
        return repo.__del__()
    await event.edit("`Deploy was failed. So restarting to update`")
    delgvar("ipaddress")
    try:
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    except CancelledError:
        pass


@doge.bot_cmd(
    pattern="update( pull| push|$)",
    command=("update", plugin_category),
    info={
        "header": "To update DogeUserbot.",
        "description": "I recommend you to do update push atlest once a week.",
        "options": {
            "pull": "Will update bot but requirements doesnt update.",
            "push": "Bot will update completly with requirements also.",
            "dogeup": "to update to the original repository, if you fork.",
        },
        "usage": [
            "{tr}update",
            "{tr}update pull",
            "{tr}update push",
            "{tr}dogeup",
        ],
    },
)
async def upstream(event):
    "To check if the bot is up to date and update if specified"
    conf = event.pattern_match.group(1).strip()
    event = await eor(event, "`Checking for updates, please wait...`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await eor(event, "`Set the required vars first to update the bot`")
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Unfortunately, the directory {error} "
                "does not seem to be a git repository.\n"
                "But we can fix that by force updating the doge bot using "
                ".update pull.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
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
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if conf == "push":
        await event.edit("`Deploying Doge, please wait...`")
        await push(event, repo, ups_rem, ac_br, txt)
        return
    if changelog == "" and not force_update:
        await event.edit(
            "\n`Doge is`  **up-to-date**  `with`  " f"**{UPSTREAM_REPO_BRANCH}**\n"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"**Command:**\n\n[ `{tr}update push` ] > update deploy\n[ `{tr}update pull` ] > update now"
        )

    if force_update:
        await event.edit("`Force-Syncing to latest stable bot code, please wait...`")
    if conf == "pull":
        await event.edit("`Updating doge, please wait...`")
        await pull(event, repo, ups_rem, ac_br)
    return


@doge.bot_cmd(
    pattern="dogeup$",
    command=("dogeup", plugin_category),
    info={
        "header": "To update to Doge.",
        "description": "I recommend you to do update push atlest once a week.",
        "options": {
            "dogeup": "To update to the original repository, if you fork.",
        },
        "usage": [
            "{tr}dogeup",
        ],
    },
)
async def variable(var):
    "To update to to the DogeRepository."
    if Config.HEROKU_API_KEY is None:
        return await edl(
            var,
            "Set the required var in heroku to function this normally `HEROKU_API_KEY`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edl(
            var,
            "Set the required var in heroku to function this normally `HEROKU_APP_NAME`.",
        )
    heroku_var = app.config()
    await eor(var, f"`Switch... wait for 2-3 minutes.`")
    heroku_var["UPSTREAM_REPO"] = "DogeUserBot"
