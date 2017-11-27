from aiohttp import web
import asyncio

async def handle(request):
    ip = request.match_info.get('ip', "Anonymous")
    text = "IP: " + ip

    create = asyncio.create_subprocess_shell('nmap -sV ' + ip)    
    loop = asyncio.get_event_loop()
    proc = loop.run_until_complete(create)

    exitcode = loop.run_until_complete(proc.wait())
    assertEqual(exitcode, 7)

    return web.Response(text = exitcode)

def main():
    app = web.Application()
    app.router.add_get('/{ip}', handle)
    web.run_app(app)


main()
