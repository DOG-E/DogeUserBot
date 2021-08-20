# UniBorg Telegram UseRBot
# Copyright (C) 2020 @UniBorg
# This code is licensed under
# the "you can't use this for anything - public or private,
# unless you know the two prime factors to the number below" license
# 543935563961418342898620676239017231876605452284544942043082635399903451854594062955
# വിവരണം അടിച്ചുമാറ്റിക്കൊണ്ട് പോകുന്നവർ
# ക്രെഡിറ്റ് വെച്ചാൽ സന്തോഷമേ ഉള്ളു..!
# uniborg

from ...Config import Config


def check_data_base_heal_th():
    # https://stackoverflow.com/a/41961968
    is_database_working = False
    output = "No Database is set"
    if not Config.DB_URI:
        return is_database_working, output
    from ...sql_helper import SESSION

    try:
        # to check database we will execute raw query
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"🚨 {e}"
        is_database_working = False
    else:
        output = "Active"
        is_database_working = True
    return is_database_working, output


async def dogealive():
    return f"🐶 Doɢᴇ UsᴇʀBoᴛ\
        \n🐾 Iɴғo\
        \n\
        \n🔹 To check it's working:\
        \n.alive\
        \n\
        \n🔹 To get help:\
        \n.doge"
