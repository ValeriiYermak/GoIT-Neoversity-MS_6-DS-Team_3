
class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags else []

    def edit_title(self, new_title):
        self.title = new_title

    def edit_content(self, new_content):
        self.content = new_content

    def edit_tags(self, new_tags):
        self.tags = new_tags

