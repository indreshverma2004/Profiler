import requests, re
from bs4 import BeautifulSoup


def facebook_search(name, pren):
    url = "https://fr-fr.facebook.com/public/{}-{}".format(pren, name)
    try:
        page = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"}).text
    except Exception:
        return []

    soup = BeautifulSoup(page, "html.parser")
    results = []
    seen = set()

    for a in soup.find_all('a', href=True):
        href = a.get('href', '')
        text = a.get_text(' ', strip=True)
        if not href or not text:
            continue
        if 'facebook.com' in href and 'public/' not in href:
            candidate = href
            if candidate.startswith('/'):
                candidate = 'https://fr-fr.facebook.com' + candidate
            if candidate.startswith('http'):
                profile_name = text.strip()
                if name.lower() in profile_name.lower() or pren.lower() in profile_name.lower():
                    if candidate not in seen:
                        seen.add(candidate)
                        results.append(f"{profile_name} | {candidate}")

    if results:
        return results[:20]

    nameAccount = re.findall(r'width="72" height="72" alt="([a-zA-Z0-9_ é,]+)"', page, flags=re.I)
    for i in nameAccount:
        if name.lower() in i.lower() and pren.lower() in i.lower():
            if i not in seen:
                seen.add(i)
                results.append(f"{i} | https://fr-fr.facebook.com/public/{pren}-{name}")

    return results[:20]

'''
This code cand be found at : 
https://github.com/lulz3xploit/LittleBrother/blob/master/core/facebookSearchTool.py
'''
