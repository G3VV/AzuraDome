from util.monitor import getListeners, icecast_url, icecast_mount, icecast_admin, icecast_password
import asyncio
import aiohttp


protection_task = None

async def defence(stop_event):
    while not stop_event.is_set():
        data = await getListeners()
        client_ips = {}
        
        if int(data['icestats']['source']['listeners']) > 1:
            client_ips = {client['ID']: {'IP': client['IP'], 'Connected': client['Connected']} 
                          for client in data['icestats']['source']['listener']}
            
            #sorted_clients = sorted(client_ips.items(), key=lambda item: item[1]['Connected'])
            #print(sorted_clients)
            #for i in range(len(sorted_clients)):
            #    for j in range(i + 1, len(sorted_clients)):
            #        if int(sorted_clients[j][1]['Connected']) - int(sorted_clients[i][1]['Connected']) > 5:
            #            print

            unique_ips = {}
            ip_count = {}
            
            for id, info in client_ips.items():
                ip = info['IP']
                if ip not in ip_count:
                    ip_count[ip] = 0
                ip_count[ip] += 1
            
            for id, info in client_ips.items():
                ip = info['IP']
                if ip_count[ip] > 1:
                    if ip not in [entry['IP'] for entry in unique_ips.values()]:
                        unique_ips[id] = info
                else:
                    unique_ips[id] = info
            
            ids_to_remove = [id for id in client_ips if id not in unique_ips]
            for id in ids_to_remove:
                url = icecast_url + "admin/killclient?mount=" + icecast_mount + "&id=" + id
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, auth=aiohttp.BasicAuth(icecast_admin, icecast_password)) as response:
                        if response.status == 200:
                            print(f"Kicked {client_ips[id]['IP']} connected for {client_ips[id]['Connected']} seconds")

        await asyncio.sleep(2)

async def startProtection():
    global protection_task
    if protection_task is None or protection_task.done():
        stop_event = asyncio.Event()
        protection_task = asyncio.create_task(defence(stop_event))
        return stop_event, protection_task
    else:
        return None, protection_task

async def stopProtection():
    global protection_task
    if protection_task is not None:
        stop_event, task = protection_task.get_coro().cr_frame.f_locals['stop_event'], protection_task
        stop_event.set()
        await task
        protection_task = None
