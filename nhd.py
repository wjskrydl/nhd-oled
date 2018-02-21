# Copyright (c) 2018 Will Skrydlak
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from time import sleep
import RPi.GPIO as GPIO

class NhdLcd:
    """This is the class responsible for interacting with the US2066 OLED controller
    provided by New Haven Display. It provides function level abstraction for 
    displaying content to the OLED screen
    """
    __delay=500
    __reset=0
    __dc=0
    __clk=0
    __d0=0
    __d1=0
    __d2=0
    __d3=0
    __d4=0
    __d5=0
    __d6=0
    __d7=0
    def __init__(self, dc, clk, cs, d0, d1, d2, d3, d4, d5, d6, d7, reset):    
        self.__dc=dc
        self.__clk=clk
        self.__cs=cs
        self.__d0=d0
        self.__d1=d1
        self.__d2=d2
        self.__d3=d3
        self.__d4=d4
        self.__d5=d5
        self.__d6=d6
        self.__d7=d7
        self.__reset=reset
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__reset, GPIO.OUT)
        # Device is now in reset LOW
        GPIO.output(self.__reset, GPIO.LOW)
        GPIO.setup(self.__dc, GPIO.OUT)
        GPIO.setup(self.__clk, GPIO.OUT)
        GPIO.setup(self.__cs, GPIO.OUT)
        
        # Chip select is set to HIGH
        GPIO.output(self.__cs, GPIO.HIGH)
        GPIO.setup(self.__d0, GPIO.OUT)
        GPIO.setup(self.__d1, GPIO.OUT)
        GPIO.setup(self.__d2, GPIO.OUT)
        GPIO.setup(self.__d3, GPIO.OUT)
        GPIO.setup(self.__d4, GPIO.OUT)
        GPIO.setup(self.__d5, GPIO.OUT)
        GPIO.setup(self.__d6, GPIO.OUT)
        GPIO.setup(self.__d7, GPIO.OUT)

        # Set all data pins to LOW
        GPIO.output(self.__d0, GPIO.LOW)
        GPIO.output(self.__d1, GPIO.LOW)
        GPIO.output(self.__d2, GPIO.LOW)
        GPIO.output(self.__d3, GPIO.LOW)
        GPIO.output(self.__d4, GPIO.LOW)
        GPIO.output(self.__d5, GPIO.LOW)
        GPIO.output(self.__d6, GPIO.LOW)
        GPIO.output(self.__d7, GPIO.LOW)
        # Take device out of reset HIGH
        GPIO.output(self.__reset, GPIO.HIGH)
    def __del__(self):
        GPIO.cleanup(self.__dc)
        GPIO.cleanup(self.__clk)
        GPIO.cleanup(self.__cs)
        GPIO.cleanup(self.__d0)
        GPIO.cleanup(self.__d1)
        GPIO.cleanup(self.__d2)
        GPIO.cleanup(self.__d3)
        GPIO.cleanup(self.__d4)
        GPIO.cleanup(self.__d5)
        GPIO.cleanup(self.__d6)
        GPIO.cleanup(self.__d7)
        GPIO.cleanup(self.__reset)

    def __command(self, byte):
        self.__bang(byte, True)

    def __data(self, byte):
        self.__bang(byte, False)

    def __bang(self, byte, command):
        if command==True:
            GPIO.output(self.__dc, GPIO.LOW)
        else:
            GPIO.output(self.__dc, GPIO.HIGH)
        GPIO.output(self.__cs, GPIO.LOW)
        if byte >= 128:
            GPIO.output(self.__d7, GPIO.HIGH)
            byte -= 128
        else:
            GPIO.output(self.__d7, GPIO.LOW)
        if byte >= 64:
            GPIO.output(self.__d6, GPIO.HIGH)
            byte -= 64
        else:
            GPIO.output(self.__d6, GPIO.LOW)
        if byte >= 32:
            GPIO.output(self.__d5, GPIO.HIGH)
            byte -= 32
        else:
            GPIO.output(self.__d5, GPIO.LOW)
        if byte >= 16:
            GPIO.output(self.__d4, GPIO.HIGH)
            byte -= 16
        else:
            GPIO.output(self.__d4, GPIO.LOW)
        if byte >= 8:
            GPIO.output(self.__d3, GPIO.HIGH)
            byte -= 8
        else:
            GPIO.output(self.__d3, GPIO.LOW)
        if byte >= 4:
            GPIO.output(self.__d2, GPIO.HIGH)
            byte -= 4
        else:
            GPIO.output(self.__d2, GPIO.LOW)
        if byte >= 2:
            GPIO.output(self.__d1, GPIO.HIGH)
            byte -= 2
        else:
            GPIO.output(self.__d1, GPIO.LOW)
        if byte >= 1:
            GPIO.output(self.__d0, GPIO.HIGH)
            byte -= 1
        else:
            GPIO.output(self.__d0, GPIO.LOW)
        
        GPIO.output(self.__clk, GPIO.HIGH)
        GPIO.output(self.__clk, GPIO.LOW)
        GPIO.output(self.__cs, GPIO.HIGH)
    def begin(self):
        """Sends a sequence of initialization messages to the US2066 controller and prepares
        the OLED for displaying messages.
        """
        self.__begin()

    def set_cursor(self, row, col):
        """Sets the cursor position to row, column"""
        self.__set_cursor(row, col)

    def __set_cursor(self, row, col):
        self.__command(0x80+(row*0x20)+col)

    def display_text(self, text):
        """Takes a string and will print at the current cursor positiong (DRAM address)."""
        self.__display_text(text)
        
    def __display_text(self, text):
        char_array=list(text)
        for c in char_array:
            self.__data(self.__get_char_hex(c))

    def __begin(self):
        self.__command(0x2A)
        self.__command(0x71)
        self.__data(0x00)
        self.__command(0x28)
        self.__command(0x08)
        self.__command(0x2A)
        self.__command(0x79)
        self.__command(0xD5)
        self.__command(0x70)
        self.__command(0x78)
        self.__command(0x09)
        self.__command(0x06)
        self.__command(0x72)
        self.__data(0x00)
        self.__command(0x2A)
        self.__command(0x79)
        self.__command(0xDA)
        self.__command(0x10)
        self.__command(0xDC)
        self.__command(0x00)
        self.__command(0x81)
        self.__command(0x7F)
        self.__command(0xD9)
        self.__command(0xF1)
        self.__command(0xDB)
        self.__command(0x40)
        self.__command(0x78)
        self.__command(0x28)
        self.__command(0x01)
        self.__command(0x80)
        self.__command(0x40)
        self.__data(0x00)
        self.__data(0x04)
        self.__data(0x04)
        self.__data(0x15)
        self.__data(0x0e)
        self.__data(0x1f)
        self.__data(0x04)
        self.__data(0x00)
        self.__command(0x0C)
        self.__command(0x01)
        self.__command(0x02)

        #self.__data(0x46)
        #self.__data(0x75)
        #self.__data(0x63)
        #self.__data(0x6b)
        #self.__data(0x20)
        #self.__data(0x61)
        #self.__data(0x20)
        #self.__data(0x64)
        #self.__data(0x75)
        #self.__data(0x63)
        #self.__data(0x6b)
        
    def __delay_microseconds(self,ticks):
        sleep(ticks/1000000.0)
    def __delay_milliseconds(self,ticks):
        sleep(ticks/1000.0)

    def __get_char_hex(self,c):
        ret=0x00
        if c==' ':
            ret=0x20
        elif c=='!':
            ret=0x21
        elif c=='"':
            ret=0x22
        elif c=='#':
            ret=0x23
        elif c=='$':
            ret=0x24
        elif c=='%':
            ret=0x25
        elif c=='&':
            ret=0x26
        elif c=='\'':
            ret=0x27
        elif c=='(':
            ret=0x28
        elif c==')':
            ret=0x29
        elif c=='*':
            ret=0x2a
        elif c=='+':
            ret=0x2b
        elif c==',':
            ret=0x2c
        elif c=='-':
            ret=0x2d
        elif c=='.':
            ret=0x2e
        elif c=='/':
            ret=0x2f
        elif c=='0':
            ret=0x30
        elif c=='1':
            ret=0x31
        elif c=='2':
            ret=0x32
        elif c=='3':
            ret=0x33
        elif c=='4':
            ret=0x34
        elif c=='5':
            ret=0x35
        elif c=='6':
            ret=0x36
        elif c=='7':
            ret=0x37
        elif c=='8':
            ret=0x38
        elif c=='9':
            ret=0x39
        elif c==':':
            ret=0x3a
        elif c==';':
            ret=0x3b
        elif c=='<':
            ret=0x3c
        elif c=='=':
            ret=0x3d
        elif c=='>':
            ret=0x3e
        elif c=='?':
            ret=0x3f
        elif c=='@':
            ret=0x40
        elif c=='A':
            ret=0x41
        elif c=='B':
            ret=0x42
        elif c=='C':
            ret=0x43
        elif c=='D':
            ret=0x44
        elif c=='E':
            ret=0x45
        elif c=='F':
            ret=0x46
        elif c=='G':
            ret=0x47
        elif c=='H':
            ret=0x48
        elif c=='I':
            ret=0x49
        elif c=='J':
            ret=0x4a
        elif c=='K':
            ret=0x4b
        elif c=='L':
            ret=0x4c
        elif c=='M':
            ret=0x4d
        elif c=='N':
            ret=0x4e
        elif c=='O':
            ret=0x4f
        elif c=='P':
            ret=0x50;
        elif c=='Q':
            ret=0x51;
        elif c=='R':
            ret=0x52;
        elif c=='S':
            ret=0x53;
        elif c=='T':
            ret=0x54;
        elif c=='U':
            ret=0x55;
        elif c=='V':
            ret=0x56;
        elif c=='W':
            ret=0x57;
        elif c=='X':
            ret=0x58;
        elif c=='Y':
            ret=0x59;
        elif c=='Z':
            ret=0x5a
        elif c=='[':
            ret=0x5b
        #elif c=='': cant print yen symbol
        #    ret=0x5
        #    ret.lo=12
        elif c==']':
            ret=0x5d
        elif c=='^':
            ret=0x5e
        elif c=='_':
            ret=0x5f
        elif c=='`':
            ret=0x60
        elif c=='a':
            ret=0x61
        elif c=='b':
            ret=0x62
        elif c=='c':
            ret=0x63
        elif c=='d':
            ret=0x64
        elif c=='e':
            ret=0x65
        elif c=='f':
            ret=0x66
        elif c=='g':
            ret=0x67
        elif c=='h':
            ret=0x68
        elif c=='i':
            ret=0x69
        elif c=='j':
            ret=0x6a
        elif c=='k':
            ret=0x6b
        elif c=='l':
            ret=0x6c
        elif c=='m':
            ret=0x6d
        elif c=='n':
            ret=0x6e
        elif c=='o':
            ret=0x6f
        elif c=='p':
            ret=0x70
        elif c=='q':
            ret=0x71
        elif c=='r':
            ret=0x72
        elif c=='s':
            ret=0x73
        elif c=='t':
            ret=0x74
        elif c=='u':
            ret=0x75
        elif c=='v':
            ret=0x76
        elif c=='w':
            ret=0x77
        elif c=='x':
            ret=0x78
        elif c=='y':
            ret=0x79
        elif c=='z':
            ret=0x7a
        elif c=='{':
            ret=0x7b
        elif c=='|':
            ret=0x7c
        elif c=='}':
            ret=0x7d
        #elif c= e '': can't handle right arrow
        #    ret=0x7
        #    ret.lo=14
        #elif c= e '': can't handle left arrow
        #    ret=0x7
        #    ret.lo=15
        elif c=='~':
            ret=0x00
        return ret
