from dotenv import load_dotenv
import aiohttp
import asyncio
import os
import xmltodict
import json
from pymongo import MongoClient

load_dotenv()
icecast_url = os.environ.get("ICECAST_URL")
icecast_mount = os.environ.get("ICECAST_MOUNT")
icecast_admin = os.environ.get("ICECAST_ADMIN")
icecast_password = os.environ.get("ICECAST_PASSWORD")

mongo_url = os.environ.get("MONGO_URL")
mongo_db = os.environ.get("MONGO_DB")
mongo_collection = os.environ.get("MONGO_COLLECTION")

client = MongoClient(mongo_url)
db = client[f"{mongo_db}"]
collection = db[f"{mongo_collection}"]

async def getListeners():
    url = icecast_url + "admin/listclients?mount=" + icecast_mount
    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=aiohttp.BasicAuth(icecast_admin, icecast_password)) as response:
            if response.status == 200:
                data = xmltodict.parse(await response.text())
                return json.loads(json.dumps(data))
            
async def startMonitor():
    while True:
        listeners = await getListeners()
        asyncio.sleep(2)
            



