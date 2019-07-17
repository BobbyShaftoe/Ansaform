
from docutils import nodes

def setup(app):

    project_url = app.config.__dict__['_raw_config']['project_repo_url']
    project_module = app.config.__dict__['_raw_config']['main_module_file']

    app.add_role('project_attribute', insert_attribute(project_module))
    app.add_role('project_url', insert_url(project_url))


def insert_attribute(attribute):
    def role(name, rawtext, lineno, inliner, options={}, content={}):
        node = nodes.paragraph()
        node.append(nodes.Text(attribute, attribute))
        return [node], []
    return role


def insert_url(url):
    def role(name, rawtext, text, lineno, inliner, options={}, content={}):
        node = nodes.reference(rawtext, text=url, refuri=url, **options)
        return [node], []
    return role


