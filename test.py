str = "PUT / gameserver/status / HTTP/1.1\r\nHost: 127.0.0.1\r\nUser-agent: GameClient/1.0\r\n"
# print(str.split(' / '))
print(str.split('\r\n')[0])