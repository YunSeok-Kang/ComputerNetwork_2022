str = "PUT gameserver/status HTTP/1.1\r\nHost: 127.0.0.1\r\nUser-agent: GameClient/1.0\r\n"
str2 = 'POST gameserver/itembuy/b HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{"item": 1}'

 # print(str.split(' / '))
print(str2)
print(str2.split('\r\n')[0].split(' '))

print('===')
for msg in str2.split('\r\n')[1:]:
    if not msg:
        # body 영역임을 감지
        continue
    
    print(msg)

# print(str2.split('\r\n')[1:])