import falcon.asgi
import logging

from .resources import WatchResource


logging.basicConfig()

app = falcon.asgi.App()

app.add_route('/watch/{target_file}', WatchResource())


def get_all_routes(api):
    routes_list = []

    def get_children(node):
        if len(node.children):
            for child_node in node.children:
                get_children(child_node)
        else:
            routes_list.append((node.uri_template, node.resource))
    [get_children(node) for node in api._router._roots]
    return routes_list
