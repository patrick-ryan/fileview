import watchgod


class WatchgodFileWatcher:

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"{self.__class__.__name__}(path={repr(self.path)})"

    async def watch(self):
        async for changes in watchgod.awatch(self.path):
            yield changes
