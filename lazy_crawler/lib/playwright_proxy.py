from typing import Optional, Dict
from lazy_crawler.lib.proxy_manager import proxy_manager
from urllib.parse import urlparse


def get_playwright_proxy() -> Optional[Dict[str, str]]:
    """
    Returns a proxy dictionary formatted for Playwright.
    Example output: {"server": "http://myproxy.com:3128", "username": "usr", "password": "pwd"}
    """
    proxy_url = proxy_manager.get_proxy()
    if not proxy_url:
        return None

    parsed = urlparse(proxy_url)

    # For Playwright, the 'server' should not contain credentials if they are passed separately.
    # However, many proxies work fine if you just pass the full URL as 'server'.
    # We'll try to pass it as just the server and credentials separately for better compatibility.
    server = f"{parsed.scheme}://{parsed.hostname}"
    if parsed.port:
        server += f":{parsed.port}"

    proxy_dict = {"server": server}

    if parsed.username:
        proxy_dict["username"] = parsed.username
    if parsed.password:
        proxy_dict["password"] = parsed.password

    return proxy_dict
