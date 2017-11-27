from aiohttp import web
import asyncio

async def handle(request):
    ip = request.match_info.get('ip', "Anonymous")
    text = "IP: " + ip

    await asyncio.create_subprocess_shell('nmap -sV ' + ip)

    return web.Response(text = text)


def main():
    app = web.Application()
    app.router.add_get('/{ip}', handle)
    web.run_app(app)


main()
