FileView Project


fileview render ./README.md [/output]
    (similar interface to unix cp)

    -> render.py

        -> render

fileview serve [--watch ./README.md]

    -> server.py
        default_port = 4437
        reloaders = {<hash>: reloader}
        
        /watch/<hash>

            -> decode(hash)

            -> add_reloader(path)

                -> reloader.add_watcher(path)

                    -> watcher(path, callback) [watchgod]

                        -> callback

                            -> reloader.notify()
                                on_fail = reloader.close() -> watcher.close()

            -> render(reloader.url)

            -> resp(html)

        /reload/<hash>

fileview watch ./README.md [/output]

    -> watch.py
        default_port = 4437

        -> open('<localhost>/watch/<hash>')
