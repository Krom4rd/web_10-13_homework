# from django import template

# register = template.Library()


def tags(quote_tags):
    return ', '.join([str(name) for name in quote_tags.all()])

# # def authors(note_authors):
# #     return ', '.join([str(name) for name in note_authors.all()])


# register.filter('tags', tags)

from django import template

register = template.Library()

def author(quote_authors):
    return ''.join([str(name) for name in quote_authors.all()])

def tags(quote_tags):
    return ', '.join([str(name) for name in quote_tags.all()])

def tags_list(quote_tags):
    return [str(name) for name in quote_tags.all()]

def author_id(quote_authors):
    author_id = quote_authors.all()[0].id
    return author_id

register.filter('author_id', author_id)

register.filter('author', author)

register.filter('tags', tags)

register.filter('tags_list', tags_list)
