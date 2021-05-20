from TikTokApi import TikTokApi, exceptions
import json
import sys

args = sys.argv
argsLength = len(args)

defaultVideoNumber = 20

if argsLength != 2 and argsLength != 3:
    print('use like this : python main.py [tiktokUsername] [numberofVideos=' + str(defaultVideoNumber) + ']')
    sys.exit()

api = TikTokApi()
numberOfVideos = int(args[2]) if argsLength == 3 else defaultVideoNumber
username = args[1]
try:
    videos = api.byUsername(username, count=numberOfVideos)
except exceptions.TikTokNotFoundError:
    print(json.dumps({'message': 'User not found'}))
    sys.exit()
except:
   print(json.dumps({'message': 'Unknown error'}))
   sys.exit()

print(json.dumps(videos))
