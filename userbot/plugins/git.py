from datetime import datetime
from os import getcwd, makedirs
from os import path as osp
from os import remove

from aiohttp import ClientSession
from github import Github
from pySmartDL import SmartDL
from requests import get

from . import Config, doge, edl, eor, lan, logging, reply_id

plugin_category = "tool"
LOGS = logging.getLogger(osp.basename(__name__))

ppath = osp.join(getcwd(), "temp", "githubuser.jpg")
GIT_TEMP_DIR = "./temp/"


@doge.bot_cmd(
    pattern="repo$",
    command=("repo", plugin_category),
    info={
        "header": "Source code link of userbot",
        "usage": [
            "{tr}repo",
        ],
    },
)
async def source(e):
    "Source code link of userbot"
    await eor(
        e,
        "Click [here](https://github.com/DOG-E/dogeuserbot) to open this bot source code",
    )


@doge.bot_cmd(
    pattern="github( .l(\d+))? ([\s\S]*)",
    command=("github", plugin_category),
    info={
        "header": "Shows the information about an user on GitHub of given username",
        "flags": {".l": "repo limit : default to 5"},
        "usage": ".github [flag] [username]",
        "examples": [".github teledoge", ".github .l5 mutlcc"],
    },
)
async def _(event):
    "Get info about an GitHub User"
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edl(event, "`" + username + " not found`")

            dogevent = await eor(event, "`fetching github info...`")
            result = await request.json()
            photo = result["avatar_url"]
            if result["bio"]:
                result["bio"] = result["bio"].strip()
            repos = []
            sec_res = get(result["repos_url"])
            if sec_res.status_code == 200:
                limit = event.pattern_match.group(2)
                limit = 5 if not limit else int(limit)
                for repo in sec_res.json():
                    repos.append(f"[{repo['name']}]({repo['html_url']})")
                    limit -= 1
                    if limit == 0:
                        break
            REPLY = "**GitHub Info for** `{username}`\
                \n👤 **Name:** [{name}]({html_url})\
                \n🔧 **Type:** `{type}`\
                \n🏢 **Company:** `{company}`\
                \n🔭 **Blog:** {blog}\
                \n📍 **Location:** `{location}`\
                \n📝 **Bio:** __{bio}__\
                \n❤️ **Followers:** `{followers}`\
                \n👁 **Following:** `{following}`\
                \n📊 **Public Repos:** `{public_repos}`\
                \n📄 **Public Gists:** `{public_gists}`\
                \n🔗 **Profile Created:** `{created_at}`\
                \n✏️ **Profile Updated:** `{updated_at}`".format(
                username=username, **result
            )
            if repos:
                REPLY += "\n🔍 **Some Repos:** " + " | ".join(repos)
            downloader = SmartDL(photo, ppath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
            await event.client.send_file(
                event.chat_id,
                ppath,
                caption=REPLY,
                reply_to=reply_to,
            )
            remove(ppath)
            await dogevent.delete()


@doge.bot_cmd(
    pattern="commit$",
    command=("commit", plugin_category),
    info={
        "header": "To commit the replied plugin to github.",
        "description": "It uploads the given file to your github repo in **userbot/plugins** folder\
        \nTo work commit plugin set `GITHUB_ACCESS_TOKEN` and `GIT_REPO_NAME` Variables in Heroku vars First",
        "note": "As of now not needed i will sure develop it ",
        "usage": "{tr}commit",
    },
)
async def download(event):
    "To commit the replied plugin to github."
    if Config.GITHUB_ACCESS_TOKEN is None:
        return await edl(event, "`Please ADD Proper Access Token from github.com`", 5)

    if Config.GIT_REPO_NAME is None:
        return await edl(
            event, "`Please ADD Proper Github Repo Name of your userbot`", 5
        )

    mone = await eor(event, lan("processing"))
    if not osp.isdir(GIT_TEMP_DIR):
        makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    if not reply_message or not reply_message.media:
        return await edl(
            event, "__Reply to a file which you want to commit in your github.__"
        )

    try:
        downloaded_file_name = await event.client.download_media(reply_message.media)
    except Exception as e:
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        await mone.edit("Committing to Github....")
        await git_commit(downloaded_file_name, mone)


async def git_commit(file_name, mone):
    content_list = []
    access_token = Config.GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name, "r", encoding="utf-8")
    commit_data = file.read()
    repo = g.get_repo(Config.GIT_REPO_NAME)
    LOGS.info(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        LOGS.info(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="' + file_name + '")':
            return await mone.edit("`File Already Exists`")

    if create_file:
        file_name = "userbot/plugins/" + file_name
        LOGS.info(file_name)
        try:
            repo.create_file(
                file_name, "Uploaded New Plugin", commit_data, branch="master"
            )
            LOGS.info("Committed File")
            ccess = Config.GIT_REPO_NAME
            ccess = ccess.strip()
            await mone.edit(
                f"`Commited On Your Github Repo`\n\n[Your PLUGINS](https://github.com/{ccess}/tree/master/userbot/plugins/)"
            )
        except BaseException:
            LOGS.info("Cannot Create Plugin")
            await mone.edit("Cannot Upload Plugin")
    else:
        return await mone.edit("`Committed Suicide`")
