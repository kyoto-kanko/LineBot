import config
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage


def main():
    # 対象のサイトのURL
    url = "https://rightcode.co.jp/blog"
    # サイトのHTML情報を取得
    res = requests.get(url)
    # 取得したHTML情報をパース
    soup = BeautifulSoup(res.text, "html.parser")
    # 一番最新の記事を取得
    new_topics = soup.find(class_="p-article01__title")
    # 取得した情報から遷移先のリンクを取得
    element_a = new_topics.find("a")
    new_topics_url = element_a.get("href")
    # 取得した最新記事のリンクにアクセス
    new_topics_res = requests.get(new_topics_url)
    new_topics_soup = BeautifulSoup(new_topics_res.text, "html.parser")
    # 最新記事の投稿日を取得
    submission_date = new_topics_soup.find(class_="mod_date").text
    submission_title = new_topics_soup.find(class_="p-entry__title").text
    # 今日の日付を取得(UTC 定世界時間)
    today = datetime.now() + timedelta(hours=9)
    # 昨日の日付を取得(UTC 定世界時間)
    yesterday = today - timedelta(1)
    verification_date = yesterday.strftime("%Y.%m.%d")

    # 最新記事が昨日の日付を一致した場合最新投稿ありと判定
    if verification_date == submission_date:
        # LINEのAPIに接続して取得した情報を送信
        line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
        messages = TextSendMessage(
            text=f"おはようございます！！記事が更新されてますよ〜！\n{submission_title}\n{new_topics_url}"
        )
        line_bot_api.push_message(config.USER_ID, messages=messages)


if __name__ == "__main__":
    main()
