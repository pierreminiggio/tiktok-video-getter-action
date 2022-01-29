from enum import Enum
from fp.fp import FreeProxy
import json
from proxyscrape import get_proxy
import sys
from TikTokApi import TikTokApi, exceptions

args = sys.argv
argsLength = len(args)

defaultVideoNumber = 20

if argsLength != 2 and argsLength != 3:
    print('use like this : python main.py [tiktokUsername] [numberofVideos=' + str(defaultVideoNumber) + ']')
    sys.exit()

api = TikTokApi()
numberOfVideos = int(args[2]) if argsLength == 3 else defaultVideoNumber
username = args[1]

class ProxyStrategy(Enum):
    NONE = 0
    FREE_PROXY = 1
    PROXYSCRAPE = 2

lastProxyStrategyIndex = ProxyStrategy.PROXYSCRAPE

def getVideos(proxyStrategy = ProxyStrategy.NONE): 
    proxy = None
    
    if proxyStrategy == ProxyStrategy.FREE_PROXY: 
        try:
            proxy = FreeProxy(https=True).get()
        except Exception as e:
            getVideos(ProxyStrategy.PROXYSCRAPE)
            return

    if proxyStrategy == ProxyStrategy.FREE_PROXY: 
        try:
            proxy = get_proxy()
        except Exception as e:
            print(json.dumps({'message': 'Couldn\'t find a working Proxy'}))
            sys.exit()

    try:
        videos = api.by_username(username, count=numberOfVideos, proxy=proxy)
    except exceptions.TikTokCaptchaError:
        if proxyStrategy == lastProxyStrategyIndex:
            print(json.dumps({'message': 'TikTok blocked the request using a Captcha'}))
            sys.exit()
        getVideos(proxyStrategy + 1)
    except exceptions.TikTokNotFoundError:
        print(json.dumps({'message': 'User not found'}))
        sys.exit()
    except Exception as e:
        print(json.dumps({'message': str(e)}))
        sys.exit()

    print(json.dumps(videos))

getVideos()
