import socket
import threading
import mysql.connector
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
password = os.getenv("password")
database = os.getenv("database")

rescan = False

#ensure only one thread is executing the code at a time
print_lock = threading.Lock()

#ensure safe print
def safe_print(msg):
    with print_lock:
        print(msg)

#function to scan ports
def scan_port(ip, port):
    try:
        # connect to the database
        db = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
        cursor = db.cursor()

        #check if the port is already scanned in the database
        if not rescan:
            cursor.execute("SELECT status FROM port_scans WHERE ip = %s AND port = %s", (ip, port))
            cache = cursor.fetchone()
            if cache:
                cursor.close()
                db.close()
                return

        #by default, assume the port is closed
        status = "closed"

        try:
            #create a socket
            s = socket.socket()
            #set timeout to 1.0 seconds
            s.settimeout(1.0)
            #connect to the target IP and port
            s.connect((ip, port))

            #get the service name using getservbyport() function
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            #print if the port is open
            status = "open"
            if rescan:
                safe_print(f"Port {port} is open. Service: {service}")

        # ignore socket errors
        except:
            pass
        finally:
            #close the socket
            s.close()

        #update the database
        cursor.execute("""
            INSERT INTO port_scans (ip, port, status)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE status = VALUES(status)
        """, (ip, port, status))
        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        safe_print(f"Error: {e}")

def display_open_ports(ip):
    try:
        db = mysql.connector.connect(user="root", password=password, host="localhost", database=database)
        cursor = db.cursor()

        # Query the database for open ports
        cursor.execute("SELECT port FROM port_scans WHERE ip = %s AND status = 'open'", (ip,))
        open_ports = cursor.fetchall()

        if open_ports:
            safe_print(f"\nOpen ports for {ip}:")
            for port in open_ports:
                safe_print(f" - Port {port[0]}")
        else:
            safe_print(f"No open ports found for {ip}.")

        cursor.close()
        db.close()

    except Exception as e:
        safe_print(f"Error while fetching open ports: {e}")

def main():
    target_ip = input("Enter the target IP: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    rescan_input = input("Force rescan? (y/n): ").lower().strip()
    global rescan
    rescan = rescan_input == "y"

    print("Scanning ports...")

    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, target_ip, port)

    print("Scan completed.")

    if not rescan:
        display_open_ports(target_ip)

if __name__ == '__main__':
    main()
