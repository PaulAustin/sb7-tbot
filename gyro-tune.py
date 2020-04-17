# Play a note based on the amount of rotation
# around the z axis

from microbit import *
import ustruct

# preallocate the low level byte arrays
# so they can be used with no gc
buf1 = bytearray([0])
buf2 = bytearray([0, 0])

class tbos:
    def gyroReadReg(r):
        global buf1
        buf1[0] = r
        i2c.write(0x6B, buf1)
        b = i2c.read(0x6B, 1)
        return b[0]

    def gyroReadReg16(r):
        global buf2
        buf2[0] = tbos.gyroReadReg(r)
        buf2[1] = tbos.gyroReadReg(r + 1)
        t = ustruct.unpack_from('<h', buf2, 0)
        return t[0]

    def gyroWriteReg(r, v):
        global buf2
        buf2[0] = r
        buf2[1] = v
        i2c.write(0x6B, buf2)

    def gyroGetX():
        return int(tbos.gyroReadReg16(0x28) / 114)

    def gyroGetY():
        return int(tbos.gyroReadReg16(0x2A) / 114)

    def gyroGetZ():
        return int(tbos.gyroReadReg16(0x2C) / 114)

    def gyroInit():
        # Initialize control registers for the
        # L3GD20H that is on the tbot control board
        tbos.gyroWriteReg(0x20, 0x0F)
        tbos.gyroWriteReg(0x21, 0x00)
        tbos.gyroWriteReg(0x22, 0x00)
        tbos.gyroWriteReg(0x23, 0x00)
        tbos.gyroWriteReg(0x24, 0x00)
        return tbos.gyroReadReg(0x0f)

    def playNote(k):
        global buf2
        buf2[0] = 62
        if k < 0:
            k = 0
        if k > 88:
            k = 88
        buf2[1] = int(k)
        pin16.write_digital(0)
        spi.write(buf2)
        pin16.write_digital(1)
        return

spi.init()
tbos.gyroInit()

############ Add your code here.##############
display.show(Image.SILLY)
sleep(1000)
dizzy = 0

# Spin your tbot and measure rotation around the z axis
while True:
    sleep(50)
    yaw = abs(tbos.gyroGetZ())
    if yaw > 15:
        # Wheeeee :)
        display.show(Image.HAPPY)
        tbos.playNote(yaw/3)
        dizzy += 1
    else:
        if dizzy > 20 :
            # I'm dizzy
            display.show(Image.SILLY)
            dizzy -= 4
        else:
            # Meh, spin me more!
            display.show(Image.MEH)
            dizzy = 0

