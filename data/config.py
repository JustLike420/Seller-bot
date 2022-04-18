import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
BOT_TOKEN = config["settings"]["token"]
admins = config["settings"]["admin_id"]
email_login = config["settings"]["email_login"]
email_password = config["settings"]["email_password"]
recipient = config["settings"]["recipient"]
if "," in admins:
    admins = admins.split(",")
else:
    if len(admins) >= 1:
        admins = [admins]
    else:
        admins = []
        print("***** You didn't enter an admin ID *****")