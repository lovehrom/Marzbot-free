import os
import re

from dotenv import load_dotenv

if DOTENV_PATH := os.getenv("PYTHON_DOTENV_FILE"):
    from decouple import Config, RepositoryEnv

    load_dotenv(DOTENV_PATH)
    config = Config(RepositoryEnv(DOTENV_PATH))
else:
    from decouple import config

    load_dotenv()

from app.logger import get_logger

log = get_logger(__name__)


LOG_LEVEL = config("LOG_LEVEL", default="info")

BOT_TOKEN = config("BOT_TOKEN")

SETTINGS = {
    "BOT:ACCESS_ONLY": config("SETTINGS:BOT:ACCESS_ONLY", default=False, cast=bool),
    "PAYMENT:CRYPTO": config("SETTINGS:PAYMENT:CRYPTO", default=True, cast=bool),
}

# socks5h://127.0.0.1:2080
PROXY = config("PROXY", None)


PARSE_MODE = config("PARSE_MODE", default="HTML")
DATABASE_URL = config(
    "DATABASE_URL", default="sqlite://db.sqlite3"
)  # example: 'mysql://user:pass@localhost:3306/db'
# exmaple: 'sqlite:///marzbot.db'

if DATABASE_URL is None:
    raise ValueError("'DATABASE_URL' environment variable has to be set!")

BOT_USERNAME = config("BOT_USERNAME", default="marzdemobot")

DEFAULT_USERNAME_PREFIX = config("DEFAULT_USERNAME_PREFIX", default="Marzdemo")

if not re.match(r"^(?!_)[A-Za-z0-9_]+$", DEFAULT_USERNAME_PREFIX):
    raise ValueError(
        "DEFAULT_USERNAME_PREFIX must be less than 20 characters and [0-9A-Za-z] and underscores in between"
    )

PAYMENTS_DISCOUNT_ON = config(
    "PAYMENTS_DISCOUNT_ON", default=400000, cast=int
)  # payments higher than this amount will have a discount, set 0 for no discount
PAYMENTS_DISCOUNT_ON_PERCENT = config(
    "PAYMENTS_DISCOUNT_ON_PERCENT", default=6, cast=int
)  # default: 6 percent free credit for payments more than 400,000t


if PAYMENTS_DISCOUNT_ON:
    FREE_CREDIT_ON_TEXT = f"🔥 تمامی پرداخت‌های بیشتر از {PAYMENTS_DISCOUNT_ON:,} руб. получают бонус {PAYMENTS_DISCOUNT_ON_PERCENT} درصد اعتبار هدیه می‌شوند😉"
else:
    FREE_CREDIT_ON_TEXT = ""

NP_API_URL = config("NP_API_URL", default="https://api.nowpayments.io/v1")
NP_API_KEY = config("NP_API_KEY", default=None)

NP_IPN_CALLBACK_URL = config(
    "NP_IPN_CALLBACK_URL", default="https://rayapardazapi.ir/cryptogw"
)

NP_IPN_SECRET_KEY = config("NP_IPN_SECRET_KEY", default=None)
NP_SUCCESS_URL = config("NP_SUCCESS_URL", default=None)
NP_CANCEL_URL = config("NP_CANCEL_URL", default=None)
# --- YooKassa ---
YOOKASSA_SHOP_ID = config("YOOKASSA_SHOP_ID", default="")
YOOKASSA_SECRET_KEY = config("YOOKASSA_SECRET_KEY", default="")
IS_TEST = config("IS_TEST", default=0, cast=int)
# ----------------


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [  # put rest of the models as so in the list
                "app.models.user",
                "app.models.server",
                "app.models.service",
                "app.models.proxy",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}

REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_PORT", default=6379)
REDIS_DB = config("REDIS_DB", default=0)


WEBAPP_HOST = config("WEBAPP_HOST", default="127.0.0.1")
WEBAPP_PORT = config("WEBAPP_PORT", default=3333)


FORCE_JOIN_CHATS = {
    chat.split("@")[0]: chat.split("@")[1]
    for chat in config("FORCE_JOIN_CHATS", default="-1001892840605@marzdemo").split(
        "\n"
    )
    if chat
}


def generate_help(text: str) -> str:
    if not text:
        return ""
    return f"~~~~~~~~~~~~~~~~~~~~~~~~\n{text}\n~~~~~~~~~~~~~~~~~~~~~~~~"


