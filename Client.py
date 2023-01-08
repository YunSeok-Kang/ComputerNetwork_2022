from socket import *

test_mode = False
serverName = "127.0.0.1"
serverPort = 12000


class HTTPRequest:
    """서버로 전송할 HTTP 요청을 만드는 클래스이다
    """
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
        """요청 문자열을 생성하는 함수

        Returns:
            string: 필드 정보(method, url, version, host, body, ...)를 기반으로 생성된 문자열을 반환한다.
        """
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
    """서버에 유저의 정보를 요청한다

    Args:
        http_version (string): 사용할 http 버전을 전달받는다

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
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
    """서버에 Item A에 대한 정보를 요청한다.

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
    request = HTTPRequest()
    request.method = "GET"
    request.url = "gameserver/iteminfo/a"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    return request.build_request()

def request_item_c_info():
    """서버에 Item C에 대한 정보를 요청한다.

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
    request = HTTPRequest()
    request.method = "GET"
    request.url = "gameserver/iteminfo/  c"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    return request.build_request()

def buy_item_b():
    """서버에 Item B의 구입 요청을 보낸다.

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
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

def request_pvp():
    """ 서버에 유저와 PVP 요청을 보낸다. body에 json 오브젝트 타입으로 user_name을 전달한다.

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
    request = HTTPRequest()
    request.method = "POST"
    request.url = "gameserver/make_match"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    request.body = '"user_name": Elon Musk'

    return request.build_request()

def get_server_status():
    """ 서버에 현재 서버의 상태를 요청한다.

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
    request = HTTPRequest()
    request.method = "HEAD"
    request.url = "gameserver/status"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    return request.build_request()

def add_money():
    """서버에 돈을 추가하는 요청을 보낸다. body에 json 오브젝트 타입으로 money를 전달한다.

    Returns:
        string: build_request()로 생성된 요청 문자열을 반환한다.
    """
    request = HTTPRequest()
    request.method = "PUT"
    request.url = "gameserver/userinfo/inventory/add"
    request.version = "HTTP/1.1"
    request.host = "127.0.0.1"
    request.user_agent = "GameClient/1.0"
    request.connection = "keep-alive"
    request.content_type = "application/json"

    request.body = '"money": 1000'

    return request.build_request()

def select_command(command):
    """command에 따라 각각 다른 요청 메시지를 생성한다.

    Args:
        command (string): command를 문자열로 전달받는다. 현재 1 ~ 8까지의 문자를 받으며, 그 외의 command는 처리하지 않는다.

    Returns:
        string: command에 대응되는 요청 메시지를 반환한다
    """
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
        msg = request_item_c_info()
    elif command == "8":
        msg = request_pvp()
    else:
        msg = None
    
    return msg

def run_client():
    """클라이언트 프로그램을 실행한다.
    """
    ip = input("ip 주소를 입력하세요(빈 문자열 입력 시 localhost):") # ip 주소를 입력받는다. 만약 공백으로 두면 localhost로 지정된다.
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
        print('7. 아이템 C 정보 가져오기')
        print('8. 일론 머스크에게 PVP 요청하기')
        print('9. 나가기')

        command = input('명령을 선택하세요:')
        if command == "9":
            clientSocket.send("close".encode())
            break
        else:
            msg = select_command(command)
            
        if msg: # 요청 메시지가 생성이 되었다면
            print()
            print("======================== Request to server ========================")
            print(msg) # 서버로 보낼 요청 표시

            clientSocket.send(msg.encode()) # 서버에 전송
            response = clientSocket.recv(1024).decode() # 전송에 따른 응답 메시지를 response에 저장
            print()
            print("======================== Response from server ========================")
            print(response) # 서버로부터 받은 응답을 표시
            print("========================  ========================")
            print()
        else:
            print('잘못된 명령입니다.')

    clientSocket.close()


def run_test():
    """서버에 실제로 연결되어 있지 않은 상태에서 테스트 모드를 작동. 테스트 모드는 각각의 command에 대응되는 요청 메시지를 생성하여 출력한다(서버와 연결 X)
    """
    for i in range(9):
        msg = select_command(str(i))
        print("========== {}번째 msg ==========".format(i))
        print(msg)

if __name__ == "__main__":
    """test_mode 변수에 따라 test 모드와 실제 클라이언트가 구동되는 모드를 작동한다
    """
    if test_mode:
        run_test()
    else:
        run_client()