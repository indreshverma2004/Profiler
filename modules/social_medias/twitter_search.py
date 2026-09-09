import requests, re
from bs4 import BeautifulSoup
from urllib.parse import quote


def _safe_get(url):
    return requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})


def twitter_search(name, pren):
    query = f"{pren} {name}"
    urls = [
        f"https://www.sotwe.com/search/{pren} {name}",
        f"https://duckduckgo.com/html/?q={quote(query + ' site:twitter.com')}"
    ]

    for url in urls:
        try:
            r = _safe_get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            if "sotwe.com" in url:
                usernames = []
                for i in soup.find_all('div', {'class': 'v-list-item__subtitle caption'}):
                    value = i.text.strip()
                    if value:
                        usernames.append(value)
                if usernames:
                    return usernames
                continue

            results = []
            seen = set()
            for link in soup.select('a.result__a'):
                href = link.get('href', '')
                text = link.get_text(' ', strip=True)
                match = re.search(r'https?://(?:www\.)?twitter\.com/([A-Za-z0-9_]+)', href)
                if match:
                    username = '@' + match.group(1)
                    profile = 'https://twitter.com/' + match.group(1)
                    display = f"{username} | {profile}"
                    if display not in seen:
                        seen.add(display)
                        results.append(display)
                elif text:
                    user_match = re.search(r'@?([A-Za-z0-9_]{3,15})', text)
                    if user_match:
                        username = '@' + user_match.group(1)
                        profile = 'https://twitter.com/' + user_match.group(1)
                        display = f"{username} | {profile}"
                        if display not in seen:
                            seen.add(display)
                            results.append(display)

            if results:
                return results[:20]

        except Exception:
            continue

    return [f'https://twitter.com/search?q={quote(query)}&src=typed_query&f=user']

