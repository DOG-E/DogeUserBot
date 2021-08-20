"""Get the info your system. Using .neofetch then .sysd"""

# .spc command is ported from  alfianandaa/ProjectAlf

from datetime import datetime
from platform import uname as puname
from sys import version

from psutil import (
    boot_time,
    cpu_count,
    cpu_freq,
    cpu_percent,
    net_io_counters,
    virtual_memory,
)
from telethon import __version__

from . import _dogeutils, doge, eor

plugin_category = "bot"


def get_size(inputbytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if inputbytes < factor:
            return f"{inputbytes:.2f}{unit}{suffix}"
        inputbytes /= factor


@doge.bot_cmd(
    pattern="spc$",
    command=("spc", plugin_category),
    info={
        "header": "To show system specification.",
        "usage": "{tr}spc",
    },
)
async def psu(event):
    "shows system specification"
    uname = puname()
    softw = "**System Information**\n"
    softw += f"`System  : {uname.system}`\n"
    softw += f"`Release : {uname.release}`\n"
    softw += f"`Version : {uname.version}`\n"
    softw += f"`Machine : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**CPU Info**\n"
    cpuu += "`Physical cores  : " + str(cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores     : " + str(cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = cpu_freq()
    cpuu += f"`Max Frequency   : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency   : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(cpu_percent(percpu=True)):
        cpuu += f"`Core {i} : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`All Core: {cpu_percent()}%`\n"
    # RAM Usage
    svmem = virtual_memory()
    memm = "**Memory Usage**\n"
    memm += f"`Total    : {get_size(svmem.total)}`\n"
    memm += f"`Available: {get_size(svmem.available)}`\n"
    memm += f"`Used     : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload : {get_size(net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(net_io_counters().bytes_recv)}`\n"
    help_string = f"{softw}\n"
    help_string += f"{cpuu}\n"
    help_string += f"{memm}\n"
    help_string += f"{bw}\n"
    help_string += "**Engine Info**\n"
    help_string += f"`Python {version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


@doge.bot_cmd(
    pattern="cpu$",
    command=("cpu", plugin_category),
    info={
        "header": "To show cpu information.",
        "usage": "{tr}cpu",
    },
)
async def cpu(event):
    "shows cpu information"
    cmd = "cat /proc/cpuinfo | grep 'model name'"
    o = (await _dogeutils.runcmd(cmd))[0]
    await eor(event, f"**[Dog's](tg://need_update_for_some_feature/) CPU Model:**\n{o}")


@doge.bot_cmd(
    pattern="sysd$",
    command=("sysd", plugin_category),
    info={
        "header": "Shows system information using neofetch",
        "usage": "{tr}cpu",
    },
)
async def sysdetails(sysd):
    "Shows system information using neofetch"
    dogevent = await eor(sysd, "`Fetching system information.`")
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
    await _dogeutils.runcmd(cmd)
    neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
    a, b, c, d = await _dogeutils.runcmd(neo)
    result = str(a) + str(b)
    await eor(dogevent, "**Neofetch Result:** `" + result + "`")
