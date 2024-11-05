from dotenv import load_dotenv
import aiohttp
import asyncio
import os
import xmltodict
import json

load_dotenv()
icecast_url = os.environ.get("ICECAST_URL")
icecast_mount = os.environ.get("ICECAST_MOUNT")
icecast_admin = os.environ.get("ICECAST_ADMIN")
icecast_password = os.environ.get("ICECAST_PASSWORD")

async def getListeners():
    url = icecast_url + "admin/listclients?mount=" + icecast_mount
    async with aiohttp.ClientSession() as session:
        async with session.get(url, auth=aiohttp.BasicAuth(icecast_admin, icecast_password)) as response:
            if response.status == 200:
                data = xmltodict.parse(await response.text())
                return json.loads(json.dumps(data))
