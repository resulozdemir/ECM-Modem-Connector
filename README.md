# ECM Mode Modem Manager

This project automates the process of establishing a cellular internet connection in ECM mode using a Sixfab LTE modem with a Raspberry Pi. The script follows the steps outlined in the [Sixfab documentation](https://docs.sixfab.com/page/cellular-internet-connection-in-ecm-mode).

## Requirements

- Raspberry Pi
- Sixfab LTE modem
- Python 3
- `pyserial` library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/ECM-Mode-Modem-Manager.git
    cd ECM-Mode-Modem-Manager
    ```

2. Install the required Python libraries:

    ```sh
    pip install pyserial
    ```

## Usage

1. Run the script with root privileges to allow network configuration changes:

    ```sh
    sudo python3 ecm_mode_modem_manager.py
    ```

2. The script will perform the following actions:
    - Check if `ModemManager` is installed and remove it.
    - Verify that the Sixfab modem is connected via USB.
    - Set the modem to ECM mode.
    - Configure the APN settings.
    - Check the `usb0` interface and attempt to establish an internet connection.
    - Monitor the internet connection and reset the modem if the connection is lost.

## Code Explanation

The main script `ecm_mode_modem_manager.py` includes the following functionalities:

- **ECM_Mode Class**: Handles the modem initialization, AT commands, and internet connectivity.
- **send_at_command**: Sends AT commands to the modem and returns the response.
- **find_modem_port**: Identifies the correct USB port for the modem.
- **is_modem_connected**: Checks if the modem is connected via USB.
- **check_and_remove_modem_manager**: Removes `ModemManager` if it is installed.
- **set_usb_mode**: Sets the modem to ECM mode.
- **set_apn**: Configures the APN settings.
- **check_usb0_interface**: Checks if the `usb0` interface is up.
- **connect_to_internet**: Attempts to establish an internet connection.
- **check_internet_connection**: Pings a server to check if the internet connection is active.
- **reset_modem**: Resets the modem if the internet connection is lost.

## Example Output

The script will output messages indicating the status of each step, such as:

- "ModemManager removed."
- "usb0 interface is up."
- "Internet connection is active."
- "Internet connection is down, resetting modem..."

## Troubleshooting

If you encounter any issues, ensure that:
- The Sixfab modem is properly connected to the Raspberry Pi.
- You have installed the required Python libraries.
- You are running the script with root privileges.

For more information, refer to the [Sixfab documentation](https://docs.sixfab.com/page/cellular-internet-connection-in-ecm-mode).

## License

This project is licensed under the MIT License.
