import serial
import subprocess
import time
import serial.tools.list_ports

# APN Information
APN = "super"

class ECM_Connector:
    def __init__(self, port=None, baudrate=115200, timeout=5, parity=serial.PARITY_NONE):
        if not self.is_modem_connected():
            raise Exception("Modem is not connected.")
        self.check_and_remove_modem_manager()
        self.port = port or self.find_modem_port()
        if not self.port:
            raise Exception("Modem port not found.")
        self.ser = serial.Serial(self.port, baudrate=baudrate, timeout=timeout, parity=parity)

    def send_at_command(self, command):
        self.ser.write((command + '\r').encode())
        time.sleep(1)
        response = self.ser.read_all().decode()
        if "OK" in response:
            return True
        else:
            return False

    @staticmethod
    def find_modem_port():
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "VID:PID=2C7C:0125" in port.hwid.upper():
                return port.device
        return None

    @staticmethod
    def is_modem_connected():
        result = subprocess.run(["lsusb"], capture_output=True, text=True)
        return "2c7c:0125" in result.stdout

    def check_and_remove_modem_manager(self):
        result = subprocess.run(["dpkg", "-s", "modemmanager"], capture_output=True, text=True)
        if "Status: install ok installed" in result.stdout:
            subprocess.run(["sudo", "apt", "purge", "modemmanager", "-y"])
            print("ModemManager removed.")
        else:
            print("ModemManager is not installed.")

    def set_usb_mode(self):
        return self.send_at_command("AT+QCFG=\"usbnet\",1")  # ECM mode

    def set_apn(self):
        return self.send_at_command(f"AT+CGDCONT=1,\"IPV4V6\",\"{APN}\"")

    def check_usb0_interface(self):
        result = subprocess.run(["ifconfig", "usb0"], capture_output=True, text=True)
        return "usb0" in result.stdout

    def connect_to_internet(self):
        if self.check_usb0_interface():
            print("usb0 interface is up.")
        else:
            print("usb0 interface is not up. Checking modem status...")
            if "1" in self.send_at_command("AT+QCFG=\"usbnet\""):
                print("USB mode is correct.")
            else:
                print("Setting USB mode...")
                self.set_usb_mode()
            if "READY" in self.send_at_command("AT+CPIN?"):
                print("SIM card is ready.")
            else:
                print("SIM card not ready.")
            network_status = self.send_at_command("AT+CREG?")
            if "0,1" in network_status or "0,5" in network_status:
                print("Network registration is successful.")
            else:
                print("Network registration failed.")
            self.reset_modem()

    def check_internet_connection(self):
        try:
            subprocess.check_call(["ping", "-I", "usb0", "sixfab.com", "-c", "5"])
            return True
        except subprocess.CalledProcessError:
            return False

    def reset_modem(self):
        self.send_at_command("AT+QPOWD")  # Power down command
        time.sleep(5)
        self.send_at_command("AT+CFUN=1,1")  # Restart modem
        print("Modem restarting...")
        time.sleep(30)  # Wait for modem to restart

try:
    modem = ECM_Connector()
    
    if modem.set_apn() and modem.set_usb_mode():
        print("USB mode and APN changed.")
        modem.reset_modem()
        modem.connect_to_internet()
        while True:
            if modem.check_internet_connection():
                print("Internet connection is active.")
            else:
                print("Internet connection is down, resetting modem...")
                modem.reset_modem()
                modem.connect_to_internet()
            time.sleep(60)  # Check every 60 seconds

except Exception as e:
    print(str(e))
