from aiohttp import web
import asyncio


def is_in_cache(ip):
    if ip in scanned_ip:
        return True
    else:
        return False

def get_ip_to_scan(ip):
    all_ip = ip.split('-') # create array 

    base_ip = (all_ip[0]).split('.')
    del base_ip[-1] # remove start ip from base
    base_ip = '.'.join(base_ip) # concatenate all parts of base ip from array

    start_ip = (all_ip[0]).split('.')[3] # get ip before '-' in url
    last_ip = all_ip[1] # get ip after '-' in url

    return base_ip, start_ip, last_ip

async def scan_ip(ip):
    process = await asyncio.create_subprocess_exec(
        'nmap', '-sV', ip,
        stdout = asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    result = stdout.decode().strip()

    return result

async def handle(request):
    ip = request.match_info.get('ip')
    print('nmap -sV ' + ip)
    scan = ''

    if '-' in ip: # for a range of ip
        base_ip, start_ip, last_ip = get_ip_to_scan(ip)

        for i in range(int(start_ip), int(last_ip) + 1):
            current_ip = str(base_ip) + '.' + str(i)
            print(current_ip) 

            if is_in_cache(current_ip):
                scan += scanned_ip.get(current_ip) # get scan result from cache
                print('IP ' + current_ip + ' found in cache')
            else:
                scan += await scan_ip(current_ip) + "\n\n"
                scanned_ip[current_ip] = scan # add to cache
                
    else: # for a single ip
        if is_in_cache(ip):
            scan = scanned_ip.get(ip) # get scan value from cache
            print('IP ' + ip + ' found in cache')
        else:
            scan = await scan_ip(ip)
            scanned_ip[ip] = scan # add to cache
        
    return web.Response(text = scan)

def main():
    # Sur Windows décommenter les 2 lignes ci-dessous :
    # loop = asyncio.ProactorEventLoop()
    # asyncio.set_event_loop(loop)

    app = web.Application()
    app.router.add_get('/{ip}', handle)
    web.run_app(app)


scanned_ip = {} # scans cache
main()
