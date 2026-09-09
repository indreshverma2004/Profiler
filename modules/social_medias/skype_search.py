import re
from urllib.parse import quote

import requests


def skype_searchh(name, pren):
    query = f'"{pren} {name}" site:skypli.com'
    url = f'https://html.duckduckgo.com/html/?q={quote(query)}'
    try:
        response = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except Exception:
        return []

    results = []
    seen = set()
    for match in re.findall(r'https?://(?:www\.)?skypli\.com/profile/[^\"\'\s<>]+', response.text):
        if match not in seen:
            seen.add(match)
            results.append(match)
    if results:
        return results[:10]
    return [f'https://www.skypli.com/search/{quote(pren + " " + name)}']
