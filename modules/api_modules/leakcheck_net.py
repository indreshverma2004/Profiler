import leakcheck

from colorama import Fore


def _get_api_class():
    for name in ("LeakCheckAPI", "LeakCheckAPI_v2", "LeakCheckAPI_Public"):
        if hasattr(leakcheck, name):
            return getattr(leakcheck, name)
    raise ImportError("No supported LeakCheckAPI class found in installed leakcheck package")


def _normalize_result(item):
    if not isinstance(item, dict):
        return {
            'password': None,
            'leak_name': None,
            'leak_date': None,
        }

    password = item.get('line') or item.get('password')
    leak_name = item.get('sources') or item.get('leak_name')
    leak_date = item.get('last_breach') or item.get('leak_date')

    if leak_name is not None:
        leak_name = str(leak_name).replace("'", "").replace("[", "").replace("]", "")

    return {
        'password': password,
        'leak_name': leak_name,
        'leak_date': leak_date,
    }


def leak_check_api(mail):
    full_results = []
    """
    GET YOUR KEY AT https://leakcheck.net/
    """
    keyy = "YOUR_KEY"  # PUT YOUR KEY HERE ONLY
    if keyy == "YOUR_KEY":
        return None

    try:
        api_class = _get_api_class()

        if hasattr(api_class, "set_key"):
            api = api_class()
            api.set_key(keyy)
            api.set_type("email")
            api.set_query(mail)
            result = api.lookup(with_sources=1)
        else:
            api = api_class(api_key=keyy)
            result = api.lookup(mail, query_type="email", limit=10, offset=0)

        if not result:
            return None

        for i in result[0:10]:
            full_results.append(_normalize_result(i))

        if len(full_results) == 0:
            return None
        return full_results
    except Exception:
        return None
