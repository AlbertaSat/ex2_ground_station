'''
 * Copyright (C) 2021  University of Alberta
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
'''
'''
 * @file test_dfgm.py
 * @author Daniel Sacro
 * @date 2022-03-01
'''

'''  to run > yarn run:test_dfgm -I uart -d /dev/ttyUSB0 '''

import numpy as np

import sys
import time
from os import path
sys.path.append("./test")

from tester import Tester

tester = Tester() #call to initialize local test class

def testAllCommandsToOBC():
    # Basic functionality tests
    tester.send('ex2.dfgm.dfgm_get_hk') # Update empty HK buffer by turning on DFGM for 1 sec
    time.sleep(2)

    tester.send('ex2.dfgm.dfgm_get_hk') # Should instantly get updated data from the HK buffer

    tester.sendAndExpect('ex2.dfgm.dfgm_run(1)', {'err': 0})
    time.sleep(2)

    tester.sendAndExpect('ex2.dfgm.dfgm_run(10)', {'err': 0})
    time.sleep(12) 

    tester.sendAndExpect('ex2.dfgm.dfgm_run(2147483647)', {'err': 0}) # INT_MAX
    time.sleep(1)
    tester.sendAndExpect('ex2.dfgm.dfgm_stop', {'err': 0}) # Check if DFGM actually stops dfgm_run

    tester.sendAndExpect('ex2.dfgm.dfgm_start', {'err': 0})
    time.sleep(5) # Let DFGM run for a bit

    tester.sendAndExpect('ex2.dfgm.dfgm_stop', {'err': 0}) # Check if DFGM actually stops dfgm_start

    tester.send('ex2.dfgm.dfgm_get_hk') # Check if data gets corrupt somehow (temp. should be ~20, not ~65000)


    # Error checking tests
    tester.sendAndExpect('ex2.dfgm.dfgm_run(2147483648)', {'err': 1}) # Bad param. - Overflow for 32-bit int
    tester.sendAndExpect('ex2.dfgm.dfgm_run(0)', {'err': 1}) # Bad param. - Less than minRuntime

    tester.sendAndExpect('ex2.dfgm.dfgm_run(100)', {'err': 0})
    tester.sendAndExpect('ex2.dfgm.dfgm_start', {'err': 2}) # Busy - DFGM already running
    tester.sendAndExpect('ex2.dfgm.dfgm_run(1000)', {'err': 2}) # Busy

    tester.send('ex2.dfgm.dfgm_get_hk') # See if any of the values get updated from other packets
    tester.sendAndExpect('ex2.dfgm.dfgm_stop', {'err': 0}) 

    tester.sendAndExpect('ex2.dfgm.dfgm_stop', {'err': 0}) # Should not fail if nothing is running


    tester.summary() #call when done to print summary of tests


if __name__ == '__main__':
    testAllCommandsToOBC()