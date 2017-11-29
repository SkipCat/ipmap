from aiohttp import web
import asyncio

async def handle(request):
    ip = request.match_info.get('ip')
    print('nmap -sV ' + ip)
    result = ''

    if '-' in ip:
        base_ip, start_ip, last_ip = ipToScan(ip)
        
        for i in range(int(start_ip), int(last_ip) + 1):
            print(str(base_ip) + '.' + str(i))
            result += await scan_ip(str(base_ip) + '.' + str(i)) + "\n\n"
            print(result)

        return web.Response(text = result)

    else:
        await scan_ip(ip)


async def scan_ip(ip):
    process = await asyncio.create_subprocess_exec(
        'nmap', '-sV', ip,
        stdout = asyncio.subprocess.PIPE
    )
    stdout, _ = await process.communicate()
    result = stdout.decode().strip()

    return result


def ipToScan(ip):
    all_ip = ip.split('-') # create array 

    base_ip = (all_ip[0]).split('.')
    del base_ip[-1] # remove start ip from base
    base_ip = '.'.join(base_ip) # concatenate all parts of base ip from array

    start_ip = (all_ip[0]).split('.')[3] # get ip before '-' in url
    last_ip = all_ip[1] # get ip after '-' in url

    return base_ip, start_ip, last_ip


def main():
    # Sur Windows décommenter les 2 lignes ci-dessous :
    # loop = asyncio.ProactorEventLoop()
    # asyncio.set_event_loop(loop)

    app = web.Application()
    app.router.add_get('/{ip}', handle)
    web.run_app(app)


main()
