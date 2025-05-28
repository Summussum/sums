import json

def get_query_pages(values, page_size):
    i, j = 0, page_size
    pages = []
    query_length = len(values)
    while i < query_length:
        pages.append(values[i:j])
        i += page_size
        j += page_size
    if not pages:
        pages.append([])
    return pages


def get_page_links(request, page_num, base_url):
    page_count = len(json.loads(request.session["records_pages"]))
    prev_page, next_page = page_num-1, page_num+1
    base_url = f'style="text-decoration: underline;" hx-get={base_url}'
    page_links = {"first_link": base_url+'1', "prev_link": base_url+str(prev_page), "next_link": base_url+str(next_page), "last_link": base_url+str(page_count), "page_num": page_num, "page_count": page_count}
    if prev_page < 1:
        page_links["prev_link"] = ""
    if next_page > page_count:
        page_links["next_link"] = ""
    return page_links