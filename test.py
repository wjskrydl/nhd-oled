#!/usr/bin/python3
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

import signal
from nhd import NhdLcd
from time import sleep
from threading import Lock

master_kill=False   
mutex=Lock()

def kill_flag(kill=False):
    """Locking kill flag for the SIGINT to gracefully
    kill the main thread.
    """
    global master_kill
    global mutex
    mutex.acquire()
    try:
        if kill==True:
            master_kill=True
        ret = master_kill
    finally:
        mutex.release()
    return ret

def signal_handler(signal, frame):
    """Handles interrupts"""
    kill_flag(True) 

def main():
    # sets up the signal handler for SIGINT
    signal.signal(signal.SIGINT,signal_handler)
    
    # creates NhdLcd object with the respective pins
    lcd=NhdLcd(2,3,18,26,19,13,6,4,17,27,22,10)
    
    # sets up the display
    lcd.begin()
    
    # everything after this is is just fancy printing
    upOne=True
    one=0
    upTwo=True
    two=0
    upThree=True
    three=0
    upFour=True
    four=0
    while kill_flag()==False:
        lcd.set_cursor(0,one)
        if upOne==True:
            lcd.display_text(' All your base')
            if one==6:
                upOne=False
            else:
                one+=1
        else:
            lcd.display_text('All your base ')
            if one==0:
                upOne=True
            else:
                one-=1
        lcd.set_cursor(1,two)
        if upTwo==True:
            lcd.display_text(' are')
            if two==16:
                upTwo=False
            else:
                two+=1
        else:
            lcd.display_text('are ')
            if two==0:
                upTwo=True
            else:
                two-=1
        lcd.set_cursor(2,three)
        if upThree==True:
            lcd.display_text(' belong')
            if three==13:
                upThree=False
            else:
                three+=1
        else:
            lcd.display_text('belong ')
            if three==0:
                upThree=True
            else:
                three-=1
        lcd.set_cursor(3,four)
        if upFour==True:
            lcd.display_text(' to us')
            if four==14:
                upFour=False
            else:
                four+=1
        else:
            lcd.display_text('to us ')
            if four==0:
                upFour=True
            else:
                four-=1
        sleep(.15)

if __name__ == '__main__':
    main()

