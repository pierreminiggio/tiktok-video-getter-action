from TikTokApi import TikTokApi
import json
import sys

args = sys.argv
argsLength = len(args)

defaultVideoNumber = 20

if argsLength != 2 and argsLength != 3:
    print('use like this : python main.py [tiktokUsername] [numberofVideos=' + str(defaultVideoNumber) + ']')
    sys.exit()

api = TikTokApi()
numberOfVideos = args[2] if argsLength == 3 else defaultVideoNumber
username = args[1]
user_videos = api.byUsername(username, count=numberOfVideos)
print(json.dumps(user_videos))
