# **🧩 Example Plugins**

## **🦴 Mandatory Imports**

```python
from userbot import doge

from ..core.managers import edl, eor

plugin_category = "fun"
```

### **🐾 Formation**

- This below one is sample format of making plugin:

```python
from userbot import doge

from ..core.managers import edl, eor

plugin_category = "fun"


@doge.bot_cmd(
    pattern="hibuddy(?:\s|$)([\s\S]*)",
    command=("hibuddy", plugin_category),
    info={
        "h": "Just to say hi to other user.",
        "d": "input string along with cmd will be added to your hi text",
        "u": "{tr}hibuddy <text>",
        "e": "{tr}hibuddy how are you doing",
    },
)
async def hi_buddy(event):
    "Just to say hi to other user."
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edl(event, "No input is found. Use proper syntax.")

    outputtext = f"~~~~~\n> H-E-L-L-O <\n~~~~~\
        \n{input_str}"
    await eor(event, outputtext)
```

- For more information refer this [docs](https://docs.telethon.dev/en/latest/)

### **🧶 Arguments in *"bot_cmd"* are as follows:**

```python
@doge.bot_cmd(
    pattern="Regex for command",
    command=("Just command name", plugin_category), # Use plugin_category name from predefined names (admin, bot, fun, misc, tool, hub)
    info={
        "h": string - "intro for command",
        "d": string - "Description for command",
        "f": dict or string - "Flags you're using in your plugin",
        "o": dict or string - "Options you're using in your plugin",
        "t": list or string - "types you're using in your plugin",
        "u": "Usage for your command",
        "e": "Example for the command",
        "your custom name if you want to use other": str or list or dict - "data/information about it",
    },
# When you assign variables to the following values, put a comma at the end.
    groups_only=True or False(by default False)  # Either your command should work only in group or not

    allow_sudo=True or False(by default True)  # Should your sudo users need to have access or not,

    edited=True or False(by default True)  # If suppose you entered wrong command syntax and if you edit it correct should It work or not.

    forword=True or False(by deafult False)  # Is forword messages should react or not.

    disable_errors=True or False(by default False)  # If any error occured during the command usage should It log or not.
)
```
