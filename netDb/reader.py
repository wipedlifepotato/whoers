import os
import re
import sys

class NetIpGrabber:
    def __init__(self, net_db_path='./netDb'):
        self.npath = net_db_path
        self.counter = 0

    def grab_ip_from_file(self, file_path):
        with open(file_path, 'rb') as df:
            data = df.read()

            # Remove non-printable ASCII characters
            printable_data = bytes(filter(lambda x: x >= 32 or x in [9, 10, 13], data))

            # Try to decode the binary data
            try:
                decoded_data = printable_data.decode('utf-8', errors='ignore')
            except UnicodeDecodeError:
                decoded_data = ""

            # Split the decoded data using ';'
            params = decoded_data.split(';')

            # Extract IP addresses and ports from the split data
            ips = re.findall(r'(\d+\.\d+\.\d+\.\d+)', ''.join(params))
            ports = re.findall(r'port=(\d+)', ''.join(params))

            if len(ips) == 0 or len(ports) == 0:
                return []

            # Combine IPs and ports into "ip:port" format
            ip_port_pairs = [f"{ip}:{port}" for ip, port in zip(ips, ports)]

            # Remove duplicates
            unique_ip_port_pairs = list(set(ip_port_pairs))

            return unique_ip_port_pairs

    def grab_ips_from_all_files(self):
        ip_addresses = []

        for root, dirs, files in os.walk(self.npath):
            for file in files:
                if file.endswith('.dat'):
                    file_path = os.path.join(root, file)
                    ip_addresses.extend(self.grab_ip_from_file(file_path))

        return ip_addresses

class NoIP(Exception):
    pass
def getIPs(path):
    net_grabber = NetIpGrabber(path)
    
    all_ip_addresses = net_grabber.grab_ips_from_all_files()
    
    if all_ip_addresses:
        print("Unique IP Addresses and Ports found in all .dat files:")
        with open('ips.txt', 'a') as f:
         for ip_port_pair in all_ip_addresses:
             print(ip_port_pair, file=f)
    else:
        raise NoIP("No IP Addresses found in any .dat files.")
# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need path to netDb")
        sys.exit(1)
    getIPs(sys.argv[1])
    sys.exit(0)

