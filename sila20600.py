#!/usr/bin/env python3

from pymodbus.client import ModbusSerialClient
from pymodbus.transaction import ModbusRtuFramer
import argparse
import json

def parse_args():
    global args

    parser = argparse.ArgumentParser(description= "Script for communicate and getting values from UPS SILA EP20-300 / EP20-600")
    parser.add_argument("com_port", help="COM port. Default value is /dev/ttyUSB0")
    parser.add_argument("-b", "--baudrate", dest="baudrate", help="Baudrate for a COM port. Default value is 9600", type=int, metavar="BAUDRATE", default=9600)
    parser.add_argument("-u", "--uid", dest="uid", help="Modbus Unit ID. Default value is 10", type=int, metavar="UID", default=10)
    parser.add_argument("-a", "--address", dest="address", help="Modbus start address for a scanner. Default value is 30000", type=int, metavar="ADDRESS", default=30000)
    parser.add_argument("-c", "--count", dest="count", help="Values count for a scanner. Default value is 27", type=int, metavar="COUNT", default=27)

    args = parser.parse_args()

def scan():
    result = {}

    modbus = ModbusSerialClient(method='rtu', port=args.com_port, baudrate=args.baudrate, stopbits=1, bytesize=8, parity='N', timeout=1, unit=args.uid)

    modbus.connect()

    response = modbus.read_holding_registers(args.address,args.count,args.uid)
    #print(response.registers)

    result['work_state'] = str(response.registers[2])
    result['ac_input_voltage'] = str(float(int(response.registers[5])*0.1))
    result['ac_input_frequency'] = str(float(int(response.registers[6])*0.1))
    result['ac_output_voltage'] = str(float(int(response.registers[7])*0.1))
    result['ac_output_frequency'] = str(float(int(response.registers[8])*0.1))
    result['ac_output_current'] = str(float(int(response.registers[9])*0.1))
    result['ac_output_active_power'] = str(float(int(response.registers[10])))
    result['ac_output_apparent_power'] = str(float(int(response.registers[11])))
    result['output_load_percent'] = str(float(int(response.registers[12])))
    result['battery_voltage'] = str(float(int(response.registers[14])*0.1))
    result['battery_current'] = str(float(int(response.registers[15])))
    result['battery_temperature'] = str(response.registers[16])
    result['battery_capacity'] = str(response.registers[17])
    result['radiator_temperature'] = str(response.registers[18])

    print(json.dumps(result))

    modbus.close()

if __name__=="__main__":
    try:
        parse_args()
        scan()
    except Exception as e:
        print('Error:',str(e))