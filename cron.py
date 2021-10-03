"""
This is a bot to send Noom messages via Telegram every day at 8am
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from app import app, PRODUCTION
import telebot
import random

NOOM_TELEGRAM_KEY = '1969438179:AAGtLOqDcA_R0JV_wMdRXYmSMGDHARRVItg'
telgram_bot = telebot.TeleBot(NOOM_TELEGRAM_KEY)


"""
cron jobs.For more info look here:
https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html
"""

sched = BlockingScheduler(job_defaults={"misfire_grace_time": 15 * 60})


# Run on 8am Isreal Time
@sched.scheduled_job("cron", minute=0)  # type: ignore
def send_noom_message() -> None:
	from noom_articles import noom_articles_urls
	if app.env not in [PRODUCTION]:
		return None

	url = random.choice(noom_articles_urls)
	telgram_bot.send_message(text=url, chat_id=505895394)

	# from PIL import Image
	# # Taking the URL from some inspect of an image
	# url = "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/f10be216-5be0-4e32-92ca-f80b7d5e8df7/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20211003%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20211003T112630Z&X-Amz-Expires=86400&X-Amz-Signature=fba26a7d16020470102a45665044876cd4d552aaa91c8a9e9dead33d873d2f83&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22"
	# # This will download the URL 
	# im = Image.open(requests.get(url, stream=True).raw)
	# This will send it via telegram
	# telgram_bot.send_photo(505895394, img)



sched.start()

