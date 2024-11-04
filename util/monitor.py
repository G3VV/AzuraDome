from dotenv import load_dotenv
import requests
import os

load_dotenv()
icecast_url = os.environ.get("ICECAST_URL")
icecast_mount = os.environ.get("ICECAST_MOUNT")

def getListeners():
    url = icecast_url + "admin/listclients?mount=" + icecast_mount
    