_START_TEXT = f"""
👋 سلااااام
به ربات خوش اومدی😉

با سرویس‌های ما میتونی همیشه و هر لحظه و با هر دستگاهی به اینترنت متصل بمونی🌝

💡 برای دریافت اخبار، وضعیت سرویس‌ها و دریافت کدهای هدیه روزانه در کانال ما عضو بشید
🆔 @marzdemo

🔍 اگه میخوای بیشتر در مورد ربات بدونی میتونی دکمه <b>«راهنما»</b> رو بزنی
"""


_FORCE_JOIN_TEXT = f"""
♻️ برای استفاده از ربات باید در کانال ما عضو بشید

توی کانالی که پایین مشخص شده عضو بشید و سپس دکمه «تأیید عضویت» رو بزنید👇

🆔 @marzdemo
"""

_SUPPORT_TEXT = """
✋ به بخش پشتیبانی خوش اومدی

قبل از اینکه به پشتیبانی پیام بدید، حواستون باشه که بخش‌ «راهنما» رو مطالعه کرده باشید، احتمالا جواب سوالتون رو پیدا می‌کنید😉

⁉️ جواب سوالتون اونجا نبود؟ اشکالی نداره، میتونید از طریق آیدی زیر با پشتیبانی ارتباط برقرار کنید👇

🆔 @govfvck1

💡 بعد از پیام دادن به پشتیبانی، لطفا صبور باشید. به همه پیام‌ها در اسرع وقت جواب داده میشه🙏
"""

_HELP_TEXT = """
به بخش راهنمای استفاده از ربات خوش اومدید

شما می‌تونید برای خرید اشتراک به چند روش پرداخت رو انجام بدید که می‌تونید با کلیک رو دکمه «شارژ حساب» اون‌ها رو ببینید. 
😃 آموزش استفاده از هرکدوم از روش‌ها رو هم اونجا براتون گذاشتیم! 

بعد از اینکه حسابتون رو شارژ کردید، میتونید روی دکمه «خرید اشتراک» کلیک کنید و پلن مناسب خودتون رو خریداری کنید و به صورت آنی تحویل بگیرید. به همین سادگی😇

برای دیدن اشتراک‌هایی که قبلا خریداری کردید کافیه روی دکمه «اشتراک‌های من» کلیک کنید🙃
توی این قسمت لیست تمام اشتراک‌های شما بهتون نشون داده میشه. برای دیدن اطلاعات و مدیریت هر کدوم از اون‌ها میتونید روش کلیک کنید و وارد بخش تنظیماتش بشید😉

برای اینکه بدونی چقدر موجودی داری میتونی روی دکمه «اطلاعات حساب» کلیک کنی و اطلاعات بیشتر رو اونجا ببینی🤓

همچنین میتونید با استفاده از دعوت بقیه به ربات، اعتبار هدیه بگیرید😋

💡یک سری سوالات متوالی که ممکنه براتون پیش بیاد رو هم توی کانالمون قرار دادیم که میتونید از این لینک مطلاعه کنید🙋:
<a href='https://t.me'>❔ سوالات متدوال</a>

اگه جواب سوالتون رو در این بخش یا بخش سوالات متداول پیدا نکردید، میتونید از طریق دکمه «پشتیبانی» با پشتیبانی ربات تماس بگیرید. خوشحال میشیم سوالاتتون رو جواب بدیم و مشکلاتتون رو حل کنیم🤗

📞 اگر فروشنده هستید و قصد خرید تعداد بالا دارید، با پشتیبانی تماس بگیرید تا سطح اکانت شما ارتقا پیدا کنه و قابلیت‌های مخصوص فروشندگان براتون فعال بشه🤫
‌‌
"""

_CRYPTO_PAYMENT_HELP = """
❗️ اگر با نحوه پرداخت به وسیله ارز دیجیتال آشنایی ندارید، حتما روی لینک زیر کلیک کنید و آموزش رو مشاهده کنید:
<a href='https://t.me/'>❔ آموزش شارژ حساب با ارز دیجیتال</a>
"""


START_TEXT = config("START_TEXT", default=_START_TEXT)
FORCE_JOIN_TEXT = config("FORCE_JOIN_TEXT", default=_FORCE_JOIN_TEXT)
SUPPORT_TEXT = config("SUPPORT_TEXT", default=_SUPPORT_TEXT)
HELP_TEXT = config("HELP_TEXT", default=_HELP_TEXT)

CRYPTO_PAYMENT_HELP = generate_help(
    config("CRYPTO_PAYMENT_HELP", default=_CRYPTO_PAYMENT_HELP)
)
