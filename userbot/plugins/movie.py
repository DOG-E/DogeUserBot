from os import getcwd, path, remove

from bs4 import BeautifulSoup
from justwatch import JustWatch, justwatchapi
from pySmartDL import SmartDL

from . import (
    Config,
    doge,
    eor,
    get_cast,
    get_moviecollections,
    imdb,
    logging,
    mov_titles,
    reply_id,
)

plugin_category = "misc"
LOGS = logging.getLogger(__name__)

moviepath = path.join(getcwd(), "temp", "moviethumb.jpg")
justwatchapi.__dict__["HEADER"] = {
    "User-Agent": "JustWatch client (github.com/dawoudt/JustWatchAPI)"
}


def get_stream_data(query):
    stream_data = {}
    # Compatibility for Current Userge Users
    try:
        country = Config.WATCH_COUNTRY
    except Exception:
        country = "IN"
    # Cooking Data
    just_watch = JustWatch(country=country)
    results = just_watch.search_for_item(query=query)
    movie = results["items"][0]
    stream_data["title"] = movie["title"]
    stream_data["movie_thumb"] = (
        "https://images.justwatch.com"
        + movie["poster"].replace("{profile}", "")
        + "s592"
    )
    stream_data["release_year"] = movie["original_release_year"]
    try:
        LOGS.info(movie["cinema_release_date"])
        stream_data["release_date"] = movie["cinema_release_date"]
    except KeyError:
        try:
            stream_data["release_date"] = movie["localized_release_date"]
        except KeyError:
            stream_data["release_date"] = None

    stream_data["type"] = movie["object_type"]

    available_streams = {}
    for provider in movie["offers"]:
        provider_ = get_provider(provider["urls"]["standard_web"])
        available_streams[provider_] = provider["urls"]["standard_web"]

    stream_data["providers"] = available_streams

    scoring = {}
    for scorer in movie["scoring"]:
        if scorer["provider_type"] == "tmdb:score":
            scoring["tmdb"] = scorer["value"]

        if scorer["provider_type"] == "imdb:score":
            scoring["imdb"] = scorer["value"]
    stream_data["score"] = scoring
    return stream_data


# Helper Functions
def pretty(name):
    if name == "play":
        name = "Google Play Movies"
    return name[0].upper() + name[1:]


def get_provider(url):
    url = url.replace("https://www.", "")
    url = url.replace("https://", "")
    url = url.replace("http://www.", "")
    url = url.replace("http://", "")
    url = url.split(".")[0]
    return url


