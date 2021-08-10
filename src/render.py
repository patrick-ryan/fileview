import markdown
import os

from jinja2 import Environment, FileSystemLoader


def render_md(path, reloader_url=None):
    title = os.path.basename(path)
    with open(path, 'r') as f:
        content = markdown.markdown(f.read())

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('page.html')
    html = template.render(
        title=title,
        content=content,
        reloader_url=reloader_url,
    )
    return html
