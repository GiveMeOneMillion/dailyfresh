from django.template import Library
register=Library()


@register.filter
def page_list(page):
    plist = page.paginator.page_range
    page_index = page.number
    num_pages = page.paginator.num_pages

    if num_pages> 5:
        if page_index <= 2:
            plist = range(1, 6)
        elif page_index >= num_pages - 1:
            plist = range(num_pages - 4, num_pages + 1)
        else:
            plist = range(page_index - 2, page_index + 3)

    return plist