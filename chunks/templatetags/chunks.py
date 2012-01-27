from django import template
from django.db import models

register = template.Library()

Chunk = models.get_model('chunks', 'chunk')
CACHE_PREFIX = "chunk_"

def do_get_chunk(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError, "%r tag should have 2 arguments" % (tokens[0],)
    else:
        tag_name, key = tokens
    return ChunkNode(key)
    
class ChunkNode(template.Node):
    def __init__(self, key):
        self.key = key
    
    def render(self, context):
        if self.key[0] == self.key[-1] and self.key[0] in ('"', "'"):
            key = self.key[1:-1]
        else:
            key = template.Variable(self.key).resolve(context)
        try:
            c = Chunk.objects.get(key=key)
            content = c.content
        except Chunk.DoesNotExist:
            content = ''
        return content
        
register.tag('chunk', do_get_chunk)
