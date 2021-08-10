import falcon
import logging
import os

from .render import render_md
from .watchers import WatchgodFileWatcher


logger = logging.getLogger("fileview")
logger.setLevel(logging.DEBUG)


class ReloadResource:

    def __init__(self, file_watcher):
        self.file_watcher = file_watcher

    def __repr__(self):
        return f"{self.__class__.__name__}(file_watcher={repr(self.file_watcher)})"

    async def on_websocket(self, req: falcon.Request, ws: falcon.asgi.WebSocket):
        try:
            await ws.accept()
            async for event in self.file_watcher.watch():
                logger.info(f"{self}: detected changes: {event}")
                await ws.send_text('reload')
        except falcon.WebSocketDisconnected:
            logger.info(f"{self}: client disconnected")
        except:
            logger.exception(f"{self}: failed to watch for changes")
            raise


class WatchResource:

    async def on_get(self, req: falcon.Request, resp: falcon.Response, target_file: str):
        path = bytes.fromhex(target_file).decode('utf-8')
        assert os.path.isfile(path)
        from .app import app, get_all_routes
        routes = dict(get_all_routes(app))
        reload_route = f'/reload/{target_file}'
        if reload_route not in routes:
            file_watcher = WatchgodFileWatcher(path)
            app.add_route(f'/reload/{target_file}', ReloadResource(file_watcher))

        reloader_url = f"ws://{req.host}:{req.port}/reload/{target_file}"
        html = render_md(path, reloader_url=reloader_url)

        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = html

