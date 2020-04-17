from microbit import *
import ustruct

ev8_16 = 116
buf1 = bytearray([0])
buf2 = bytearray([0, 0])
buf4 = bytearray([63, ev8_16, 0, 0])
bufEnc = bytearray([0, 3, 2, 1, 0])
bufEncOut = bytearray([0, 0, 0, 0, 0])

class tbos:
    def gyroReadReg(r):
        global buf1
        buf1[0] = r
        i2c.write(0x6B, buf1)
        b = i2c.read(0x6B, 1)
        return b[0]

    def gyroReadReg16(r):
        global buf2
        l = tbos.gyroReadReg(r)
        h = tbos.gyroReadReg(r + 1)
        buf2[0] = l
        buf2[1] = h
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
        # Initialize control registers
        # on the L3GD20H
        tbos.gyroWriteReg(0x20, 0x0F)
        tbos.gyroWriteReg(0x21, 0x00)
        tbos.gyroWriteReg(0x22, 0x00)
        tbos.gyroWriteReg(0x23, 0x00)
        tbos.gyroWriteReg(0x24, 0x00)
        return tbos.gyroReadReg(0x0f)

    def setMotorPower(m, p):
        global buf2
        if m == 1:
            buf2[0] = 10
        elif m == 2:
            buf2[0] = 20
        else:
            return  # no such motor
        if p > 100:
            p = 100
        if p < -100:
            p = -100
        buf2[1] = int(p)
        pin16.write_digital(0)
        spi.write(buf2)
        pin16.write_digital(1)
        return

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

    def playFrequency(k):
        global buf4
        if k < 0:
            k = 0
        if k > 10000:
            k = 10000

        buf4[0] = 0
        buf4[1] = 0
        buf4[2] = (int(k) & 0x0000ff00) >> 8
        buf4[3] = (int(k) & 0x000000ff)

        pin16.write_digital(0)
        spi.write(buf4)
        pin16.write_digital(1)
        return

    def getEncoder(i):
        global bufEnc
        if i == 1:
            bufEnc[0] = -30
        elif i == 2:
            bufEnc[0] = -31
        else:
            return 0  # no such encoder

        pin16.write_digital(0)
        spi.write_readinto(bufEnc, bufEncOut)
        pin16.write_digital(1)
        t = ustruct.unpack_from('<i', bufEncOut, 1)
        return t[0]

spi.init()
tbos.gyroInit()

############ Add your code here.##############
display.show(Image.SILLY)
sleep(1000)
dizzy = 0

# Spin your TB2 and measure rotation around the z axis
while True:
    sleep(50)
    yaw = abs(tbos.gyroGetZ() / 3)
    if yaw > 5:
        # Wheeeee :)
        display.show(Image.HAPPY)
        tbos.playNote(yaw)
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



