import re
from urllib.parse import quote

import requests


def _search_public(query, site=None):
    q = query if site is None else f'{query} site:{site}'
    url = f'https://html.duckduckgo.com/html/?q={quote(q)}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, timeout=15, headers=headers)
        response.raise_for_status()
    except Exception:
        return []

    matches = []
    for link in re.findall(r'<a rel="nofollow" class="result-link" href="(.*?)">', response.text):
        decoded = link.replace('\\/', '/')
        if 'linkedin.com' in decoded.lower():
            matches.append(decoded)
    return matches


def linkedin_search(name, pren):
    query = f'"{pren} {name}" LinkedIn'
    results = _search_public(query, 'linkedin.com')
    if not results:
        return [f'https://www.linkedin.com/search/results/people/?keywords={quote(f"{pren} {name}")}']
    seen = set()
    final = []
    for item in results:
        if 'linkedin.com/in/' in item.lower() or 'linkedin.com/pub/' in item.lower():
            if item not in seen:
                seen.add(item)
                final.append(item)
    if final:
        return final[:10]
    return [f'https://www.linkedin.com/search/results/people/?keywords={quote(f"{pren} {name}")}']


def official_linkedin_search(name, pren):
    return None


