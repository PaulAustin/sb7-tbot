# Make wheel 2 position match wheel 1 position
# No PID yet.

from microbit import *
import ustruct

ev8_16 = 116
buf1 = bytearray([0])
buf2 = bytearray([0, 0])
buf4 = bytearray([0, 0, 0, 0])
bufEnc = bytearray([0, 3, 2, 1, 0])
bufEncOut = bytearray([0, 0, 0, 0, 0])

class tbos:
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

        buf4[0] = 63
        buf4[1] = ev8_16
        buf4[2] = (int(k) & 0x0000ff00) >> 8
        buf4[3] = (int(k) & 0x000000ff)

        pin16.write_digital(0)
        spi.write(buf4)
        pin16.write_digital(1)
        return

    def clearEncoder(i):
        global buf2
        if i == 1:
            buf2[0] = 15
        elif i == 2:
            buf2[0] = 25
        else:
            return 0  # no such encoder

        buf2[1] = 0
        pin16.write_digital(0)
        spi.write(buf2)
        pin16.write_digital(1)
        return


    def getEncoder(i):
        global bufEnc
        if i == 1:
            bufEnc[0] = -15
        elif i == 2:
            bufEnc[0] = -25
        else:
            return 0  # no such encoder

        pin16.write_digital(0)
        spi.write_readinto(bufEnc, bufEncOut)
        pin16.write_digital(1)
        t = ustruct.unpack_from('<i', bufEncOut, 1)
        return t[0]

spi.init()

############ Add your code here.##############
display.show(Image.HAPPY)
sleep(1000)
tbos.clearEncoder(1)
tbos.clearEncoder(2)
sleep(100)
# Spin your TB2 and measure rotation around the z axis
while True:
    e1 = tbos.getEncoder(1)
    e2 = -tbos.getEncoder(2)
    ediff = e1-e2
    tbos.setMotorPower(2, ediff/50)
