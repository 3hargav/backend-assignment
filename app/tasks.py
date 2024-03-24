import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build

from celery import shared_task
from celery.contrib.abortable import AbortableTask

from app.models import ApiKeys, db, Videos, Thumbnails
from app.constants import YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, QUERY, MAX_RESULTS, YOUTUBE_API_URL


def update_to_db(video_data):
    video_ids = [video['id']["videoId"] for video in video_data]

    # Fetching the existing video data from the DB
    existing_videos = {video.id: video for video in Videos.query.filter(Videos.id.in_(video_ids)).all()}
    print("Existing videos found: {}".format(len(existing_videos)))

    thumbnails_by_video_id = {}

    print("Processing the video data")
    c = 0
    for video_item in video_data:
        video_id = video_item['id']['videoId']
        video = existing_videos.get(video_id)

        # Create or update video
        if video is None:
            c += 1
            video = Videos(id=video_id)
        video.title = video_item['snippet']['title']
        video.channel_id = video_item['snippet']['channelId']
        video.description = video_item['snippet']['description']
        video.published_at = datetime.strptime(video_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        db.session.add(video)

        # Store thumbnail data by video ID
        thumbnails_by_video_id[video_id] = video_item['snippet']['thumbnails']

    print("saving {} new videos data to db".format(c))
    # Delete existing thumbnails for a video
    print("deleting the existing thumbnail data")
    Thumbnails.query.filter(~Thumbnails.video_id.in_(video_ids)).delete(synchronize_session=False)

    print("Processing the thumbnails data")
    # update thumbnails
    for video_id, thumbnails_data in thumbnails_by_video_id.items():
        for res, thumbnail_data in thumbnails_data.items():
            thumbnail = Thumbnails(
                resolution=res,
                url=thumbnail_data.get("url"),
                video_id=video_id,
                height=int(thumbnail_data.get("height")),
                width=int(thumbnail_data.get("width"))
            )
            thumbnail.url = thumbnail_data['url']
            thumbnail.video_id = video_id
            db.session.add(thumbnail)

    db.session.commit()
    print("successfully pushed the data into database")


@shared_task(bind=True, base=AbortableTask)
def fetch_youtube_videos(self):
    key_record = ApiKeys.query.filter_by(is_quota_exceeded=False).first()
    print(key_record)
    video_data = []

    if not key_record:
        print("No key found. Please provide the API key..")
    else:
        youtube = build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=key_record.key
        )
        last_x_hrs_datetime = (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'
        try:
            search_response = (
                youtube.search()
                .list(q=QUERY, part="id,snippet", maxResults=MAX_RESULTS, publishedAfter=last_x_hrs_datetime, order="date")
                .execute()
            )
            print("google api client call done")
            video_data = search_response.get("items", [])
            print("fetched {} items from the api".format(len(video_data)))
        except Exception as e:
            # Exception will occur if the quota exceeded than the presribed limit.
            # HttpError (403)
            print("Exception occurred while calling the Youtube API: {}".format(e))
            key_record.is_quota_exceeded = True   # Marking the API_KEY as quota_exceeded in DB
            db.session.commit()

        update_to_db(video_data)