# Credits: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
@doge.bot_cmd(
    pattern="watch ([\s\S]*)",
    command=("watch", plugin_category),
    info={
        "header": "To search online streaming sites for that movie.",
        "description": "Fetches the list of sites(standard) where you can watch that movie.",
        "usage": "{tr}watch <movie name>",
        "examples": "{tr}watch aquaman",
    },
)
async def _(event):
    "To search online streaming sites for that movie."
    query = event.pattern_match.group(1)
    et = await eor(event, "`Finding Sites...`")
    try:
        streams = get_stream_data(query)
    except Exception as e:
        return await et.edit(f"**Error:** `{e}`")
    title = streams["title"]
    thumb_link = streams["movie_thumb"]
    release_year = streams["release_year"]
    release_date = streams["release_date"]
    scores = streams["score"]
    try:
        imdb_score = scores["imdb"]
    except KeyError:
        imdb_score = None
    try:
        tmdb_score = scores["tmdb"]
    except KeyError:
        tmdb_score = None

    stream_providers = streams["providers"]
    if release_date is None:
        release_date = release_year

    output_ = f"**Movie:**\n`{title}`\n**Release Date:**\n`{release_date}`"
    if imdb_score:
        output_ = output_ + f"\n**IMDB: **{imdb_score}"
    if tmdb_score:
        output_ = output_ + f"\n**TMDB: **{tmdb_score}"

    output_ = output_ + "\n\n**Available on:**\n"
    for provider, link in stream_providers.items():
        if "sonyliv" in link:
            link = link.replace(" ", "%20")
        output_ += f"[{pretty(provider)}]({link})\n"
    downloader = SmartDL(thumb_link, moviepath, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    await event.client.send_file(
        event.chat_id,
        caption=output_,
        file=moviepath,
        force_document=False,
        allow_cache=False,
        silent=True,
    )
    await et.delete()


@doge.bot_cmd(
    pattern="imdb ([\s\S]*)",
    command=("imdb", plugin_category),
    info={
        "header": "To fetch imdb data about the given movie or series.",
        "usage": "{tr}imdb <movie/series name>",
    },
)
async def imdb_query(event):  # sourcery no-metrics
    """To fetch imdb data about the given movie or series."""
    dogevent = await eor(event, "`searching........`")
    reply_to = await reply_id(event)
    try:
        movie_name = event.pattern_match.group(1)
        movies = imdb.search_movie(movie_name)
        movieid = movies[0].movieID
        movie = imdb.get_movie(movieid)
        moviekeys = list(movie.keys())
        for i in mov_titles:
            if i in moviekeys:
                mov_title = movie[i]
                break
        for j in reversed(mov_titles):
            if j in moviekeys:
                mov_ltitle = movie[j]
                break
        mov_runtime = movie["runtimes"][0] + " min" if "runtimes" in movie else ""
        if "original air date" in moviekeys:
            mov_airdate = movie["original air date"]
        elif "year" in moviekeys:
            mov_airdate = movie["year"]
        else:
            mov_airdate = ""
        mov_genres = ", ".join(movie["genres"]) if "genres" in moviekeys else "Not Data"
        mov_rating = str(movie["rating"]) if "rating" in moviekeys else "Not Data"
        mov_rating += (
            " (by " + str(movie["votes"]) + ")"
            if "votes" in moviekeys and "rating" in moviekeys
            else ""
        )
        mov_countries = (
            ", ".join(movie["countries"]) if "countries" in moviekeys else "Not Data"
        )
        mov_languages = (
            ", ".join(movie["languages"]) if "languages" in moviekeys else "Not Data"
        )
        mov_plot = (
            str(movie["plot outline"]) if "plot outline" in moviekeys else "Not Data"
        )
        mov_director = await get_cast("director", movie)
        mov_composers = await get_cast("composers", movie)
        mov_writer = await get_cast("writer", movie)
        mov_cast = await get_cast("cast", movie)
        mov_box = await get_moviecollections(movie)
        resulttext = f"""
<b>Title : </b><code>{mov_title}</code>
<b>Imdb Url : </b><a href='https://www.imdb.com/title/tt{movieid}'>{mov_ltitle}</a>
<b>Info : </b><code>{mov_runtime} | {mov_airdate}</code>
<b>Genres : </b><code>{mov_genres}</code>
<b>Rating : </b><code>{mov_rating}</code>
<b>Country : </b><code>{mov_countries}</code>
<b>Language : </b><code>{mov_languages}</code>
<b>Director : </b><code>{mov_director}</code>
<b>Music Director : </b><code>{mov_composers}</code>
<b>Writer : </b><code>{mov_writer}</code>
<b>Stars : </b><code>{mov_cast}</code>
<b>Box Office : </b>{mov_box}
<b>Story Outline : </b><i>{mov_plot}</i>"""
        if "full-size cover url" in moviekeys:
            imageurl = movie["full-size cover url"]
        else:
            imageurl = None
        soup = BeautifulSoup(resulttext, features="html.parser")
        rtext = soup.get_text()
        if len(rtext) > 1024:
            extralimit = len(rtext) - 1024
            climit = len(resulttext) - extralimit - 20
            resulttext = resulttext[:climit] + "...........</i>"
        if imageurl:
            downloader = SmartDL(imageurl, moviepath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        if path.exists(moviepath):
            await event.client.send_file(
                event.chat_id,
                moviepath,
                caption=resulttext,
                reply_to=reply_to,
                parse_mode="HTML",
            )
            remove(moviepath)
            return await dogevent.delete()
        await dogevent.edit(
            resulttext,
            link_preview=False,
            parse_mode="HTML",
        )
    except IndexError:
        await dogevent.edit(f"__No movie found with name {movie_name}.__")
    except Exception as e:
        await dogevent.edit(f"**Error:**\n__{e}__")
