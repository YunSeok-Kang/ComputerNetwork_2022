from datetime import datetime

str = "PUT gameserver/status HTTP/1.1\r\nHost: 127.0.0.1\r\nUser-agent: GameClient/1.0\r\n"
str2 = 'POST gameserver/itembuy/b HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{"item": 1}'
str3 = 'GET gameserver/itembuy/  c HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{"item": 1}'

 # print(str.split(' / '))
# print(str2)
# print(str2.split('\r\n')[0].split(' '))


# start_line = str2.split('\r\n')[0].split(' ')
# headers = []
# body = None

# is_body = False
# for msg in str2.split('\r\n')[1:]:
#     if is_body:
#         body = msg

#     if not msg:
#         # body 영역임을 감지
#         is_body = True
#         continue
    
#     headers.append(msg)
    # print(msg)

# print(str2.split('\r\n')[1:])

class RequestScenario:
    def __init__(self):
        valid_url = ['']

class ServerInfo:
    def __init__(self):
        pass

    # 0: 지원하지 않음
    # 1: 지원함
    # -1: 잘못된 프로토콜
    @classmethod
    def is_supporting_http_protocol(self, version):
        if version == "HTTP/1.1":
            return 1
        elif version == "HTTP/1.0":
            return 0
        elif version == "HTTP/2.0":
            return 0
        else:
            return -1


class HTTPResponse:
    def __init__(self, request):
        self.response_start_line, self.response_headers, self.response_body = self.retrieve_msg(request)

        self.status_line = []
        self.headers = []
        self.body = None

    def retrieve_msg(self, request):
        start_line = request.split('\r\n')[0].split(' ')
        headers = []
        body = ""

        is_body = False
        splitted_msg = request.split('\r\n')[1:]
        for msg in splitted_msg:
            # if is_body:
            #     body = msg

            if not msg:
                # body 영역임을 감지
                is_body = True
                break
            
            headers.append(msg)
        if is_body:
            body = splitted_msg[-1]

        return start_line, headers, body

    def make_status_line(self, http_version, status_code, status_text):
        self.status_line.append(http_version)
        self.status_line.append(status_code)
        self.status_line.append(status_text)
    
    def make_default_headers(self):
        self.headers.append('Server: GameServer/1.0')
        self.headers.append('Date: {}'.format(datetime.now().date()))
        self.headers.append('Connection: keep-alive')

    def get_response_msg(self):
        response_msg = self.status_line[0] + " " + self.status_line[1] + " " + self.status_line[2] + "\r\n"

        for header_msg in self.headers:
            response_msg += header_msg + "\r\n"

        response_msg += "\r\n"

        if self.body:
            response_msg += self.body

        print(response_msg)
        # for status_msg in self.status_line:
        #     response_msg = status_msg

            # msg = self.method + " " + self.url + " " + self.version + "\r\nHost: " + self.host + "\r\n"

    def response_step_one_status(self, method_type, request_target, http_version):
        self.make_default_headers()

        if ServerInfo.is_supporting_http_protocol(http_version) == 0:
            print('505')
            self.make_status_line('505', http_version, 'HTTP Version Not Supported')
            return
        elif ServerInfo.is_supporting_http_protocol(http_version) == -1:
            print('400')
            self.make_status_line('400', http_version, 'Bad Request')
            return

        if method_type == "GET":
            if request_target == 'gameserver/userinfo':
                print('200') # 유저 정보 전달
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"user_name:"YSKing"}'
            elif request_target == 'gameserver/iteminfo/a':
                print('301') # 메시지 301
                self.make_status_line('301', http_version, 'Moved Permanetly')
                self.headers.append('Location: gameserver/iteminfo/b')
            elif request_target == 'gameserver/iteminfo/b':
                print('200') # 아이템 b 설명
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"item:"ItemB"}'

        elif method_type == "POST":
            if request_target == 'gameserver/itembuy/b':
                print('200')
                self.make_status_line('200', http_version, 'OK')
            elif request_target == 'gameserver/make_match':
                print('404')
                self.make_status_line('404', http_version, 'Not Found')
        elif method_type == "HEAD":
            if request_target == 'gameserver/status':
                print('200')
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"server_info:"Game server version 1.0"}'
        elif method_type == "PUT":
            if request_target == 'gameserver/userinfo/inventory/add':
                print('200')
                self.make_status_line('200', http_version, 'OK')

    def build_response(self):
        method_type = self.response_start_line[0]
        request_target = self.response_start_line[1]
        http_version = self.response_start_line[2]

        # self.response_step_one_status(method_type, request_target, http_version)
        self.make_default_headers()

        if ServerInfo.is_supporting_http_protocol(http_version) == 0:
            print('505')
            self.make_status_line('505', http_version, 'HTTP Version Not Supported')
            self.get_response_msg()
            return
        elif ServerInfo.is_supporting_http_protocol(http_version) == -1:
            print('400')
            self.make_status_line('400', http_version, 'Bad Request')
            self.get_response_msg()
            return

        if method_type == "GET":
            if request_target == 'gameserver/userinfo':
                print('200') # 유저 정보 전달
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"user_name:"YSKing"}'
            elif request_target == 'gameserver/iteminfo/a':
                print('301') # 메시지 301
                self.make_status_line('301', http_version, 'Moved Permanetly')
                self.headers.append('Location: gameserver/iteminfo/b')
            elif request_target == 'gameserver/iteminfo/b':
                print('200') # 아이템 b 설명
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"item:"ItemB"}'

        elif method_type == "POST":
            if request_target == 'gameserver/itembuy/b':
                print('200')
                self.make_status_line('200', http_version, 'OK')
            elif request_target == 'gameserver/make_match':
                print('404')
                self.make_status_line('404', http_version, 'Not Found')
        elif method_type == "HEAD":
            if request_target == 'gameserver/status':
                print('200')
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"server_info:"Game server version 1.0"}'
        elif method_type == "PUT":
            if request_target == 'gameserver/userinfo/inventory/add':
                print('200')
                self.make_status_line('200', http_version, 'OK')

        
        self.get_response_msg()
        



# print("===== HTTPResponse =====")
# response = HTTPResponse(str2)
# print(response.response_start_line)
# print(response.response_headers)
# print(response.response_body)

# response.build_response()

# print("===== HTTPResponse2 =====")
# response = HTTPResponse(str3)
# print(response.response_start_line)
# print(response.response_headers)
# print(response.response_body)

# response.build_response()


test_msg = []
test_msg.append('GET gameserver/userinfo HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{}') # 1
test_msg.append('GET gameserver/userinfo HTTP/1.0\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{}') # 2
test_msg.append('GET gameserver/iteminfo/a HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{}') # 3
test_msg.append('POST gameserver/itembuy/b HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{"item": 1}') # 4
test_msg.append('HEAD gameserver/status HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{}') # 5
test_msg.append('PUT gameserver/userinfo/inventory/add HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{"money": 1000}') # 6
test_msg.append('GET gameserver/iteminfo/  c HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{}') # 7
test_msg.append('POST gameserver/make_match HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nContent-Type: application/json\r\nUser-agent: GameClient/1.0\r\n\r\n{"user_name": Elon Musk}') # 9

for msg in test_msg:
    print("===== HTTPResponse =====")
    response = HTTPResponse(msg)
    print(response.response_start_line)
    print(response.response_headers)
    print(response.response_body)

    response.build_response()