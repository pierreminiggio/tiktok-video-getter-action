import requests

def get_proxy(proxy_protocol = 'https', countries = 'en', excluded_proxies = []):
    proxies_request = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=' + proxy_protocol + '&timeout=10000&country=' + countries)
    if proxies_request.status_code != 200:
        raise Exception('Couldn\'t get proxy list : Bad HTTP code')

    proxies_request_content = proxies_request.text

    if not proxies_request_content:
        raise Exception('Couldn\'t get proxy list : Empty list')

    proxy_ips_to_try = proxies_request_content.splitlines()

    for proxy_ip_to_try in proxy_ips_to_try:
        if not proxy_ip_to_try:
            continue

        proxy_to_try = proxy_protocol + '://' + proxy_ip_to_try
        
        if len(excluded_proxies) and proxy_to_try in excluded_proxies:
            continue

        try:
            trying_proxy_request = requests.get('https://api.myip.com', proxies={
                'https': proxy_to_try
            }, timeout=5)
        except requests.exceptions.ProxyError:
            continue
        except:
            continue

        if trying_proxy_request.status_code == 200:
            return proxy_to_try

    raise Exception('No working proxy at this time')
