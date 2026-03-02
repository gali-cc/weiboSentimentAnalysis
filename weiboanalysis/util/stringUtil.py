import re


def remove_all_tags(html_text):
    return re.sub(r'<[^>]+>', '', html_text)


def remove_urls_clean(text):
    no_urls = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.\-?=%&:#@$,;+!]*', '', text)
    return re.sub(r'\s+', ' ', no_urls).strip()


def clean_string(text):
    text = remove_urls_clean(text)
    text = remove_all_tags(text)
    pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6dfa-zA-Z0-9]')
    return ''.join(pattern.findall(text))
