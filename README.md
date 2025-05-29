# Port Scanner

A simple, multi-threaded port scanner written in Python that allows users to scan a range of ports on a target IP address.

## Description

This port scanner tool enables users to check which ports are open on a specified IP address. It utilizes threading to scan multiple ports concurrently, making the scanning process faster and more efficient.

## Features

- Multi-threaded scanning for improved performance
- User-friendly command-line interface
- Service identification for open ports
- Customizable port range selection

## Requirements

- Python 3.x
- Standard library modules:
  - socket
  - threading

## Installation

1. Clone this repository or download the `main.py` file
2. No additional packages need to be installed as the script only uses Python's standard library

## Usage

Run the script using Python:

```
python main.py
```

You will be prompted to enter:
1. Target IP address (e.g., 192.168.1.1 or localhost)
2. Start port number (e.g., 1)
3. End port number (e.g., 1000)

The program will then scan all ports in the specified range and display which ports are open along with the service running on each port (if identifiable).

## How It Works

1. The script creates a separate thread for each port to be scanned
2. Each thread attempts to establish a TCP connection to the target IP on its assigned port
3. If the connection is successful, the port is marked as open
4. The script attempts to identify the service running on open ports using socket.getservbyport()
5. Thread locking is implemented to ensure thread-safe printing of results

## Example

```
Enter the target IP: 127.0.0.1
Enter the start port: 1
Enter the end port: 1000
Scanning ports...
Port 80 is open. Service: http
Port 443 is open. Service: https
Port 3306 is open. Service: mysql
Scan completed.
```

## License

This project is open source and available for personal and educational use.