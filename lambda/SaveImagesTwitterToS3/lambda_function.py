import datetime
import json
import logging
import os
from typing import NamedTuple
from urllib.request import urlopen

import boto3
import tweepy

# Get environment variables
DB_NAME = os.environ["DB_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
TWITTER_API_KEY = os.environ["TWITTER_API_KEY"]
TWITTER_API_SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
WRITE_HEADER = os.environ["WRITE_HEADER"]
LOG_LEVEL = os.environ["LOG_LEVEL"]

# Client initialization
ssm_client = boto3.client("ssm")
s3_client = boto3.client("s3")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DB_NAME)

# set logging
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)


class ImgMaster(NamedTuple):
    url: str
    current_key: str
    next_key: str
    id: str
    item: dict


def get_value_from_ssm(key: str) -> str:
    value = ssm_client.get_parameter(
        Name=key,
        WithDecryption=True
    )
    return value["Parameter"]["Value"]


def tag_strf_query_paramater(tag: dict) -> str:
    return "&".join(f"{k}={v}" for k, v in tag.items())


def s3_upload(data: bin, key: str) -> str:
    logger.info(f"s3 upload: {key}")
    res = s3_client.put_object(
        Body=data,
        Bucket=BUCKET_NAME,
        Key=key,
        Tagging=tag_strf_query_paramater(
            {
                "creater": "sdk",
                "project": "SaveImagesTwitterToS3"
            }
        )
    )
    return s3_to_jst_isformat(res["ResponseMetadata"]["HTTPHeaders"]["date"])


def put_db(img_info: dict) -> None:
    table.put_item(
        Item=img_info
    )


def get_write_header() -> str:
    res = table.get_item(
        Key={
            "partition_key": WRITE_HEADER
        }
    )
    logger.info(
        f"get write header: {json.dumps(res, indent=2, ensure_ascii=False)}")
    return res["Item"]["max_id"]


def download_img(url: str) -> bin:
    logger.info(f"download img: {url}")
    with urlopen(url) as twitter_img:
        return twitter_img.read()


def rebuild_url(before_url: str) -> str:
    # https://pbs.twimg.com/media/hogehoge.jpg
    # https://pbs.twimg.com/media/hogehoge?format=png&name=large
    # に変更することで, png画像を取得することが出来る
    return f"{before_url[:-4]}?format=png&name=large"


def to_jst_isoformat(timestr: str, format: str) -> str:
    tt = datetime.datetime.strptime(timestr, format)
    jst_delta = datetime.timedelta(hours=9)
    jst_zone = datetime.timezone(jst_delta)
    tt += jst_delta
    return tt.astimezone(jst_zone).isoformat()


def twitter_to_jst_isformat(time_str: str) -> str:
    return to_jst_isoformat(time_str, "%a %b %d %H:%M:%S +0000 %Y")


def s3_to_jst_isformat(time_str: str) -> str:
    return to_jst_isoformat(time_str, "%a, %d %b %Y %H:%M:%S GMT")


def get_likes_from_twitter(max_id: str = None) -> list:

    consumer_key = get_value_from_ssm(TWITTER_API_KEY)
    consumer_secret = get_value_from_ssm(TWITTER_API_SECRET_KEY)
    access_token = get_value_from_ssm(TWITTER_ACCESS_TOKEN)
    access_token_secret = get_value_from_ssm(TWITTER_ACCESS_TOKEN_SECRET)

    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    if max_id:
        return [like._json for like in api.get_favorites(max_id=max_id)]
    else:
        return [like._json for like in api.get_favorites()]


def service() -> list:
    max_id = get_write_header()
    likes = get_likes_from_twitter(max_id)
    img_items = []
    for like in likes:
        if "extended_entities" not in like.keys():
            continue
        if "media" not in like["extended_entities"].keys():
            continue
        for idx, extended_entity in enumerate(like["extended_entities"]["media"]):
            if extended_entity["type"] != "photo":
                continue
            item = {
                "url": rebuild_url(extended_entity["media_url_https"]),
                "partition_key": f"test/{like['id_str']}_{str(idx)}.png",
                "id": like["id_str"],
                "created_at": twitter_to_jst_isformat(like["created_at"]),
                "user_id": like["user"]["id_str"],
                "user_name": like["user"]["name"],
                "user_screen_name": like["user"]["screen_name"],
            }
            img_items.append(item)
    next_key = "None"
    result = []
    for item in img_items[::-1]:
        result.append(ImgMaster(
            url=item["url"],
            current_key=item["partition_key"],
            id=item["id"],
            next_key=next_key,
            item=item
        ))
        next_key = item["partition_key"]
    return result[::-1]


def controller() -> None:
    img_masters = service()
    if len(img_masters) < 1:
        return
    for a_img_master in img_masters:
        img = download_img(a_img_master.url)
        s3_upload_at = s3_upload(img, a_img_master.current_key)
        temp = {
            "s3_upload_at": s3_upload_at,
            "next_key": a_img_master.next_key,
        }
        img_info = temp | a_img_master.item
        put_db(img_info)
    put_db({
        "partition_key": WRITE_HEADER,
        "max_id": img_masters[-1].current_key
    })


def handler(event, context):
    logger.info("Lambda Start!")
    try:
        controller()
        return 200
    except Exception as e:
        print(e)
        return 400


if __name__ == "__main__":
    controller()
