from enum import Enum
from fp.fp import FreeProxy
import json
from proxyscrape.get_proxy import get_proxy
import sys
from TikTokApi import TikTokApi, exceptions

args = sys.argv
argsLength = len(args)

defaultVideoNumber = 20

if argsLength != 2 and argsLength != 3:
    print('use like this : python main.py [tiktokUsername] [numberofVideos=' + str(defaultVideoNumber) + ']')
    sys.exit()

numberOfVideos = int(args[2]) if argsLength == 3 else defaultVideoNumber
username = args[1]

class ProxyStrategy(Enum):
    NONE = 0
    FREE_PROXY = 1
    PROXYSCRAPE = 2

lastProxyStrategyIndex = ProxyStrategy.PROXYSCRAPE.value

numberOfFreeProxyProxiesToTry = 3
triedFreeProxyProxies = []

numberOfProxyScrapeProxiesToTry = 3
triedProxyScrapeProxies = []

def getVideos(proxyStrategy = ProxyStrategy.NONE.value): 
    proxy = None

    if proxyStrategy == ProxyStrategy.FREE_PROXY.value: 
        try:
            proxy = FreeProxy(https=True, rand=True).get()
        except Exception as e:
            if len(triedFreeProxyProxies) < numberOfFreeProxyProxiesToTry:
                triedFreeProxyProxies.append(proxy)
                getVideos(ProxyStrategy.FREE_PROXY.value)
                return
            getVideos(ProxyStrategy.PROXYSCRAPE.value)
            return

    if proxyStrategy == ProxyStrategy.PROXYSCRAPE.value: 
        try:
            proxy = get_proxy(excluded_proxies=triedProxyScrapeProxies)
        except Exception as e:
            print(json.dumps({'message': 'Couldn\'t find a working Proxy : ' + str(e) }))
            sys.exit()

    videos = []
    try:
        with TikTokApi(proxy=proxy) as api:
            videosGenerator = api.user(username=username).videos(count=numberOfVideos)
            for video in videosGenerator:
                videos.append(video)
    except exceptions.CaptchaException:
        if (proxyStrategy == ProxyStrategy.FREE_PROXY.value):
            if len(triedFreeProxyProxies) < numberOfFreeProxyProxiesToTry:
                triedFreeProxyProxies.append(proxy)
                getVideos(ProxyStrategy.FREE_PROXY.value)
                return
        
        if (proxyStrategy == ProxyStrategy.PROXYSCRAPE.value):
            if len(triedProxyScrapeProxies) < numberOfProxyScrapeProxiesToTry:
                triedProxyScrapeProxies.append(proxy)
                getVideos(ProxyStrategy.PROXYSCRAPE.value)
                return

        if proxyStrategy == lastProxyStrategyIndex:
            print(json.dumps({'message': 'TikTok blocked the request using a Captcha'}))
            sys.exit()

        getVideos(proxyStrategy + 1)
        return
    except exceptions.NotFoundException:
        print(json.dumps({'message': 'User not found'}))
        sys.exit()
    except Exception as e:
        if (proxyStrategy == ProxyStrategy.FREE_PROXY.value):
            if len(triedFreeProxyProxies) < numberOfFreeProxyProxiesToTry:
                triedFreeProxyProxies.append(proxy)
                getVideos(ProxyStrategy.FREE_PROXY.value)
                return
        
        if (proxyStrategy == ProxyStrategy.PROXYSCRAPE.value):
            if len(triedProxyScrapeProxies) < numberOfProxyScrapeProxiesToTry:
                triedProxyScrapeProxies.append(proxy)
                getVideos(ProxyStrategy.PROXYSCRAPE.value)
                return

        if proxyStrategy == lastProxyStrategyIndex:
            print(json.dumps({'message': str(e)}))
            sys.exit()

        getVideos(proxyStrategy + 1)
        return

    print(json.dumps(videos))

getVideos()
