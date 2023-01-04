from socket import *
serverPort = 12000

class HTTPResponse:
    def __init__(self, request):
        print(request)

        
        

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

    while True:
        request_msg = connectionSocket.recv(1024).decode()
        if (request_msg == "close"):
            print("close")
            break
        else:
            HTTPResponse(request_msg)
            connectionSocket.send("oo".encode())

    # while True:
        # request_msg = connectionSocket.recv(1024).decode()

    # # 도착 및 순서 보장되는 형태로 데이터 주고 받음(TCP 연결이기에)
    # sentence = connectionSocket.recv(1024).decode()
    # capitalizedSentence = sentence.upper()
    # connectionSocket.send(capitalizedSentence.encode())
    

    # 소켓 닫음. 그러나 serverSocket이 열려있기에 다른 클라이언트가 접근 가능.
    connectionSocket.close()
    