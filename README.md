# Port Scanner

A simple, multi-threaded port scanner written in Python that allows users to scan a range of ports on a target IP address.

## Description

This port scanner tool enables users to check which ports are open on a specified IP address. It utilizes threading to scan multiple ports concurrently, making the scanning process faster and more efficient.

## Features

- Multi-threaded scanning for improved performance
- User-friendly command-line interface
- Service identification for open ports
- Customizable port range selection
- Database storage of scan results
- Caching to avoid rescanning previously checked ports
- Option to force rescan of ports

## Requirements

- Python 3.x
- Standard library modules:
  - socket
  - threading
  - concurrent.futures
- External packages:
  - mysql-connector-python
  - python-dotenv

## Installation

1. Clone this repository or download the project files
2. Install the required packages:
   ```
   pip install mysql-connector-python python-dotenv
   ```
3. Set up a MySQL database for storing scan results
4. Create a `.env` file in the project root with the following variables:
   ```
   password = your_mysql_password
   database = your_database_name
   ```
5. Create a table in your MySQL database for storing scan results:
   ```sql
   CREATE TABLE port_scans (
     ip VARCHAR(45),
     port INT,
     status VARCHAR(10),
     PRIMARY KEY (ip, port)
   );
   ```

## Usage

Run the script using Python:

```
python main.py
```

You will be prompted to enter:
1. Target IP address (e.g., 192.168.1.1 or localhost)
2. Start port number (e.g., 1)
3. End port number (e.g., 1000)
4. Whether to force rescan (y/n) - if 'n', the program will use cached results from previous scans when available

The program will then scan all ports in the specified range. If a port is open and you've chosen to force rescan, it will display the open port along with the service running on it (if identifiable). After scanning, it will display a summary of all open ports found for the target IP.

## How It Works

1. The script connects to a MySQL database to store and retrieve scan results
2. If not forcing a rescan, it checks if the port has been scanned before and uses cached results
3. For ports that need scanning, it uses a ThreadPoolExecutor to manage a pool of worker threads
4. Each worker thread attempts to establish a TCP connection to the target IP on its assigned port
5. If the connection is successful, the port is marked as open in the database
6. The script attempts to identify the service running on open ports using socket.getservbyport()
7. Thread locking is implemented to ensure thread-safe printing of results
8. After scanning, it displays a summary of all open ports from the database

## Example

```
Enter the target IP: 127.0.0.1
Enter the start port: 1
Enter the end port: 1000
Force rescan? (y/n): y
Scanning ports...
Port 80 is open. Service: http
Port 443 is open. Service: https
Port 3306 is open. Service: mysql
Scan completed.
```

With caching (no force rescan):
```
Enter the target IP: 127.0.0.1
Enter the start port: 1
Enter the end port: 1000
Force rescan? (y/n): n
Scanning ports...
Scan completed.

Open ports for 127.0.0.1:
 - Port 80
 - Port 443
 - Port 3306
```

## License

This project is open source and available for personal and educational use.
