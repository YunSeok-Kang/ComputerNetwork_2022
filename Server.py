from socket import *
from datetime import datetime
serverPort = 12000

class ServerInfo:
    """ 서버의 상태 등을 나타내고 관리하는 클래스.
    """
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


"""
클라이언트로부터 전송 받은 HTTP 요청을 처리하고, 그에 대응되는 응답 메시지를 생성하는 클래스
"""
class HTTPResponse:
    def __init__(self, request):
        """_summary_

        Args:
            request (string): HTTPResponse 객체를 생성하며 argument로 전달하는 클라이언트로부터 전달받은 string 타입의 요청 메시지
        """
        self.response_start_line, self.response_headers, self.response_body = self.retrieve_msg(request)

        self.status_line = []
        self.headers = []
        self.body = None

        self.response_msg = ""

    def retrieve_msg(self, request):
        """클라이언트로부터 전달 받은 string 타입의 request를 분해하여 status line, header, body를 각각 반환하는 함수
        분해되어 반환된 정보를 바탕으로 요청을 알아내어 응답 메시지를 생성함

        Args:
            request (string): 클라이언트로부터 전달받은 string 타입의 요청 메시지

        Returns:
            start_line: Request line의 method, url, version 정보를 문자열로부터 분리하여 리스트 형태로 반환함
            headers: Header line을 모두 분리하여 각각의 헤더를 list의 요소로 저장하여 반환함
            body: body 정보를 string 형태로 반환함
        """
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
        """응답에 필요한 http_version, 상태 코드, 상태 메시지 정보를 입력하면 HTTPResponse 클래스의 필드인 status_line에 append하는 함수

        Args:
            http_version (string): http 버전 정보 문자열
            status_code (string): 상태 코드의 문자열
            status_text (string): 상태 메시지의 문자열
        """
        self.status_line.append(http_version)
        self.status_line.append(status_code)
        self.status_line.append(status_text)
    
    def make_default_headers(self):
        """기본적으로 포함되는 헤더를 생성해주는 함수
        """
        self.headers.append('Server: GameServer/1.0')
        self.headers.append('Date: {}'.format(datetime.now().date()))
        self.headers.append('Connection: keep-alive')

    def get_response_msg(self):
        """
        응답에 필요하여 생성했던 Status line, Header line, Entity Body를 문자열로 만들어 반환하는 함수
        build_response 함수의 마지막에 실행되어 ㅁ
        """
        response_msg = self.status_line[0] + " " + self.status_line[1] + " " + self.status_line[2] + "\r\n"

        for header_msg in self.headers:
            response_msg += header_msg + "\r\n"

        response_msg += "\r\n"

        if self.body:
            response_msg += self.body

        self.response_msg = response_msg

    def build_response(self):
        """응답에 필요한 정보들을 생성하는 함수. 각 요청에 대한 응답의 정리는 ReadMe에서 진행함.
        """
        method_type = self.response_start_line[0]
        request_target = self.response_start_line[1]
        http_version = self.response_start_line[2]

        """기본적으로 붙는 헤더 파일을 생성하는 코드
        """
        self.make_default_headers()

        # HTTP 버전에서 문제가 생기면 아래 코드(메서드 구분 및 바디 붙이기)를 실행하지 않고 바로 응답 메시지를 만든다.
        if ServerInfo.is_supporting_http_protocol(http_version) == 0:
            self.make_status_line('505', http_version, 'HTTP Version Not Supported')
            self.get_response_msg() 
            return
        elif ServerInfo.is_supporting_http_protocol(http_version) == -1:
            self.make_status_line('400', http_version, 'Bad Request')
            self.get_response_msg()
            return

        """메서드 타입과 request target 등을 기반으로 응답 메시지를 생성함
        """
        if method_type == "GET":
            if request_target == 'gameserver/userinfo':
                # 유저 정보 전달
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"user_name:"YSKing"}'
            elif request_target == 'gameserver/iteminfo/a':
                # 메시지 301
                self.make_status_line('301', http_version, 'Moved Permanetly')
                self.headers.append('Location: gameserver/iteminfo/b')
            elif request_target == 'gameserver/iteminfo/b':
                # 아이템 b 설명
                self.make_status_line('200', http_version, 'OK')
                self.body = '{"item:"ItemB"}'

        elif method_type == "POST":
            if request_target == 'gameserver/itembuy/b':
                self.make_status_line('200', http_version, 'OK')
            elif request_target == 'gameserver/make_match':
                self.make_status_line('404', http_version, 'Not Found')
        elif method_type == "HEAD":
            if request_target == 'gameserver/status':
                self.make_status_line('200', http_version, 'OK')
        elif method_type == "PUT":
            if request_target == 'gameserver/userinfo/inventory/add':
                self.make_status_line('200', http_version, 'OK')

        
        self.get_response_msg()


if __name__ == "__main__":
    # 소켓 생성
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # 서버 포트 번호를 소켓과 연관시킴
    serverSocket.bind(('', serverPort))

    # 소켓 연결 대기. 서버가 클라이언트로부터의 TCP 연결 요청을 듣도록 함.
    serverSocket.listen(1)

    print('The server is ready to receive')
    while True:
        # 클라이언트의 연결 요청을 받으면 accept 함수 실행하여 대응되는 클라이언트에게 지정된 소켓 생성.
        # 그 이후 handshaking 완료하여 클라이언트의 소켓과 connectionSocket 간에 TCP 연결 생성.
        connectionSocket, addr = serverSocket.accept()
        print('client connected...')

        while True:
            request_msg = connectionSocket.recv(1024).decode() # 클라이언트로부터 요청 메시지를 받는다.
            if (request_msg == "close"): # 만약 close라는 내용의 메시지가 날아오면 연결을 종료한다.
                print("close")
                break
            else:
                response = HTTPResponse(request_msg) # 요청 메시지를 기반으로 응답 메시지를 생성한다.
                response.build_response() # 실질적으로 응답을 문자열로 생성해주는 부분.
                response_msg = response.response_msg
                print(response_msg) # 서버의 콘솔에 메시지를 남겨놓는다.

                connectionSocket.send(response_msg.encode()) # 응답을 클라이언트에게 전송한다.

        # 소켓 닫음. 그러나 serverSocket이 열려있기에 다른 클라이언트가 접근 가능.
        connectionSocket.close()