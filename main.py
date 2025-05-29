import socket
import threading

#ensure only one thread is executing the code at a time
print_lock = threading.Lock()

#ensure safe print
def safe_print(msg):
    with print_lock:
        print(msg)

#function to scan ports
def scan_port(ip, port):
    try:
        #create a socket
        s = socket.socket()
        #set timeout to 0.5 seconds
        s.settimeout(0.5)
        #connect to the target IP and port
        s.connect((ip, port))

        #get the service name using getservbyport() function
        try:
            service = socket.getservbyport(port)
        except:
            service = "Unknown"

        #print if the port is open
        safe_print(f"Port {port} is open. Service: {service}")
        #close the socket
        s.close()
    # ignore socket errors
    except:
        pass

def main():
    target_ip = input("Enter the target IP: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    threads = []
    print("Scanning ports...")

    for port in range(start_port, end_port + 1):
        #create a new thread for each port
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        #append the thread to the list of threads
        threads.append(t)
        #start the thread
        t.start()

    #ensure all threads have finished executing
    for t in threads:
        t.join()

    print("Scan completed.")


if __name__ == '__main__':
    main()


