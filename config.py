# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv

load_dotenv()

# 環境変数を参照
import os

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")
