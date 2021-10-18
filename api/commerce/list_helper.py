def get_index(request, products_count, page):
    max_index = products_count // 10 + 1
    abs_url = request.build_absolute_uri('?page=')
    sort = request.GET.get('sort', None)
    next_val = None if max_index == page else page + 1
    prev_val = None if page == 1 else page - 1
    if next_val is not None:
        next_val = abs_url + str(next_val) + '&sort={}'.format(sort) if sort is not None else abs_url + str(next_val)
    if prev_val is not None:
        prev_val = abs_url + str(prev_val) + '&sort={}'.format(sort) if sort is not None else abs_url + str(prev_val)
    return max_index, prev_val, next_val


def get_index_catalog(request, products_count, page):
    max_index = products_count // 10 + 1
    abs_url = request.build_absolute_uri('?page=')
    sort = request.GET.get('distribute', None)
    next_val = None if max_index == page else page + 1
    prev_val = None if page == 1 else page - 1
    if next_val is not None:
        next_val = abs_url + str(next_val) + '&distribute={}'.format(sort) if sort is not None else abs_url + str(next_val)
    if prev_val is not None:
        prev_val = abs_url + str(prev_val) + '&distribute={}'.format(sort) if sort is not None else abs_url + str(prev_val)
    return max_index, prev_val, next_val
