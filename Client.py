from socket import *

serverName = "127.0.0.1"
serverPort = 12000

# def select_method(input):
#     print('명령어를 선택하세요.')
#     print('1. 연결')
# while True:
#     command = select_method()
#     break;

class HTTPRequest:
    def __init__(self):
        self.method = ""
        self.url = ""
        self.version = "HTTP/1.1"
        self.host = "127.0.0.1"
        self.user_agent = ""
        self.connection = ""
        self.content_type = ""
        self.body = ""
    

    def build_request(self):
        # 요청 라인 빌드
        msg = self.method + " " + self.url + " " + self.version + "\r\nHost: " + self.host + "\r\n"
        
        # 헤더 라인 빌드
        if self.connection:
            msg += "Connection: " + self.connection + "\r\n"

        if self.content_type:
            msg += "Content-Type: " + self.content_type + "\r\n"

        if self.user_agent:
            msg += "User-agent: " + self.user_agent + "\r\n"

        # 공백 라인
        msg += "\r\n"

        # 개체 몸체 빌드
        if self.method != "HEAD":
            msg += "{" + self.body + "}"
        
        
        return msg

def request_user_info(http_version):
    request = HTTPRequest()
    request.method = "GET"
    request.url = "gameserver/userinfo"
    request.version = http_version
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"


    return request.build_request()

def request_item_a_info():
    request = HTTPRequest()
    request.method = "GET"
    request.url = "gameserver/iteminfo/a"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    return request.build_request()

def buy_item_b():
    request = HTTPRequest()
    request.method = "POST"
    request.url = "gameserver/itembuy/b"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    request.body = '"item": 1'

    return request.build_request()

def get_server_status():
    request = HTTPRequest()
    request.method = "GET"
    request.url = "gameserver/status"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    return request.build_request()

def add_money():
    request = HTTPRequest()
    request.method = "PUT"
    request.url = "gameserver/status"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    return request.build_request()

ip = input("ip 주소를 입력하세요(빈 문자열 입력 시 localhost):")
if (ip == ""):
    serverName = "127.0.0.1"
else:
    serverName = ip

# IPv4, TCP 소켓 사용 명시
clientSocket = socket(AF_INET, SOCK_STREAM)

# # 서버와의 연결 설정. 3 way handshake 수행 이후 설정이 완료됨.
clientSocket.connect((serverName, serverPort))
while True:
    print('1. 유저 정보 요청 GET')
    print('2. 유저 정보 요청(http 1.0) GET')
    print('3. 아이템 A 정보 가져오기')
    print('4. 아이템 B 구입하기(POST)')
    print('5. 서버 상태 확인하기(HEAD)')
    print('6. 돈 줍기(PUT)')
    print('7. 나가기')

    command = input('명령을 선택하세요:')
    msg = ""
    if command == "1":
        msg = request_user_info("HTTP/1.1")
    elif command == "2":
        msg = request_user_info("HTTP/1.0")
    elif command == "3":
        msg = request_item_a_info()
    elif command == "4":
        msg = buy_item_b()
    elif command == "5":
        msg = get_server_status()
    elif command == "6":
        msg = add_money()
    elif command == "7":
        clientSocket.send("close".encode())
        break
    else:
        print('잘못된 명령입니다.')

    if msg:
        clientSocket.send(msg.encode())
        response = clientSocket.recv(1024)
        print(response)


clientSocket.close()
# sentence = input('Input lowercase sentence:')

# # 문자열을 바이트 타입으로 변환 후 서버로 전송
# clientSocket.send(sentence.encode())

# # 서버로부터 받으 문자열을 모은다. 라인이 return 키로 끝날 때까지 계속 쌓인다.
# modifiedSentence = clientSocket.recv(1024)

# print('From Server:', modifiedSentence.decode())

# # 소켓을 닫고, 서버와의 TCP 연결 종료.
# clientSocket.close()