from Server import Server as Flask_Server
from Socket_maker import *

def main():
    # TCP_connection
    socket = UDP_Server()
    #accept_thread = Thread(target=socket.accept_client)
    stream_thread = Thread(target=socket.get_stream)
    stream_thread.start()
    # Flask WAS
    server=Flask_Server()
    server.start_server()

if __name__ == "__main__":
    main()


