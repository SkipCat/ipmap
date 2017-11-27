from aiohttp import web
import asyncio

async def handle(request):
    ip = request.match_info.get('ip', "Anonymous")
    text = "IP: " + ip
    print(text)

    process = await asyncio.create_subprocess_shell(
        'nmap -sV ' + ip,
        stdout = asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = stdout.decode().strip()

    return web.Response(text = result)


def main():
    app = web.Application()
    app.router.add_get('/{ip}', handle)
    web.run_app(app)


main()
