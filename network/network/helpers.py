from django.core.paginator import Paginator


def prepare_post_page(posts, page, num_posts):
    posts_paginated = Paginator(posts, num_posts)
    posts_page = posts_paginated.page(page)

    for post in posts_page:
        print(post.likes.all())

    if posts_page.has_previous():
        previous_page = page - 1
    else:
        previous_page = None
    if posts_page.has_next():
        next_page = page + 1
    else:
        next_page = None

    pn = (previous_page, next_page)

    return (posts_page, pn)
