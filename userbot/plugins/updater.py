# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/DOG-E/DogeUserBot > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
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
    HEROKU_API_KEY,
    HEROKU_APP,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_URL,
    Config,
    dgvar,
    doge,
    edl,
    eor,
    logging,
    tr,
)

plugin_category = "bot"
LOGS = logging.getLogger(__name__)

disable_warnings(InsecureRequestWarning)
if HEROKU_API_KEY:
    heroku = from_key(HEROKU_API_KEY)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, changelog):
    changelog_str = f"**Güɴᴄᴇʟʟᴇᴍᴇʟᴇʀ ᴠᴀʀ!:\n\
        \nDᴇɢ̆ɪşɪᴋʟɪᴋʟᴇʀ:**\
        \n`{changelog}`"
    if len(changelog_str) > 4096:
        await event.edit(
            "`🐶 Değişiklik listesi upuzun.\
            \n🐾 Bu yüzden değişiklikleri dosya olarak gönderiyorum...`"
        )
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
    try:
        process = await create_subprocess_shell(
            " ".join(
                [
                    executable,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(
                        osp.join(
                            osp.dirname(osp.dirname(osp.dirname(__file__))),
                            "requirements.txt",
                        ),
                    ),
                ],
            ),
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
        "`Güncelleme başarıyla tamamlandı!\n"
        "Bot yeniden başlatılıyor... Lütfen bekleyin!`"
    )
    await event.client.reload(dogevent)


async def push(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        await event.edit("**Lütfen** `HEROKU_API_KEY` **değerini ayarlayın!**")
        repo.__del__()
        return
    heroku_app = None
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit("**Lütfen** `HEROKU_APP_NAME` **değerini ayarlayın!**")
        repo.__del__()
        return
    for app in heroku_applications:
        if app.name == HEROKU_APP_NAME:
            heroku_app = app
            break
    if heroku_app is None:
        await event.edit(f"{txt}\n\n`Heroku dyno kimlik bilgileri yanlış!`")
        return repo.__del__()
    dogevent = await event.edit(
        "`Doge dyno derlemesi devam ediyor, lütfen işlem bitene kadar bekleyin, genellikle 4 ila 5 dakika sürer.`"
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(f"🚨 {e}")
    try:
        add_to_collectionlist("restart_update", [dogevent.chat_id, dogevent.id])
    except Exception as e:
        LOGS.error(f"🚨 {e}")
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
        await event.edit(f"{txt}\n**Hata log'unuz burada:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edl(
            event,
            "`Yapılandırma iptal edildi! ❌\n"
            "Kullanıcı tarafından iptal edildi ya da bazı hatalar oluştu...`",
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n*Hata log'unuz burada:**\n`{error}`")
        return repo.__del__()
    await event.edit(
        "`Deploy edilirken hata oluştu! Bu yüzden yeniden başlatılarak güncelleniyor!`"
    )
    dgvar("ipaddress")
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
        "h": "DogeUserbot'unuzu günceller.",
        "d": "Haftada en az bir defa `.update push` yapmanız önerilir..",
        "o": {
            "pull": "Bot günceller ama gereksinimler güncellenmiyor.",
            "push": "Bot ve  gereksinimlerini de tamamen güncelleyecektir.",
        },
        "u": [
            "{tr}update",
            "{tr}update pull",
            "{tr}update push",
        ],
    },
)
async def upstream(event):
    "Botun güncel olup olmadığını kontrol eder ve günceller."
    conf = event.pattern_match.group(1).strip()
    event = await eor(event, "`Güncellemeleri kontrol ediyorum, lütfen bekleyin...`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await eor(
            event, "`Botu güncellemek için önce gerekli değerleri ayarlayın.`"
        )
    try:
        txt = "`Oops... Hata! Güncelleme şu nedenle devam edemiyor: "
        txt += "Bazı sorunlar oluştu:`\n\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}`{error} dizininde bulunamadı!`")
        repo = Repo()
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`{error}`")
        repo = Repo()
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Ne yazık ki, dizin {error} "
                "bir GİT reposu gibi görünmüyor..\n"
                "Ancak bunu, doge botunu kullanarak zorla güncelleyerek düzeltebiliriz "
                ".update pull.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("DOGE-TR", origin.refs.DOGE)
        repo.heads.DOGE.set_tracking_branch(origin.refs.DOGE)
        repo.heads.DOGE.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != Config.UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"__Görünüşe göre kendi özel reponuzu kullanıyorsunuz:__[ `{ac_br}` ]. "
            "__Bu durumda hangi 'Branch' üzerinden"
            "güncelleneceği tanımlanamaz. "
            "Lütfen resmi repoyu kullanın.__"
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
        await event.edit("`Doge güncelleniyor, lütfen bekleyin...`")
        await push(event, repo, ups_rem, ac_br, txt)
        return
    if changelog == "" and not force_update:
        await event.edit("`🐶`** Doge UserBot **`en güncel durumda!`")
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, changelog)
        await event.delete()
        return await event.respond(
            f"**Komut:**\n\n[ `{tr}update push` ] > Deploy ile günceller...\n[ `{tr}update pull` ] > Şimdi günceller..."
        )

    if force_update:
        await event.edit(
            "`Son yol olarak, bot kodlarına zorunlu-güncelleştirme uygulanıyor.`"
        )
    if conf == "pull":
        await event.edit("`Doge güncelleniyor, lütfen bekleyin...`")
        await pull(event, repo, ups_rem, ac_br)
    return
