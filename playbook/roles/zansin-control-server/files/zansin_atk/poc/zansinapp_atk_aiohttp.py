#!/usr/bin/env python
# coding: UTF-8
import sys
from aiohttp import web
from pathlib import Path
from aiohttp.web_runner import GracefulExit

args = sys.argv
if len(args) != 3:
    print("usage: zansinapp_atk_aiohttp.py <host> <port>")
    sys.exit(1)

host = args[1]
port = args[2]


async def stopserver(request):
    print("======== Stop WebServer ========")
    raise GracefulExit()

app = web.Application()
app.add_routes([
    web.get('/stopserver', stopserver),
    web.static('/', path=str(Path.cwd().joinpath('public')), show_index=False)
    ])

if __name__ == '__main__':
    web.run_app(app, host=host, port=int(port))

