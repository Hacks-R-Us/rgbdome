import subprocess

ip = [192, 168, 10, 102]
mac = [0x92, 0x00, 0x00, 0x00, 0x00, 0x02]

def_ip = "#define IP {{{},{},{},{}}}".format(*ip)
def_mac = "#define MAC {{0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x},0x{:02x}}}".format(*mac)


stlink_exe = "C:\\Program Files (x86)\\Arduino\\hardware\\Arduino_STM32-master\\tools\\win\\stlink\\ST-LINK_CLI.exe"
stlink_args = ["-c", "SWD", "-P", "generic_boot20_pc13.bin", "0x8000000", "-Rst", "-Run"]

arduino_exe = "C:\\Program Files (x86)\\Arduino\\arduino_debug.exe"
arduino_args = ["--upload"]
arduino_file = "temp/temp.ino"
arduino_final = "stmstrand\\stmstrand.ino"

args = [stlink_exe] + stlink_args
input("Move boot0 to 1...")
subprocess.run(args)

with open("eepromflash\\eepromflash.ino", "r") as eeprom_file:
    with open("temp\\temp.ino", "w") as temp_file:
        temp_file.write(def_ip + "\n")
        temp_file.write(def_mac + "\n")
        for line in eeprom_file.readlines():
            if "define IP" in line or "define MAC" in line:
                continue
            temp_file.write(line)

input("Move boot0 to 0...")

## Flash eeprom
args = [arduino_exe] + arduino_args + [arduino_file]
subprocess.run(args)

## Flash final script
args = [arduino_exe] + arduino_args + [arduino_final]
subprocess.run(args)