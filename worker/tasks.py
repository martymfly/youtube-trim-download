import os
import requests
import subprocess
import yt_dlp
from celery import Celery
from dotenv import load_dotenv
from glob import glob

load_dotenv()

REDIS_LOCAL_URL = "redis://localhost:6379"
UPLOAD_LOCAL_URL = "http://localhost:8000/uploadfromworker"
UPLOAD_SECRET_KEY = os.environ.get("UPLOAD_SECRET_KEY")
UPLOAD_URL = os.environ.get("UPLOAD_URL", UPLOAD_LOCAL_URL)
VIDEOS_PATH = "videos/"

celery = Celery(
    "tasks",
    broker=os.environ.get("REDIS_URL", REDIS_LOCAL_URL),
    backend=os.environ.get("REDIS_URL", REDIS_LOCAL_URL),
)


def create_videos_folder():
    try:
        if not os.path.exists("videos"):
            os.mkdir("videos")
    except Exception as e:
        print(e)


create_videos_folder()


def get_adjusted_start(val):
    if val > 4:
        return val - 4
    else:
        return val


def get_path(id, quality):
    files = glob(f"{VIDEOS_PATH}*{id}*")
    for v in files:
        if f"qi{str(quality)}" in v:
            path = v
    print(path)
    return path


@celery.task
def trim(url, quality, start, end, ip):
    start = int(start)
    end = int(end) + 1
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            id = result["id"]

            download_video_command = [
                "yt-dlp",
                "-f",
                f"{quality}+ba",
                url,
                "-o",
                VIDEOS_PATH + "%(title)s-%(id)s-qi%(format_id)s.%(ext)s",
            ]

            p1 = subprocess.Popen(download_video_command, stdin=subprocess.PIPE)
            p1.wait()

            original_video_path = get_path(id, quality)
            original_video_name = original_video_path.split(".")[0]
            original_video_ext = original_video_path.split(".")[-1]

            if original_video_ext == "m4a":
                final_ext = "mp3"
            else:
                final_ext = original_video_ext

            final_file_name = (
                f"{original_video_name}-s{start}-e{end}-trimmed.{final_ext}"
            )

            audio_command = [
                "ffmpeg",
                "-ss",
                str(start),
                "-i",
                original_video_path,
                "-t",
                str(end),
                "-c:v",
                "copy",
                "-c:a",
                "libmp3lame",
                "-q:a",
                "4",
                final_file_name,
                "-y",
            ]

            video_command = [
                "ffmpeg",
                "-ss",
                str(start),
                "-i",
                original_video_path,
                "-t",
                str(end),
                "-avoid_negative_ts",
                "make_zero",
                "-c",
                "copy",
                final_file_name,
                "-y",
            ]

            if original_video_ext == "m4a":
                p2 = subprocess.Popen(audio_command, stdin=subprocess.PIPE)
                p2.wait()
            else:
                p2 = subprocess.Popen(video_command, stdin=subprocess.PIPE)
                p2.wait()

            file_to_upload = {"file": open(final_file_name, "rb")}
            headers = {"secret_key": UPLOAD_SECRET_KEY}
            upload_result = requests.post(
                UPLOAD_URL, files=file_to_upload, headers=headers
            )
            return upload_result.json()
    except Exception as e:
        print(e, "was handled")
        return {"success": False, "data": None, "message": "Something went wrong"}
