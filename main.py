# simple HTTP Server — যেটা ব্রাউজার থেকে রিকোয়েস্ট নিলে রিপ্লাই দেয়(HTML পেজ পাঠায়)

# socket লাইব্রেরি থেকে সবকিছু ইমপোর্ট করি
from socket import *

# সার্ভারের হোস্ট ও পোর্ট নাম্বার নির্ধারণ করি
host = "localhost"     # নিজের কম্পিউটারকেই নির্দেশ করছে
port = 8888            # আমরা ৮৮৮৮ নাম্বার পোর্টে কান করবো

try:
    # একটি TCP/IP টাইপের socket তৈরি করি
    server_socket = socket(AF_INET, SOCK_STREAM)

    # socket-টি নির্দিষ্ট IP এবং port-এ bind করি
    server_socket.bind((host, port))

    # সার্ভার socket-কে বলি সর্বোচ্চ ৫টি ক্লায়েন্টের রিকোয়েস্ট অপেক্ষা করতে
    server_socket.listen(5)

    # এখন সার্ভার চলতে থাকবে এবং ক্লায়েন্টের রিকোয়েস্ট গ্রহণ করবে
    while True:
        print("🔊 Server is ready to receive request!")

        # কোনো ক্লায়েন্ট কানেক্ট করলে তাকে অ্যাকসেপ্ট করি
        client_socket, address = server_socket.accept()
        print(f"📡 Client Address: {address}")

        # ক্লায়েন্ট থেকে আসা ডেটা পড়ি
        request_data = client_socket.recv(1024)
        request_data = request_data.decode()
        print("\n📨 Request Data:")
        print(request_data)

        # আমরা ক্লায়েন্টকে একটি HTTP রেসপন্স পাঠাবো
        response_data = "HTTP/1.1 200 OK\n\r"
        response_data += "Content-Type: text/html; charset=utf-8\r\n\r\n"
        response_data += "<html><body><h1>Hello, World! I am Meherab Mejbah</h1></body></html>\r\n\r\n"

        # রেসপন্সটিকে encode করে পাঠাতে হবে (bytes হিসেবে)
        response_data = response_data.encode()

        # ক্লায়েন্টকে রেসপন্স পাঠাই
        client_socket.sendall(response_data)

        # তারপর ক্লায়েন্টের সাথে কানেকশন বন্ধ করে দেই
        client_socket.shutdown(SHUT_RDWR)

except Exception as e:
    # যদি কোনো এরর হয়, তাহলে তা প্রিন্ট করি
    print(e)





# simple multithreaded TCP Server (টেক্সট রেসপন্স)
import socket           # সোকেট লাইব্রেরি
import threading        # থ্রেডিং লাইব্রেরি
import socketserver     # socketserver — সার্ভার বানানোর জন্য Python এর তৈরি মডিউল

# প্রথমে ক্লায়েন্টের রিকোয়েস্ট হ্যান্ডল করার জন্য হ্যান্ডলার ক্লাস বানাই
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    # এই ফাংশনটি তখনই চালু হবে যখন কোনো ক্লায়েন্ট রিকোয়েস্ট পাঠাবে
    def handle(self):
        # ক্লায়েন্ট থেকে আসা ডেটা পড়ি (1024 বাইট পর্যন্ত)
        data = str(self.request.recv(1024), "ascii")

        # এখনকার থ্রেডের নাম নিয়ে রাখি (যেমন: Thread-1, Thread-2)
        cur_thread = threading.current_thread()

        # থ্রেডের নাম সহ রেসপন্স বানাই
        response = bytes("{}: {}".format(cur_thread.name, data), "ascii")

        # ক্লায়েন্টকে রেসপন্স পাঠাই
        self.request.sendall(response)

# এখন আমরা একাধিক থ্রেড সমর্থন করে এমন সার্ভার বানাই
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass  # এখানে কিছু আলাদা লাগছে না, শুধু ক্লাস ডেফিনেশন

# ক্লায়েন্ট ফাংশন: এটা সার্ভারে কানেক্ট হয়ে মেসেজ পাঠাবে
def client(ip, port, message):
    # একটা সাধারণ TCP সোকেট বানাই
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # সার্ভারে কানেক্ট করি
        sock.connect((ip, port))

        # মেসেজ পাঠাই
        sock.sendall(bytes(message, "ascii"))

        # সার্ভার থেকে রেসপন্স পাই
        response = str(sock.recv(1024), "ascii")

        # রেসপন্স প্রিন্ট করি
        print("📥 Received: {}".format(response))

# মেইন স্ক্রিপ্ট চালু হবার অংশ
if __name__ == "__main__":
    # 0 দিলে অটো একটাই খালি পোর্ট নেয়
    HOST, PORT = "localhost", 0

    # সার্ভার তৈরি করি (হোস্ট, পোর্ট, হ্যান্ডলার)
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    # with ব্লক — সার্ভার চালানোর জন্য নিরাপদ উপায়
    with server:
        # server.server_address থেকে প্রকৃত IP এবং port পাই
        ip, port = server.server_address

        # নতুন থ্রেডে সার্ভার চালু করি যাতে একাধিক ক্লায়েন্ট হ্যান্ডল করা যায়
        server_thread = threading.Thread(target=server.serve_forever)

        # মেইন প্রোগ্রাম বন্ধ হলে যেন থ্রেডও বন্ধ হয়
        server_thread.daemon = True
        server_thread.start()

        print("🧵 Server loop running in thread:", server_thread.name)

        # এখন একে একে তিনটি ক্লায়েন্ট পাঠাই
        client(ip, port, "Hello World 1")
        client(ip, port, "Hello World 2")
        client(ip, port, "Hello World 3")

        # সব শেষ হলে সার্ভার বন্ধ করি
        server.shutdown()
