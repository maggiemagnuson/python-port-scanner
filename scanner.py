import argparse
from json.tool import main
import textwrap
import pyfiglet
import sys
import socket
from datetime import datetime
import pytz
from concurrent import futures


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped


def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = s.connect_ex((target, port))
        if result == 0:
            print(f"{port} is Open")
            return {port: "Open"}
        s.close()
    except Exception as e:
        return None


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)
    parser = argparse.ArgumentParser(
        description="Port Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            scanner.py -t <TARGET> -p <PORT>
        """))
    parser.add_argument("-t", "--target", help="Host name or IP")
    parser.add_argument("-p", "--port", help="Port number")
    args = parser.parse_args()

    print("-" * 50)
    print(f"Scanning Target: : {args.target}")
    print(f"Scanning started at: {datetime.now(pytz.timezone('America/Chicago'))}")
    print("-" * 50)

    input = [i for i in range(1, 1000)]
    data = []
    
    ##############################################
    # TEST RUN WITH CONCURRENCY
    ##############################################
    print(f"Process started at: {datetime.now(pytz.timezone('America/Chicago'))}")
    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_list = [executor.submit(scan_port, args.target, ip) for ip in input]
        for f in futures.as_completed(future_list):
            try:
                result = f.result()
            except Exception as e:
                print(e)
            else:
                if result is not None:
                    data.append(result)
            
    print(f"Process stopped at: {datetime.now(pytz.timezone('America/Chicago'))}")
    print(data)
    
    ##############################################
    # TEST RUN WITHOUT CONCURRENCY
    ##############################################
    print(f"Process started at: {datetime.now(pytz.timezone('America/Chicago'))}")
    data_2 = []
    for port in input:
        res = scan_port(args.target, port)
        if res is not None:
            data_2.append(res)
    print(f"Process stopped at: {datetime.now(pytz.timezone('America/Chicago'))}")
    print(data_2)
    