import speedtest
import os
import subprocess
from datetime import datetime
import csv

def get_wifi_name():
    try:
        lines = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True).split('\n')
        return next((line.split(":")[1].strip() for line in lines if "SSID" in line), "N/A")
    except Exception as e:
        print(f"Error getting WiFi name: {e}")
        return "N/A"

def speed_test():
    try:
        st = speedtest.Speedtest()
        
        print("Speed Test Initiated...")
        print("Finding best server...")
        st.get_best_server()
        server = st.results.server
        isp = st.results.client.get('isp', 'N/A')
        wifi_name = get_wifi_name()

        print("Service Info:")
        server_info = f"Server: {server['host']} ({server.get('name', 'N/A')}, {server.get('country', 'N/A')})" if 'host' in server else "Server information not available."
        print(server_info)
        print(f"ISP: {isp}")
        print(f"WiFi Name: {wifi_name}")

        ip_address = st.results.client['ip']
        print(f"IP: {ip_address}")

        print("\nTesting Download Speed...")
        download_speed_mbps = st.download() / 10**6
        download_speed_mbs = st.download() / 8 / 10**6
        download_latency = st.results.ping
        print(f"Download Speed: {download_speed_mbps:.2f} Mbps / {download_speed_mbs:.2f} MB/s")
        print(f"Download Ping: {download_latency:.2f} ms")

        print("\nTesting Upload Speed...")
        upload_speed_mbps = st.upload() / 10**6
        upload_speed_mbs = st.upload() / 8 / 10**6
        upload_latency = st.results.ping
        print(f"Upload Speed: {upload_speed_mbps:.2f} Mbps / {upload_speed_mbs:.2f} MB/s")
        print(f"Upload Ping: {upload_latency:.2f} ms")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open('speedresults.csv', 'a', newline='') as csvfile:
            fieldnames = ['Date', 'Time', 'ISP', 'Download', 'D_Ping', 'Upload', 'U_Ping', 'IP', 'Wifi_Name', 'Test_Server']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'Date': current_time.split(' ')[0],
                'Time': current_time.split(' ')[1],
                'ISP': isp,
                'Download': f"{download_speed_mbps:.2f} Mbps",
                'D_Ping': f"{download_latency:.2f} ms",
                'Upload': f"{upload_speed_mbps:.2f} Mbps",
                'U_Ping': f"{upload_latency:.2f} ms",
                'IP': ip_address,
                'Wifi_Name': wifi_name,
                'Test_Server': f"{server.get('host', 'N/A')} ({server.get('name', 'N/A')}, {server.get('country', 'N/A')})"
            })

        print(f"\nTest completed on: {current_time}")
    except Exception as e:
        print(f"Error during speed test: {e}")

if __name__ == "__main__":
    speed_test()
    print("Results saved to speedresults.csv")
