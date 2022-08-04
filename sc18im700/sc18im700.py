# -*- coding: utf-8 -*-

# Standard libraries
# Non-standard libraries
import serial

class SC18IM700:
    """SC18IM700 class
    """

    START_CMD      = b'S'
    STOP_CMD       = b'P'
    READ_REG_CMD   = b'R'
    WRITE_REG_CMD  = b'W'
    GPIO_READ_CMD  = b'I'
    GPIO_WRITE_CMD = b'O'
    POWER_DOWN_CMD = b'Z'

    REG_BRG0      = 0x00
    REG_BRG1      = 0x01
    REG_PortConf1 = 0x02
    REG_PortConf2 = 0x03
    REG_IOState   = 0x04
    REG_I2CAdr    = 0x06
    REG_I2CClkL   = 0x07
    REG_I2CClkH   = 0x08
    REG_I2CTO     = 0x09
    REG_I2CStat   = 0x0A

    I2CStat_I2C_OK = 0xF0
    I2CStat_I2C_NACK_ON_ADDRESS = 0xF1
    I2CStat_I2C_NACK_ON_DATA = 0xF2
    I2CStat_I2C_TIME_OUT = 0xF8

    def __init__(self, port:str, baudrate:int = 9600, default_i2c_addr=None) -> None:
        self._serial = serial.Serial(port, timeout=0.655, baudrate=9600)
        self._i2c_addr = default_i2c_addr
        if baudrate != 9600:
            val = 7372800 / baudrate - 16
            bytes_brg = round(val).to_bytes(2, 'little')
            brg0 = bytes_brg[0]
            brg1 = bytes_brg[1]
            self.write_regs([self.REG_BRG0, brg0, self.REG_BRG1, brg1])
            self._serial.close()
            self._serial = serial.Serial(port, timeout=0.655, baudrate=baudrate)


    def __del__(self):
        self._serial.close()


    def _tx(self, data_bytes:bytes) -> None:
        self._serial.write(data_bytes)


    def _rx(self, size:int = 1) -> bytes:
        return self._serial.read(size=size)


    def _i2c_write_addr(self, addr:int) -> int:
        return (addr << 1) & 0xFE


    def _i2c_read_addr(self, addr:int) -> int:
        return (addr << 1) | 0x01


    def set_defalt_i2c_addr(self, default_i2c_addr:int) -> None:
        """Set default I2C Address

        Args:
            default_i2c_addr (int): I2C Address

        Returns:
            None
        """
        self._i2c_addr = default_i2c_addr


    def i2c_write(self, data_bytes:bytes, i2c_addr=None) -> None:
        """I2C: Transmits in master mode an amount of data

        Args:
            data_bytes (bytes): Data
            i2c_addr (optional): Target device address. If omitted, use `default_i2c_addr`

        Returns:
            None
        """
        size = len(data_bytes)
        if i2c_addr is None:
            i2c_addr = self._i2c_addr
        if size >= 256:
            raise Exception("Cannot i2c write more than 256 bytes")
        addr_w = self._i2c_write_addr(i2c_addr)
        wdata = self.START_CMD + bytes([addr_w, size]) + data_bytes + self.STOP_CMD
        self._tx(wdata)


    def i2c_read(self, i2c_addr=None, size:int=1) -> bytes:
        """I2C: Receives in master mode an amount of data

        Args:
            i2c_addr (optional): Target device address. If omitted, use `default_i2c_addr`
            size (int): Amount of data

        Returns:
            bytes: Received data
        """
        if i2c_addr is None:
            i2c_addr = self._i2c_addr
        addr_r = self._i2c_read_addr(i2c_addr)
        wdata = self.START_CMD + bytes([addr_r, size]) + self.STOP_CMD
        self._tx(wdata)
        return self._rx(size)


    def i2c_mem_write(self, reg_addr:int, data_bytes:bytes, i2c_addr=None) -> None:
        """I2C: Write an amount of data to a specific memory address

        Args:
            reg_addr (int): Register address
            data_bytes (bytes): Data
            i2c_addr (optional): Target device address. If omitted, use `default_i2c_addr`

        Returns:
            None
        """
        if i2c_addr is None:
            i2c_addr = self._i2c_addr
        addr_w = self._i2c_write_addr(i2c_addr)
        wdata =  self.START_CMD + bytes([addr_w, 1 + len(data_bytes)]) + bytes([reg_addr]) + bytes(data_bytes) + self.STOP_CMD
        self._tx(wdata)


    def i2c_mem_read(self, reg_addr:int, size:int=1, i2c_addr=None) -> bytes:
        """I2C: Read an amount of data from a specific memory address

        Args:
            reg_addr (int): Register address
            size (int): Amount of data
            i2c_addr (optional): Target device address. If omitted, use `default_i2c_addr`

        Returns:
            bytes: Received data
        """
        if i2c_addr is None:
            i2c_addr = self._i2c_addr
        addr_w = self._i2c_write_addr(i2c_addr)
        addr_r = self._i2c_read_addr(i2c_addr)
        wdata =  self.START_CMD + bytes([addr_w, 1]) + bytes([reg_addr])
        wdata += self.START_CMD + bytes([addr_r, size]) + self.STOP_CMD
        self._tx(wdata)
        return self._rx(size)


    def gpio_write(self, data:int) -> None:
        """Write GPIO register

        Args:
            data (int): GPIO register value

        Returns:
            None
        """
        wdata = self.GPIO_WRITE_CMD +  bytes([data]) + self.STOP_CMD
        self._tx(wdata)


    def gpio_read(self) -> bytes:
        """Read GPIO register

        Returns:
            bytes: Received GPIO register value
        """
        wdata = self.GPIO_READ_CMD + self.STOP_CMD
        self._tx(wdata)
        return self._rx(1)


    def power_down(self) -> None:
        """Power down
        """
        wdata = self.POWER_DOWN_CMD +  bytes([0x5A, 0xA5]) + self.STOP_CMD
        self._tx(wdata)


    def write_reg(self, reg_addr:int, data:int) -> None:
        """Set value in one register

        Args:
            reg_addr (int): Register address
            data (int): Register value

        Returns:
            None
        """
        wdata = self.WRITE_REG_CMD + bytes([reg_addr]) + bytes([data]) + self.STOP_CMD
        self._tx(wdata)


    def write_regs(self, regAddr_vals:list[int]) -> None:
        """Set values in multiple registers

        Args:
            regAddr_vals (list[int]): Register address and values. [REG_ADDR0, REG_VAL0, ..., REG_ADDRn, REG_VALn]

        Returns:
            None
        """
        wdata = self.WRITE_REG_CMD + bytes(regAddr_vals) + self.STOP_CMD
        self._tx(wdata)


    def read_reg(self, reg_addr:int) -> bytes:
        """Get value in one register

        Args:
            reg_addr (int): Register address

        Returns:
            bytes: Register value
        """
        wdata = self.READ_REG_CMD + bytes([reg_addr]) + self.STOP_CMD
        self._tx(wdata)
        return self._rx(1)


    def read_regs(self, regAddrs:list[int]) -> bytes:
        """Get values in multiple registers

        Args:
            regAddrs (list[int]): Register addresses. [REG_ADDR0, ..., REG_ADDRn]

        Returns:
            bytes: Received register values
        """
        wdata = self.READ_REG_CMD + bytes(regAddrs) + self.STOP_CMD
        self._tx(wdata)
        return self._rx(len(regAddrs))


    def enable_timeout(self):
        """Enable timeout
        """
        self.write_reg(self.REG_I2CTO, 0x67)


    def i2c_device_search(self) -> list[int]:
        """Search and get I2C device address list

        Returns:
            list[int]: Found I2C address list
        """
        self.enable_timeout()
        dev_addr_list = []
        print('*I2C Device Search Start*')
        for addr in range(0x01, 0x7E, 1):
            self.i2c_write(bytes([0x00]), i2c_addr=addr)
            res = self.read_reg(self.REG_I2CStat)
            if res == bytes([self.I2CStat_I2C_OK]):
                print('Device Found: 0x' + '{:X}'.format(addr) + ' (7bit Address)')
                dev_addr_list.append(addr)
        print('*I2C Device Search End*')
        return dev_addr_list


if __name__ == "__main__":
    import sys
    sc18 = SC18IM700(port='COM7', baudrate=9600)
    dev_addr_list = sc18.i2c_device_search()
    if len(dev_addr_list) == 0:
        sys.exit(1)

    i2c_addr = dev_addr_list[0]
    sc18.set_defalt_i2c_addr(i2c_addr)
    print(sc18.i2c_mem_read(reg_addr=0x03, size=4))
