Change env values for bot.py:\
```TOKEN = os.getenv("TG_BOT_TOKEN")```

Change env values for get_members.py(to get the members for the selected group and create members.csv (uses in bot.py for random selecting user from chat)):\
```api_id = os.getenv("TG_API_ID")```\
```api_hash = os.getenv("TG_API_HASH")```\
```phone = os.getenv("TG_PHONE")```

Change env values for wordle.py:\
```IMGUR_ID = os.getenv("IMGUR_ID")```\
And change ```chromedriver``` to your ARCH(snipped chromedriver-v17.3.0-linux-arm64)

Used wordle(https://wordle.belousov.one/) solver from https://github.com/pedrecho/wordle
