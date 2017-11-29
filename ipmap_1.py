import asyncio
from aiohttp import web

async def handle(request):
    ip = request.match_info.get('ip')
    print("nmap -sV " + ip)

    process = await asyncio.create_subprocess_exec(
        'nmap', '-sV', ip,
        stdout = asyncio.subprocess.PIPE
    )

    stdout, _ = await process.communicate()
    result = stdout.decode().strip()

    return web.Response(text = result)


def main():
    # Sur Windows décommenter les 2 lignes ci-dessous :
    # loop = asyncio.ProactorEventLoop()
    # asyncio.set_event_loop(loop)

    app = web.Application()
    app.router.add_get('/{ip}', handle)
    web.run_app(app)


main()
