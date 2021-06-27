from sample_config import Config


class Development(Config):
    # Get this values from the https://my.telegram.org/apps
    APP_ID = 6
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
    # The name to display in your alive message
    ALIVE_NAME = "Your value"
    # Create any PostgreSQL database (recommend to use ElephantSQL) and paste that link here
    DB_URI = "Your value"
    # Get this value by running ### or https://
    STRING_SESSION = "Your value"
    # Create a new bot in @BotFather(https://t.me/BotFather) and fill the following vales with Bot TokenAPI and username respectively
    TG_BOT_TOKEN = "Your value"
    TG_BOT_USERNAME = "Your value"
    # Set Doge language
    DOGELANG = "en"
    # Create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -100
    # Command handler
    COMMAND_HAND_LER = "."
    # Sudo enter the id of sudo users userid's in that array
    SUDO_USERS = []
    # Command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
