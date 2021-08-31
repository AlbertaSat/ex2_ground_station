'''
 * Copyright (C) 2020  University of Alberta
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
 * @file system.py
 * @author Andrew Rooney
 * @date 2020-08-26
'''

'''
Numpy types (> for BE)
'?' boolean

'b' (signed) byte

'B' unsigned byte

'i' (signed) integer

'u' unsigned integer

'f' floating-point

'c' complex-floating point

'm' timedelta

'M' datetime

'O' (Python) objects

'S', 'a' zero-terminated bytes (not recommended)

'U' Unicode string

'V' raw data (void)

'var' variable-size (non-numpy). Checks the data type from elsewhere
'''


import numpy as np


class SystemValues(object):
    def __init__(self):
        self.appIdx = 0
        self.serviceIdx = 2
        self.subserviceIdx = 4
        
        self.varTypes = {
            0: '<u1',
            1: '<i1',
            2: '<u2',
            4: '<u4',
            9: '<S16' #Empty means all zero or Use <V16
        }

        self.APP_DICT = {
            'OBC': 1,
            'EPS': 4,  # hard coded by manufacturer
            'ADCS': 2,
            'COMMS': 3,
            'IAC': 5,
            'DBG': 7,
            'GND': 16,
            'DEMO': 30,
            'LAST': 31
        }
        self.SERVICES = {
            'TIME_MANAGEMENT': {
                'port': 8,  # share a port with EPS time service
                # TODO: these need a error response value
                'subservice': {
                    'GET_EPS_TIME': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': None,  # SID
                            'returns': {
                                'err': '>b',
                                'timestamp': '<u4'
                            }
                        }
                    },
                    'SET_EPS_TIME': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['<u4'],  # timestamp
                            'returns': {
                                'err': '>b'  # err
                            }
                        }
                    },
                    'GET_LAST_PPS_TIME': {
                        'what': 'Get last PPS time (EPS)',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',  # error is 2 (wrong pps)
                                #'timestampInS': '<u4',
                                #'secondFraction': '<u4'
                            }
                        }
                    },
                    'GET_PRECISE_TIME': {
                        'what': 'A command to get precise time (NTP-like format)',
                        'subPort': 3,
                        'inoutInfo': {
                            # Same as return (just reserving space)
                            'args': ['>B', '<u4', '<u4', '<u4', '<u4', '<u4', '<u4', '<u4', '<u4'],
                            'returns': {
                                'err': '>B',
                                'requestTimeInS': '<u4',
                                'requestSecondFraction': '<u4',
                                'receiveTimeInS': '<u4',
                                'receiveSecondFraction': '<u4',
                                'transmitTimeInS': '<u4',
                                'transmitSecondFraction': '<u4',
                                'receptionTimeInS': '<u4',
                                'receptionSecondFraction': '<u4'
                            }
                        }
                    },
                    'GET_TIME': { # OBC time
                        'subPort': 10,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'timestamp': '>u4'
                            }
                        }
                    },
                    'SET_TIME': { # OBC time
                        'subPort': 11,
                        'inoutInfo': {
                            'args': ['>u4'],  # timestamp
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                }
            },
            'GENERAL': {
                'port' : 11,
                'subservice' : {
                    'REBOOT': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['>B'],  # mode. Can be 'A', 'B', 'G'
                            'returns': {
                                'err': '>b'  # err
                            }
                        }
                    }
                }
            },
            'COMMUNICATION': {
                'port': 10,
                'subservice': {
                    'S_GET_FREQ': {
                        'what': 'Gets the S-band frequency (MHz)',
                        'subPort': 1,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'frequency': '>f4',
                            }
                        }
                    },
                    'S_GET_CONTROL': {
                        'what': 'Gets the S-band`s power amplifier write status and its mode = {0:configuration, 1: synchronization, 2:data, 3:test data}',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'status': '>u1',
                                'mode': '>u1',
                            }
                        }
                    },
                    'S_GET_ENCODER': {
                        'what': 'Gets the S-band encoding configuration. mod={0:QPSK, 1:OQPSK}, rate={0:half, 1:full}',
                        'subPort': 3,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'scrambler': '>u1',
                                'filter': '>u1',
                                'modulation': '>u1',
                                'rate': '>u1',
                            }
                        }
                    },
                    'S_GET_PAPOWER': {
                        'what': 'Gets the power value of S-band power amplifier',
                        'subPort': 4,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Power Amplifier Power': '>u1',
                            }
                        }
                    },
                    'S_GET_STATUS': {
                        'what': 'Checks if the power of S-band power aamplifier is good and if the frequency lock is achieved',
                        'subPort': 5,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'PWRGD': '>u1',
                                'TXL': '>u1',
                            }
                        }
                    },
                    'S_GET_TR': {
                        'what': 'S-band Transmit Ready Indicator = {0: >2560B in buffer}',
                        'subPort': 6,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Transmit Ready': '>i4',
                            }
                        }
                    },
                    'S_GET_BUFFER': {
                        'what': 'Gets the pointer to the buffer quantity in S-band. Input = {0:Count, 1:Underrun, 2:Overrun}',
                        'subPort': 7,
                        'inoutInfo': {
                            'args': ['>B'],
                            'returns': {
                                'err': '>b',
                                'buffer': '>u2',
                            }
                        }
                    },
                    'S_GET_HK': {
                        'what': 'Gets S-band housekeeping info',
                        'subPort': 8,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Output Power': '>f',
                                'Power Amplifier Temperature': '>f',
                                'Top Temperature': '>f',
                                'Bottom Temperature': '>f',
                                'Battery Current': '>f',
                                'Battery Voltage': '>f',
                                'Power Amplifier Current': '>f',
                                'Power Amplifier Voltage': '>f',
                            }
                        }
                    },
                    'S_SOFT_RESET': {
                        'what': 'Reset S-band FPGA registers to default',
                        'subPort': 9,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_GET_FULL_STATUS': {
                        'what': 'A full status of S-band non-configurable parameters',
                        'subPort': 10,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'PWRGD': '>u1',
                                'TXL': '>u1',
                                'Transmit Ready': '>i4',
                                'Buffer Count': '>u2',
                                'Buffer Underrun': '>u2',
                                'Buffer Overrun': '>u2',
                                'Output Power': '>f',
                                'Power Amplifier Temperature': '>f',
                                'Top Temperature': '>f',
                                'Bottom Temperature': '>f',
                                'Battery Current': '>f',
                                'Battery Voltage': '>f',
                                'Power Amplifier Current': '>f',
                                'Power Amplifier Voltage': '>f',
                            }
                        }
                    },
                    'S_SET_FREQ': {
                        'what': 'Sets the frequency of S-band (MHz)',
                        'subPort': 11,
                        'inoutInfo': {
                            'args': ['>f'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_SET_CONTROL': {
                        'what': 'Sets the S-band`s power amplifier write status and its mode = {0:config, 1: synch, 2:data, 3:test data}. Input: 2 binary',
                        'subPort': 12,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_SET_ENCODER': {
                        'what': 'Sets the S-band encoding configuration. mod={0:QPSK, 1:OQPSK}, rate={1:half, 0:full}. Input: 4 binary',
                        'subPort': 13,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_SET_PAPOWER': {
                        'what': 'Sets the power value of S-band power amplifier (24, 26, 28, 30 dBm)',
                        'subPort': 14,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'S_GET_CONFIG': {
                        'what': 'A full status of S-band configurable parameters (the ones with set functions)',
                        'subPort': 15,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Frequency': '>f',
                                'Power Amplifier Power': '>u1',
                                'Power Amplifier status': '>u1',
                                'Power Amplifier mode': '>u1',
                                'Encoder scrambler': '>u1',
                                'Encoder filter': '>u1',
                                'Encoder modulation': '>u1',
                                'Encoder rate': '>u1',
                            }
                        }
                    },
                    'S_SET_CONFIG': {
                        'what': 'Sets all the 8 S-band configurable parameters (freq PA_power PA_status PA_mode Enc_scrambler Enc_filter Enc_mod Enc_rate)',
                        'subPort': 16,
                        'inoutInfo': {
                            'args': ['>f', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_SCW': {
                        'what': 'Sets UHF status control word',
                        'subPort': 20,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_FREQ': {
                        'what': 'Sets UHF frequency (Hz)',
                        'subPort': 21,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_PIPE_T': {
                        'what': 'Sets UHF PIPE timeout period',
                        'subPort': 22,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_BEACON_T': {
                        'what': 'Sets UHF beacon message transmission period',
                        'subPort': 23,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_AUDIO_T': {
                        'what': 'Sets UHF audio beacon period b/w transmissions',
                        'subPort': 24,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_PARAMS': {
                        'what': 'Sets UHF freq, pipe_t, beacon_t, audio_t parameters. Input:4',
                        'subPort': 25,
                        'inoutInfo': {
                            'args': ['>u4', '>u4', '>u4', '>u4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_RESTORE': {
                        'what': 'Restore UHF default values',
                        'subPort': 26,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_LOW_PWR': {
                        'what': 'Puts UHF TRX into low power mode',
                        'subPort': 27,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_DESTINATION': {
                        'what': 'Sets UHF destination callsign',
                        'subPort': 28,
                        'inoutInfo': {
                            'args': ['>S6'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_SOURCE': {
                        'what': 'Sets UHF source callsign',
                        'subPort': 29,
                        'inoutInfo': {
                            'args': ['>S6'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_MORSE': {
                        'what': 'Sets UHF morse code callsign (max 36)',
                        'subPort': 30,
                        'inoutInfo': {
                            'args': ['>S36'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_MIDI': {
                        'what': 'Sets UHF MIDI audio beacon (max 36 notes)',
                        'subPort': 31,
                        'inoutInfo': {
                            # increase packet size and switch to >U108
                            'args': ['>S60'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_BEACON_MSG': {
                        'what': 'Sets UHF beacon message (max 98)',
                        'subPort': 32,
                        'inoutInfo': {
                            # Switch to >U97 after packet configuration
                            'args': ['>S60'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_I2C': {
                        'what': 'Sets UHF I2C address (22 | 23)',
                        'subPort': 33,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_WRITE_FRAM': {
                        'what': 'Sets UHF FRAM address and write 16-byte data',
                        'subPort': 34,
                        'inoutInfo': {
                            'args': ['>u4', '>S16'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SECURE': {
                        'what': 'Puts UHF TRX into secure mode',
                        'subPort': 35,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_GET_FULL_STAT': {
                        'what': 'Returns the fulla status of all the UHF non-configurable parameters',
                        'subPort': 36,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'HFXT': '>u1',
                                'UartBaud': '>u1',
                                'Reset': '>u1',
                                'RF Mode': '>u1',
                                'Echo': '>u1',
                                'BCN': '>u1',
                                'PIPE': '>u1',
                                'Bootloader': '>u1',
                                'CTS': '>u1',
                                'SEC': '>u1',
                                'FRAM': '>u1',
                                'RFTS': '>u1',
                                'Frequency': '>u4',
                                'PIPE timeout': '>u4',
                                'Beacon period': '>u4',
                                'Audio trans. period': '>u4',
                                'Uptime': '>u4',
                                'Packets out': '>u4',
                                'Packets in': '>u4',
                                'Packets in CRC16': '>u4',
                                'Temperature': '>f',
                            }
                        }
                    },
                    'UHF_GET_CALLSIGN': {
                        'what': 'Gets UHF destination and source callsign',
                        'subPort': 37,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Destination': '>S6',
                                'Source': '>S6',
                            }
                        }
                    },
                    'UHF_GET_MORSE': {
                        'what': 'Gets UHF morse callsign',
                        'subPort': 38,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Morse': '>S36',
                            }
                        }
                    },
                    'UHF_GET_MIDI': {
                        'what': 'Gets UHF MIDI audio beacon',
                        'subPort': 39,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'MIDI': '>S60',
                            }
                        }
                    },
                    'UHF_GET_BEACON_MSG': {
                        'what': 'Gets the beacon message',
                        'subPort': 40,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Beacon Message': '>S60',
                            }
                        }
                    },
                    'UHF_GET_FRAM': {
                        'what': 'Reads the FRAM data',
                        'subPort': 41,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b',
                                'FRAM': '>S16',
                            }
                        }
                    },
                    'UHF_SET_ECHO': {
                        'what': 'Starts echo over UART',
                        'subPort': 42,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_BCN': {
                        'what': 'Set the communication to the beacon mode',
                        'subPort': 43,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_SET_PIPE': {
                        'what': 'Set the communication to the PIPE(transparent) mode',
                        'subPort': 44,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'UHF_GET_SECURE_KEY': {
                        'what': 'Gets the key for secure mode',
                        'subPort': 45,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Secure Key': '>u4',
                            }
                        }
                    },
                }
            },
            
            'CONFIGURATION': {
                'port': 9,  # As per EPS docs
                'subservice': {
                    'GET_ACTIVE_CONFIG': {
                        'what': 'Gets config values in active mode for a specific type',
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['<u2', '<u1'], #id, type_id
                            'returns': {
                                'err': '>B',
                                'type': '<u1',
                                'Value': 'var' #In command parser it gets the data type from the return value for 'type'
                            }
                        }
                    },   
                    'GET_MAIN_CONFIG': {
                        'what': 'Gets config values in main mode for a specific type',
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['<u2', '<u1'], #id, type_id
                            'returns': {
                                'err': '>B',
                                'type': '<u1',
                                'Value': 'var' #See comment for active
                            }
                        }
                    },  
                    'GET_FALLBACK_CONFIG': {
                        'what': 'Gets config values in fallback mode for a specific type',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': ['<u2', '<u1'], #id, type_id
                            'returns': {
                                'err': '>B',
                                'type': '<u1',
                                'Value': 'var' #See comment for active
                            }
                        }
                    },
                    'GET_DEFAULT_CONFIG': {
                        'what': 'Gets config values in default mode for a specific type',
                        'subPort': 3,
                        'inoutInfo': {
                            'args': ['<u2', '<u1'], #id, type_id
                            'returns': {
                                'err': '>B',
                                'type': '<u1',
                                'Value': 'var' #See comment for active
                            }
                        }
                    },                                                                                                                      
                    'SET_CONFIG': {
                        'what': 'Sets the configuration',
                        'subPort': 4,
                        'inoutInfo': {
                            'args': ['<u2', '<u1', 'var'], #id, type, config
                            'returns': {
                                'err': '>B',
                            }
                        }
                    },   
                    'LOAD_MAIN2ACTIVE': {
                        'what': 'Load main configuration from file into active',
                        'subPort': 5,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },
                    'LOAD_FALLBACK2ACTIVE': {
                        'what': 'Load fallback configuration from file into active',
                        'subPort': 6,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },        
                    'LOAD_DEFAULT2ACTIVE': {
                        'what': 'Load default configuration from file into active',
                        'subPort': 7,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },   
                    'UNLOCK_CONFIG': {
                        'what': 'Unlock configuration for saving',
                        'subPort': 8,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },  
                    'LOCK_CONFIG': {
                        'what': 'Lock configuration from saving',
                        'subPort': 9,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    }, 
                    'SAVE_ACTIVE2MAIN': {
                        'what': 'Save active configuration to main file',
                        'subPort': 10,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },      
                    'SAVE_ACTIVE2FALLBACK': {
                        'what': 'Save active configuration to fallback file',
                        'subPort': 11,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },                                                                                                                              
                    'ELEVATE_ACCESS': {
                        'what': 'Elevates access role',
                        'subPort': 12,
                        'inoutInfo': {
                            'args': ['<u1', '<u4'],  # role, key (see docs)
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },                
                    'GET_STATUS': {
                        'what': 'Gets status and errors info',
                        'subPort': 13,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B',
                                'isInitialized': '<u1',
                                'isLocked': '<u1',
                                'isFallbackConfigurationLoaded': '<u1',
                                'isMainConfigurationLoaded': '<u1',
                                'wasFallbackRequested': '<u1',
                                'initSource': '<u1',
                                'currAccessRole': '<u1',
                                'totalNumofErrors': '<u1',
                                'numOfParameterDoesNotExistErrors': '<u1',
                                'numOfInvalidParameterTypeErrors': '<u1',
                                'numOfValidationFailErrors': '<u1',
                                'numOfStorageFailErrors': '<u1',
                                'numOfNotInitializedErrors': '<u1',
                                'numOfNotLoadedOnInitErrors': '<u1',
                                'numOfLockedErrors': '<u1',
                                'numOfAccessDeniedErrors': '<u1',
                                'numOfWrongPasswordErrors': '<u1',
                                'numOfUnknownErrors': '<u1',
                            }
                        }
                    },  
                }
            },  
                       
            'HOUSEKEEPING': {
                'port': 17,
                'subservice': {
                    'GET_HK': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['>u2', '>u2', '>u4'], #limit, before_id, before_time
                            'returns' : {
                                'err': '>b',
                                #packet meta
                                'final': '<B',
                                'UNIXtimestamp': '>u4',
                                'dataPosition': '>u2',
                                #ADCS
                                'Estimated_Angular_Rate_X': '>f4',
                                'Estimated_Angular_Rate_Y': '>f4',
                                'Estimated_Angular_Rate_Z': '>f4',
                                'Estimated_Angular_Angle_X': '>f4',
                                'Estimated_Angular_Angle_Y': '>f4',
                                'Estimated_Angular_Angle_Z': '>f4',
                                'Sat_Position_ECI_X': '>f4',
                                'Sat_Position_ECI_Y': '>f4',
                                'Sat_Position_ECI_Z': '>f4',
                                'Sat_Velocity_ECI_X': '>f4',
                                'Sat_Velocity_ECI_Y': '>f4',
                                'Sat_Velocity_ECI_Z': '>f4',
                                'Sat_Position_LLH_X': '>f4',
                                'Sat_Position_LLH_Y': '>f4',
                                'Sat_Position_LLH_Z': '>f4',
                                'ECEF_Position_X': '>i2',
                                'ECEF_Position_Y': '>i2',
                                'ECEF_Position_Z': '>i2',
                                'Coarse_Sun_Vector_X': '>f4',
                                'Coarse_Sun_Vector_Y': '>f4',
                                'Coarse_Sun_Vector_Z': '>f4',
                                'Fine_Sun_Vector_X': '>f4',
                                'Fine_Sun_Vector_Y': '>f4',
                                'Fine_Sun_Vector_Z': '>f4',
                                'Nadir_Vector_X': '>f4',
                                'Nadir_Vector_Y': '>f4',
                                'Nadir_Vector_Z': '>f4',
                                'Wheel_Speed_X': '>f4',
                                'Wheel_Speed_Y': '>f4',
                                'Wheel_Speed_Z': '>f4',
                                'Mag_field_vector_X': '>f4',
                                'Mag_field_vector_Y': '>f4',
                                'Mag_field_vector_Z': '>f4',
                                'Comm_Status': '>u2',
                                'Wheel1_Current': '>f4',
                                'Wheel2_Current': '>f4',
                                'Wheel3_Current': '>f4',
                                'CubeSense1_Current': '>f4',
                                'CubeSense2_Current': '>f4',
                                'CubeControl_Current3v3': '>f4',
                                'CubeControl_Current5v0': '>f4',
                                'CubeStar_Current': '>f4',
                                'CubeStart_Temp': '>f4',
                                'Magnetorquer_Current': '>f4',
                                'MCU_Temp': '>f4',
                                'Rate_Sensor_Temp_X': '>i2',
                                'Rate_Sensor_Temp_Y': '>i2',
                                'Rate_Sensor_Temp_Z': '>i2',
                                #Athena
                                'temparray1': '>i4',
                                'temparray2': '>i4',
                                'temparray3': '>i4',
                                'temparray4': '>i4',
                                'temparray5': '>i4',
                                'temparray6': '>i4',
                                #EPS
                                'cmd': '<B',
                                'status' : '<b',
                                'timestamp': '<f8',
                                'uptimeInS': '<u4',
                                'bootCnt': '<u4',
                                'gs_wdt_time_left_s': '<u4',
                                'counter_wdt_gs': '<u4',
                                'mpptConverterVoltage1_mV': '<u2',
                                'mpptConverterVoltage2_mV': '<u2',
                                'mpptConverterVoltage3_mV': '<u2',
                                'mpptConverterVoltage4_mV': '<u2',
                                'curSolarPanels1_mA': '<u2',
                                'curSolarPanels2_mA': '<u2',
                                'curSolarPanels3_mA': '<u2',
                                'curSolarPanels4_mA': '<u2',
                                'curSolarPanels5_mA': '<u2',
                                'curSolarPanels6_mA': '<u2',
                                'curSolarPanels7_mA': '<u2',
                                'curSolarPanels8_mA': '<u2',
                                'vBatt_mV': '<u2',
                                'curSolar_mA': '<u2',
                                'curBattIn_mA': '<u2',
                                'curBattOut_mA': '<u2',
                                'curOutput1_mA': '<u2',
                                'curOutput2_mA': '<u2',
                                'curOutput3_mA': '<u2',
                                'curOutput4_mA': '<u2',
                                'curOutput5_mA': '<u2',
                                'curOutput6_mA': '<u2',
                                'curOutput7_mA': '<u2',
                                'curOutput8_mA': '<u2',
                                'curOutput9_mA': '<u2',
                                'curOutput10_mA': '<u2',
                                'curOutput11_mA': '<u2',
                                'curOutput12_mA': '<u2',
                                'curOutput13_mA': '<u2',
                                'curOutput14_mA': '<u2',
                                'curOutput15_mA': '<u2',
                                'curOutput16_mA': '<u2',
                                'curOutput17_mA': '<u2',
                                'curOutput18_mA': '<u2',
                                'AOcurOutput1_mA': '<u2',
                                'AOcurOutput2_mA': '<u2',
                                'outputConverterVoltage1': '<u2',
                                'outputConverterVoltage2': '<u2',
                                'outputConverterVoltage3': '<u2',
                                'outputConverterVoltage4': '<u2',
                                'outputConverterVoltage5': '<u2',
                                'outputConverterVoltage6': '<u2',
                                'outputConverterVoltage7': '<u2',
                                'outputConverterVoltage8': '<u2',
                                'outputConverterState': '<B',  # 4 bits!
                                'outputStatus': '<u4',
                                'outputFaultStatus': '<u4',
                                'protectedOutputAccessCnt': '>u2',
                                'outputOnDelta1': '<u2',
                                'outputOnDelta2': '<u2',
                                'outputOnDelta3': '<u2',
                                'outputOnDelta4': '<u2',
                                'outputOnDelta5': '<u2',
                                'outputOnDelta6': '<u2',
                                'outputOnDelta7': '<u2',
                                'outputOnDelta8': '<u2',
                                'outputOnDelta9': '<u2',
                                'outputOnDelta10': '<u2',
                                'outputOnDelta11': '<u2',
                                'outputOnDelta12': '<u2',
                                'outputOnDelta13': '<u2',
                                'outputOnDelta14': '<u2',
                                'outputOnDelta15': '<u2',
                                'outputOnDelta16': '<u2',
                                'outputOnDelta17': '<u2',
                                'outputOnDelta18': '<u2',
                                'outputOffDelta1': '<u2',
                                'outputOffDelta2': '<u2',
                                'outputOffDelta3': '<u2',
                                'outputOffDelta4': '<u2',
                                'outputOffDelta5': '<u2',
                                'outputOffDelta6': '<u2',
                                'outputOffDelta7': '<u2',
                                'outputOffDelta8': '<u2',
                                'outputOffDelta9': '<u2',
                                'outputOffDelta10': '<u2',
                                'outputOffDelta11': '<u2',
                                'outputOffDelta12': '<u2',
                                'outputOffDelta13': '<u2',
                                'outputOffDelta14': '<u2',
                                'outputOffDelta15': '<u2',
                                'outputOffDelta16': '<u2',
                                'outputOffDelta17': '<u2',
                                'outputOffDelta18': '<u2',
                                'outputFaultCount1': '<B',
                                'outputFaultCount2': '<B',
                                'outputFaultCount3': '<B',
                                'outputFaultCount4': '<B',
                                'outputFaultCount5': '<B',
                                'outputFaultCount6': '<B',
                                'outputFaultCount7': '<B',
                                'outputFaultCount8': '<B',
                                'outputFaultCount9': '<B',
                                'outputFaultCount10': '<B',
                                'outputFaultCount11': '<B',
                                'outputFaultCount12': '<B',
                                'outputFaultCount13': '<B',
                                'outputFaultCount14': '<B',
                                'outputFaultCount15': '<B',
                                'outputFaultCount16': '<B',
                                'outputFaultCount17': '<B',
                                'outputFaultCount18': '<B',
                                'temp1_c': '<b',
                                'temp2_c': '<b',
                                'temp3_c': '<b',
                                'temp4_c': '<b',
                                'temp5_c': '<b',
                                'temp6_c': '<b',
                                'temp7_c': '<b',
                                'temp8_c': '<b',
                                'temp9_c': '<b',
                                'temp10_c': '<b',
                                'temp11_c': '<b',
                                'temp12_c': '<b',
                                'temp13_c': '<b',
                                'temp14_c': '<b',
                                'battMode': '<B',
                                'mpptMode': '<B',
                                'battHeaterMode': '<B',
                                'battHeaterState': '<B',
                                'PingWdt_toggles': '<u2',
                                'PingWdt_turnOffs': '<B',
                                #UHF
                                'scw1': '<B',
                                'scw2': '<B',
                                'scw3': '<B',
                                'scw4': '<B',
                                'scw5': '<B',
                                'scw6': '<B',
                                'scw7': '<B',
                                'scw8': '<B',
                                'scw9': '<B',
                                'scw10': '<B',
                                'scw11': '<B',
                                'scw12': '<B',
                                'freq': '>u4',
                                'pipe_t': '>u4',
                                'beacon_t': '>u4',
                                'audio_t': '>u4',
                                'uptime': '>u4',
                                'pckts_out': '>u4',
                                'pckts_in': '>u4',
                                'pckts_in_crc16': '>u4',
                                'temperature': '>f4',
                                #Sband
                                'Output_Power': '>f4',
                                'PA_Temp': '>f4',
                                'Top_Temp': '>f4',
                                'Bottom_Temp': '>f4',
                                'Bat_Current': '>f4',
                                'Bat_Voltage': '>f4',
                                'PA_Current': '>f4',
                                'PA_Voltage': '>f4',
                                #hyperion
                                'Nadir_Temp1': '>f4',
                                'Port_Temp1': '>f4',
                                'Port_Temp2': '>f4',
                                'Port_Temp3': '>f4',
                                'Port_Temp_Adc': '>f4',
                                'Port_Dep_Temp1': '>f4',
                                'Port_Dep_Temp2': '>f4',
                                'Port_Dep_Temp3': '>f4',
                                'Port_Dep_Temp_Adc': '>f4',
                                'Star_Temp1': '>f4',
                                'Star_Temp2': '>f4',
                                'Star_Temp3': '>f4',
                                'Star_Temp_Adc': '>f4',
                                'Star_Dep_Temp1': '>f4',
                                'Star_Dep_Temp2': '>f4',
                                'Star_Dep_Temp3': '>f4',
                                'Star_Dep_Temp_Adc': '>f4',
                                'Zenith_Temp1': '>f4',
                                'Zenith_Temp2': '>f4',
                                'Zenith_Temp3': '>f4',
                                'Zenith_Temp_Adc': '>f4',
                                'Nadir_Pd1': '>f4',
                                'Port_Pd1': '>f4',
                                'Port_Pd2': '>f4',
                                'Port_Pd3': '>f4',
                                'Port_Dep_Pd1': '>f4',
                                'Port_Dep_Pd2': '>f4',
                                'Port_Dep_Pd3': '>f4',
                                'Star_Pd1': '>f4',
                                'Star_Pd2': '>f4',
                                'Star_Pd3': '>f4',
                                'Star_Dep_Pd1': '>f4',
                                'Star_Dep_Pd2': '>f4',
                                'Star_Dep_Pd3': '>f4',
                                'Zenith_Pd1': '>f4',
                                'Zenith_Pd2': '>f4',
                                'Zenith_Pd3': '>f4',
                                'Port_Voltage': '>f4',
                                'Port_Dep_Voltage': '>f4',
                                'Star_Voltage': '>f4',
                                'Star_Dep_Voltage': '>f4',
                                'Zenith_Voltage': '>f4',
                                'Port_Current': '>f4',
                                'Port_Dep_Current': '>f4',
                                'Star_Current': '>f4',
                                'Star_Dep_Current': '>f4',
                                'Zenith_Current': '>f4',
                                

                            }
                        }
                    },
                    'SET_MAX_FILES': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['<u2'], #number of hk entries to store
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'GET_MAX_FILES': {
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'max': '>u2'
                            }
                        }
                    }
                }
            },

            'GROUND_STATION_WDT': {
                'port': 16,  # As per EPS docs
                'subservice': {
                    'RESET_WDT': {
                        'what': 'Resets the ground station watchdog timer',
                        'subPort': 0,
                        'inoutInfo': {
                            'args': ['<u2'],  # key (see docs)
                            'returns': {
                                'err': '>B'
                            }
                        }
                    },
                    'GET_WDT_REMAINING': {
                        'what': 'Gets GS watchdog time left in seconds',
                        'subPort': 1,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B',
                                'timeLeftInS': '<u4'
                            }
                        }
                    },
                    'CLEAR_WDT_RESET_MARK': {
                        'what': 'Clears GS watchdog reset mark',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': ['<u2'],  # key (see docs)
                            'returns': {
                                'err': '>B',
                            }
                        }
                    },
                    'CHECK_STARTUP_POST_RESET': {
                        'what': 'Checks if startup happened after GS watchdog reset',
                        'subPort': 3,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>B',
                                'startupAfterGsWdt': '?',
                            }
                        }
                    }
                }
            },

            'EPS_RESET': {
                'port': 15,  # As per EPS docs
                'subservice': {
                    'EPS_HARD_RESET': {  # Not recommended to use by the operator
                        'what': 'Does a hard reset on EPS (Resets the config)',
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['<u2'],  # 17767
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                }
            },

            'REBOOT': {
                'port': 4,  # As per CSP docs
                # EPS soft reset
                # Not recommended to use by the operator
                # no subport (command ID) needed.
                'subservice':{
                    'SOFT': {                	
                        'what': 'Does a soft reset on EPS (reboot)',
                        'subPort': 128,
                        'inoutInfo': {
                            'args': ['<u4'],  # 491527 or 2147975175
                            'returns': {
                                'err': '>b',
                            }
                        }
                    }
                }
                # magic number 0x80078007 must be sent with csp port 4 and no subport number
            },

            'CLI': {
                # EPS SPECIFIC
                'port': 7,  # EPS remote CLI uses port 13 unless Otherwise specified
                'subservice': {
                    'GENERAL_TELEMETRY': {
                        'what': 'Gets the general housekeeping telemetry data',
                        'subPort': 0,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'timestamp': '<f8',
                                'uptimeInS': '<u4',
                                'bootCnt': '<u4',
                                'gs_wdt_time_left_s': '<u4',
                                'counter_wdt_gs': '<u4',
                                'mpptConverterVoltage1_mV': '<u2',
                                'mpptConverterVoltage2_mV': '<u2',
                                'mpptConverterVoltage3_mV': '<u2',
                                'mpptConverterVoltage4_mV': '<u2',
                                'curSolarPanels1_mA': '<u2',
                                'curSolarPanels2_mA': '<u2',
                                'curSolarPanels3_mA': '<u2',
                                'curSolarPanels4_mA': '<u2',
                                'curSolarPanels5_mA': '<u2',
                                'curSolarPanels6_mA': '<u2',
                                'curSolarPanels7_mA': '<u2',
                                'curSolarPanels8_mA': '<u2',
                                'vBatt_mV': '<u2',
                                'curSolar_mA': '<u2',
                                'curBattIn_mA': '<u2',
                                'curBattOut_mA': '<u2',
                                'curOutput1_mA': '<u2',
                                'curOutput2_mA': '<u2',
                                'curOutput3_mA': '<u2',
                                'curOutput4_mA': '<u2',
                                'curOutput5_mA': '<u2',
                                'curOutput6_mA': '<u2',
                                'curOutput7_mA': '<u2',
                                'curOutput8_mA': '<u2',
                                'curOutput9_mA': '<u2',
                                'curOutput10_mA': '<u2',
                                'curOutput11_mA': '<u2',
                                'curOutput12_mA': '<u2',
                                'curOutput13_mA': '<u2',
                                'curOutput14_mA': '<u2',
                                'curOutput15_mA': '<u2',
                                'curOutput16_mA': '<u2',
                                'curOutput17_mA': '<u2',
                                'curOutput18_mA': '<u2',
                                'AOcurOutput1_mA': '<u2',
                                'AOcurOutput2_mA': '<u2',
                                'outputConverterVoltage1': '<u2',
                                'outputConverterVoltage2': '<u2',
                                'outputConverterVoltage3': '<u2',
                                'outputConverterVoltage4': '<u2',
                                'outputConverterVoltage5': '<u2',
                                'outputConverterVoltage6': '<u2',
                                'outputConverterVoltage7': '<u2',
                                'outputConverterVoltage8': '<u2',
                                'outputConverterState': '<B',  # 4 bits!
                                'outputStatus': '<u4',
                                'outputFaultStatus': '<u4',
                                'protectedOutputAccessCnt': '<u2',
                                'outputOnDelta1': '<u2',
                                'outputOnDelta2': '<u2',
                                'outputOnDelta3': '<u2',
                                'outputOnDelta4': '<u2',
                                'outputOnDelta5': '<u2',
                                'outputOnDelta6': '<u2',
                                'outputOnDelta7': '<u2',
                                'outputOnDelta8': '<u2',
                                'outputOnDelta9': '<u2',
                                'outputOnDelta10': '<u2',
                                'outputOnDelta11': '<u2',
                                'outputOnDelta12': '<u2',
                                'outputOnDelta13': '<u2',
                                'outputOnDelta14': '<u2',
                                'outputOnDelta15': '<u2',
                                'outputOnDelta16': '<u2',
                                'outputOnDelta17': '<u2',
                                'outputOnDelta18': '<u2',
                                'outputOffDelta1': '<u2',
                                'outputOffDelta2': '<u2',
                                'outputOffDelta3': '<u2',
                                'outputOffDelta4': '<u2',
                                'outputOffDelta5': '<u2',
                                'outputOffDelta6': '<u2',
                                'outputOffDelta7': '<u2',
                                'outputOffDelta8': '<u2',
                                'outputOffDelta9': '<u2',
                                'outputOffDelta10': '<u2',
                                'outputOffDelta11': '<u2',
                                'outputOffDelta12': '<u2',
                                'outputOffDelta13': '<u2',
                                'outputOffDelta14': '<u2',
                                'outputOffDelta15': '<u2',
                                'outputOffDelta16': '<u2',
                                'outputOffDelta17': '<u2',
                                'outputOffDelta18': '<u2',
                                'outputFaultCount1': '<B',
                                'outputFaultCount2': '<B',
                                'outputFaultCount3': '<B',
                                'outputFaultCount4': '<B',
                                'outputFaultCount5': '<B',
                                'outputFaultCount6': '<B',
                                'outputFaultCount7': '<B',
                                'outputFaultCount8': '<B',
                                'outputFaultCount9': '<B',
                                'outputFaultCount10': '<B',
                                'outputFaultCount11': '<B',
                                'outputFaultCount12': '<B',
                                'outputFaultCount13': '<B',
                                'outputFaultCount14': '<B',
                                'outputFaultCount15': '<B',
                                'outputFaultCount16': '<B',
                                'outputFaultCount17': '<B',
                                'outputFaultCount18': '<B',
                                'temp1_c': '<b',
                                'temp2_c': '<b',
                                'temp3_c': '<b',
                                'temp4_c': '<b',
                                'temp5_c': '<b',
                                'temp6_c': '<b',
                                'temp7_c': '<b',
                                'temp8_c': '<b',
                                'temp9_c': '<b',
                                'temp10_c': '<b',
                                'temp11_c': '<b',
                                'temp12_c': '<b',
                                'temp13_c': '<b',
                                'temp14_c': '<b',
                                'battMode': '<B',
                                'mpptMode': '<B',
                                'battHeaterMode': '<B',
                                'battHeaterState': '<B',
                                'PingWdt_toggles': '<u2',
                                'PingWdt_turnOffs': '<B',
                            }
                        }
                    },
                    # ALL the EPS CLI commands:
                    'SET_TELEMETERY_PERIOD': {
                        'what': 'Set telemetery collection period on EPS',
                        'subPort': 255,
                        'inoutInfo': {
                            # magicWord (refer to docs), telem. ID, period
                            # (ms), duration (s)
                            'args': ['<u4', '<B', '<u4', '<u4'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            },

            'CONTROL': {
                # EPS SPECIFIC
                'port': 14,
                'subservice': {
                    # POWER OUTPUTS
                    'SINGLE_OUTPUT_CONTROL': {
                        'what': 'Turns on/off a power output channel (with a defined delay)',
                        'subPort': 0,
                        'inoutInfo': {
                            # output num., state, delay (s)
                            'args': ['<B', '<B', '<u2'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ALL_OUTPUT_CONTROL': {
                        'what': 'Sets all ouputs status at once (nth bit -> nth channel',
                        'subPort': 1,
                        'inoutInfo': {
                            'args': ['<u4'],  # binary 18-bit
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SINGLE_OUTPUT_CONTROL_NORMAL_BATT': {
                        'what': 'Set the output channels mode on normal battery mode',
                        'subPort': 9,
                        'inoutInfo': {
                            # output num., state, delay (s)
                            'args': ['<B', '<B', '<u2'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },

                    # SOLAR PANEL INPUTS & MPPT
                    'SET_SINGLE_MPPT_CONV_V': {
                        'what': 'Sets single MPPT converter voltage',
                        'subPort': 2,
                        'inoutInfo': {
                            'args': ['<B', '<u2'],  # channel, voltage (mv)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_ALL_MPPT_CONV_V': {
                        'what': 'Sets all MPPT converter voltage at once',
                        'subPort': 3,
                        'inoutInfo': {
                            'args': ['<u2', '<u2', '<u2', '<u2'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_MODE_MPPT': {
                        'what': 'Sets MPPT mode',
                        'subPort': 4,
                        'inoutInfo': {
                            # 0-Hw, 1-manual, 2-auto, 3-auto w/ timeout
                            'args': ['<B'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'SET_AUTO_TIMEOUT_MPPT': {
                        'what': 'Sets MPPT auto timeout period',
                        'subPort': 5,
                        'inoutInfo': {
                            'args': ['<u4'],  # timeout
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },

                    # BATTERY HEATER
                    'SET_HEATER_MODE': {
                        'what': 'Manual, or automatic',
                        'subPort': 6,
                        'inoutInfo': {
                            'args': ['<B'],  # Mode (see docs)
                            'returns': {
                                'status': '>b'  # 0 = success
                            }
                        }
                    },
                    'SET_HEATER_STATE': {
                        'what': 'On, or off',
                        'subPort': 7,
                        'inoutInfo': {
                            'args': ['<B', '<u2'],  # state, duration (s)
                            'returns': {
                                'err': '>b'
                            }
                        }
                    }
                }
            },
            'UPDATER' : {
                'port': 12,
                'subservice': {
                    'FLASH_UPDATE': {
                        'what' : 'GOLDEN_IMAGE ONLY Flashes file VOL0:/application_image.bin from filesystem to working image',
                        'subPort': 0,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'GET_GOLDEN_INFO': {
                        'what': "Get golden image metadata",
                        'subPort': 1,
                        'inoutInfo': {
                            'args' : None,
                            'returns': {
                                'err'    : '>b',
                                'exists' : '>u4',
                                'size'   : '>u4',
                                'addr'   : '>u4',
                                'crc'    : '>u2'
                            }
                        }
                    },
                    'GET_APP_INFO' : {
                        'what': "Get working image metadata",
                        'subPort': 2,
                        'inoutInfo': {
                            'args' : None,
                            'returns': {
                                'err'    : '>b',
                                'exists' : '>u4',
                                'size'   : '>u4',
                                'addr'   : '>u4',
                                'crc'    : '>u2'
                            }
                        }
                    },
                    'SET_APP_ADDRESS' : {
                        'what': 'Set the starting address of the working image',
                        'subPort' : 3,
                        'inoutInfo' : {
                            'args' : ['>u4'],
                            'returns' : {
                                'err' : '>b'
                            }
                        }
                    },
                    'SET_APP_CRC' : {
                        'what': 'Set the starting address of the working image',
                        'subPort' : 4,
                        'inoutInfo' : {
                            'args' : ['>u2'],
                            'returns' : {
                                'err' : '>b'
                            }
                        }
                    },
                    'ERASE_APP' : {
                        'what' : 'Erase working image',
                        'subPort' : 5,
                        'inoutInfo' : {
                            'args' : None,
                            'returns' : {
                                'err' : '>b'
                            }
                        }
                    },
                    'VERIFY_APP' : {
                        'what' : 'Verify crc of working image',
                        'subPort' : 6,
                        'inoutInfo' : {
                            'args' : None,
                            'returns' : {
                                'err' : '>b'
                            }
                        }
                    },
                    'VERIFY_GOLDEN' : {
                        'what' : 'Verify crc of golden image',
                        'subPort' : 7,
                        'inoutInfo' : {
                            'args' : None,
                            'returns' : {
                                'err' : '>b'
                            }
                        }
                    }
                }
            },

            'LOGGER': {
                'port': 13,
                'subservice': {
                    'GET_FILE': {
                        'subPort': 0,
                        'inoutInfo': {
                            'args': [],
                            'returns': {
                                'err': '>b',
                                'log': '>S500',
                            }
                        }
                    },
                    'GET_OLD_FILE': {
                        'subPort': 1,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'log': '>S500',
                            }
                        }
                    },
                    'SET_FILE_SIZE': {
                        'subPort': 3,
                        'inoutInfo': {
                            'args': ['>u4'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'GET_FILE_SIZE': {
                        'subPort': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'size': '>u4'
                            }
                        }
                    }
                }
            },

            'adcs': { # refer to the adcs service
                'port': 18,
                'subservice': {
                    'ADCS_RESET': {
                        'subport': 0,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_RESET_LOG_POINTER': {
                        'subport': 1,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_ADVANCE_LOG_POINTER': {
                        'subport': 2,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_RESET_BOOT_REGISTERS': {
                        'subport': 3,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_FORMAT_SD_CARD': {
                        'subport': 4,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_ERASE_FILE': {
                        'subport': 5,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1'], #file_type, file_counter, erase_all
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_LOAD_FILE_DOWNLOAD_BLOCK': {
                        'subport': 6,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u4', '>u2'], #file_type, file_counter, offset, block_length
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_ADVANCE_FILE_LIST_READ_POINTER': {
                        'subport': 7,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_INITIATE_FILE_UPLOAD': {
                        'subport': 8,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'], # file_dest, block_size
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_FILE_UPLOAD_PACKET': {
                        'subport': 9,
                        'inoutInfo': {
                            'args': ['>u2', '>u1'], # packet_number, file_bytes
                            'returns': {
                                'err': '>b',
                                'file_bytes': '>b'
                            }
                        }
                    },
                    'ADCS_FINALIZE_UPLOAD_BLOCK': {
                        'subport': 10,
                        'inoutInfo': {
                            'args': ['>u2', '>u4', 'u2'], # file_dest, offset, block_length
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_RESET_UPLOAD_BLOCK': {
                        'subport': 11,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_RESET_FILE_LIST_READ_POINTER': {
                        'subport': 12,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_INITIATE_DOWNLOAD_BURST': {
                        'subport': 13,
                        'inoutInfo': {
                            'args': ['>u1', '>?'], # msg_legnth, ignore_hole_map
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_GET_NODE_IDENTIFICATION': {
                        'subport': 14,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Node_Type': '>u1',
                                'Interface_Ver': '>u1',
                                'Major_Firm_Ver': '>u1',
                                'Minor_Firm_Ver': '>u1',
                                'Runtime_S': '>u2',
                                'Runtime_Ms': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_BOOT_PROGRAM_STAT': {
                        'subport': 15,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Mcu_Reset_Cause': '>u1',
                                'Boot_Cause': '>u1',
                                'Boot_Count': '>u2',
                                'Boot_Idx': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_BOOT_INDEX': {
                        'subport': 16,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Program_Idx': '>u1',
                                'Boot_Stat': '>u1',
                            }
                        }
                    },
                    'ADCS_GET_LAST_LOGGED_EVENT': {
                        'subport': 17,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Time': '>u4',
                                'Event_Id': '>u1',
                                'Event_Param': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_SD_FORMAT_PROCESS': {
                        'subport': 18,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'FormT_Busy': '>?',
                                'Erase_All_Busy': '>?',
                            }
                        }
                    },
                    'ADCS_GET_TC_ACK': {
                        'subport': 19,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Last_Tc_Id': '>u1',
                                'Tc_Processed': '>?',
                                'Tc_Err_Stat': '>b'
                            }
                        }
                    },
                    'ADCS_GET_FILE_DOWNLOAD_BUFFER': {
                        'subport': 20,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Packet_Count': '>u2',
                                'File': '>u4', #TODO: array
                            }
                        }
                    },
                    'ADCS_GET_FILE_DOWNLOAD_BLOCK_STAT': {
                        'subport': 21,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Ready': '>?',
                                'Param_Err': '?',
                                'Crc16_Checksum': '>u2',
                                'Length': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_FILE_INFO': {
                        'subport': 22,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Type': '>u1',
                                'Updating': '?',
                                'Size': '>u4',
                                'Time': '>u4',
                                'Crc16_Checksum': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_INIT_UPLOAD_STAT': {
                        'subport': 23,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Busy': '>?',
                            }
                        }
                    },
                    'ADCS_GET_FINALIZE_UPLOAD_STAT': {
                        'subport': 24,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Busy': '>?',
                                'Error': '>?'
                            }
                        }
                    },
                    'ADCS_GET_UPLOAD_CRC16_CHECKSUM': {
                        'subport': 25,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Checksum': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_SRAM_LATCHUP_COUNT': {
                        'subport': 26,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Sram1': '>u2',
                                'Sram2': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_EDAC_ERR_COUNT': {
                        'subport': 27,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Single_Sram': '>u2',
                                'Double_Sram': '>u2',
                                'Multi_Sram': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_COMMS_STAT': {
                        'subport': 28,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Comm_Status': '>u2',
                            }
                        }
                    },
                    'ADCS_SET_CACHE_EN_STATE': {
                        'subport': 29,
                        'inoutInfo': {
                            'args': ['>?'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_SRAM_SCRUB_SIZE': {
                        'subport': 30,
                        'inoutInfo': {
                            'args': ['>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_UNIXTIME_SAVE_CONFIG': {
                        'subport': 31,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_HOLE_MAP': {
                        'subport': 32,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                                'Hole_Map': '>u1'
                            }
                        }
                    },
                    'ADCS_SET_UNIX_T': {
                        'subport': 33,
                        'inoutInfo': {
                            'args': ['>u4', '>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_GET_CACHE_EN_STATE': {
                        'subport': 34,
                        'inoutInfo': {
                            'args': ['>?'],
                            'returns': {
                                'err': '>b',
                                'En_State': '>?'
                            }
                        }
                    },
                    'ADCS_GET_SRAM_SCRUB_SIZE': {
                        'subport': 35,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Size': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_UNIXTIME_SAVE_CONFIG': {
                        'subport': 36,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'When': '>u1',
                                'Period': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_HOLE_MAP': {
                        'subport': 37,
                        'inoutInfo': {
                            'args': ['>u1'], #num
                            'returns': {
                                'err': '>b',
                                'Hole_Map': '>u1',
                            }
                        }
                    },
                    'ADCS_GET_UNIX_T': {
                        'subport': 38,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Unix_t': '>u4',
                                'Count_Ms': '>u2'
                            }
                        }
                    },
                    'ADCS_CLEAR_ERR_FLAGS': {
                        'subport': 39,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_BOOT_INDEX': {
                        'subport': 40,
                        'inoutInfo': {
                            'args': ['>u1'], #index
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_RUN_SELECTED_PROGRAM': {
                        'subport': 41,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_READ_PROGRAM_INFO': {
                        'subport': 42,
                        'inoutInfo': {
                            'args': ['>u1'], #index
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_COPY_PROGRAM_INTERNAL_FLASH': {
                        'subport': 43,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'], #index, overwrite_flag
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_GET_BOOTLOADER_STATE': {
                        'subport': 44,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Uptime': '>u2',
                                'Flags_arr': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_PROGRAM_INFO': {
                        'subport': 45,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Index': '>u1',
                                'Busy': '>?',
                                'File_Size': '>u4',
                                'Crc16_Checksum': '>u2'
                            }
                        }
                    },
                    'ADCS_COPY_INTERNAL_FLASH_PROGRESS': {
                        'subport': 46,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Error': '>?',
                                'Busy': '>?',
                            }
                        }
                    },
                    'ADCS_DEPLOY_MAGNETOMETER_BOOM': {
                        'subport': 47,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_ENABLED_STATE': {
                        'subport': 48,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_CLEAR_LATCHED_ERRS': {
                        'subport': 49,
                        'inoutInfo': {
                            'args': ['>?', '>?'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_ATTITUDE_CTR_MODE': {
                        'subport': 50,
                        'inoutInfo': {
                            'args': ['>u1', '>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_ATTITUDE_ESTIMATE_MODE': {
                        'subport': 51,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_TRIGGER_ADCS_LOOP': {
                        'subport': 52,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_TRIGGER_ADCS_LOOP_SIM': {
                        'subport': 53,
                        'inoutInfo': {
                            'args': None, #TODO: sim_sensor_data type ?
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_ASGP4_RUNE_MODE': {
                        'subport': 54,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_TRIGGER_ASGP4': {
                        'subport': 55,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_MTM_OP_MODE': {
                        'subport': 56,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_CNV2JPG': {
                        'subport': 57,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SAVE_IMG': {
                        'subport': 58,
                        'inoutInfo': {
                            'args': ['>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SAVE_CONFIG': {
                        'subport': 61,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SAVE_ORBIT_PARAMS': {
                        'subport': 62,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_GET_JPG_CNV_PROGESS': {
                        'subport': 64,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Percentage': '>u1',
                                'Result': '>u1',
                                'File_Counter': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_CUBEACP_STATE': {
                        'subport': 65,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Flags_Arr': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_SAT_POS_LLH': {
                        'subport': 66,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'X': '>f4',
                                'Y': '>f4',
                                'Z': '>f4',
                            }
                        }
                    },
                    'ADCS_GET_EXECUTION_TIMES': {
                        'subport': 67,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Adcs_Update': '>u2',
                                'Sensor_Comm': '>u2',
                                'Sgp4_propag': '>u2',
                                'Igrf_model': '>u2'
                            }
                        }
                    },
                    'ADCS_GET_ACP_LOOP_STAT': {
                        'subport': 68,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Time': '>u2',
                                'Execution_point': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_IMG_SAVE_PROGRESS': {
                        'subport': 69,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Percentage': '>u1',
                                'Status': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_MEASUREMENTS': {
                        'subport': 70,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Magnetic_field_X': 'f4',
                                'Magnetic_field_Y': 'f4',
                                'Magnetic_field_Z': 'f4',
                                'Coarse_Sun_X': 'f4',
                                'Coarse_Sun_Y': 'f4',
                                'Coarse_Sun_Z': 'f4',
                                'Sun_X': 'f4',
                                'Sun_Y': 'f4',
                                'Sun_Z': 'f4',
                                'Nadir_X': 'f4',
                                'Nadir_Y': 'f4',
                                'Nadir_Z': 'f4',
                                'Angular_Rate_X': 'f4',
                                'Angular_Rate_Y': 'f4',
                                'Angular_Rate_Z': 'f4',
                                'Wheel_Speed_X': 'f4',
                                'Wheel_Speed_Y': 'f4',
                                'Wheel_Speed_Z': 'f4',
                                'Star1b_X': 'f4',
                                'Star1b_Y': 'f4',
                                'Star1b_Z': 'f4',
                                'Star1o_X': 'f4',
                                'Star1o_Y': 'f4',
                                'Star1o_Z': 'f4',
                                'Star2b_X': 'f4',
                                'Star2b_Y': 'f4',
                                'Star2b_Z': 'f4',
                                'Star2o_X': 'f4',
                                'Star2o_Y': 'f4',
                                'Star2o_Z': 'f4',
                                'Star3b_X': 'f4',
                                'Star3b_Y': 'f4',
                                'Star3b_Z': 'f4',
                                'Star3o_X': 'f4',
                                'Star3o_Y': 'f4',
                                'Star3o_Z': 'f4',
                            }
                        }
                    },
                    'ADCS_GET_ACTUATOR': {
                        'subport': 71,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Magnetorquer_X': '>f4',
                                'Magnetorquer_Y': '>f4',
                                'Magnetorquer_Z': '>f4',
                                'Wheel_Speed_X': '>f4',
                                'Wheel_Speed_Y': '>f4',
                                'Wheel_Speed_Z': '>f4',
                            }
                        }
                    },
                    'ADCS_GET_ESTIMATION': {
                        'subport': 72,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Igrf_magnetic_field_X': 'f4',
                                'Igrf_magnetic_field_Y': 'f4',
                                'Igrf_magnetic_field_Z': 'f4',
                                'Sun_X': 'f4',
                                'Sun_Y': 'f4',
                                'Sun_Z': 'f4',
                                'Gyro_bias_X': 'f4',
                                'Gyro_bias_Y': 'f4',
                                'Gyro_bias_Z': 'f4',
                                'Innovation_X': 'f4',
                                'Innovation_Y': 'f4',
                                'Innovation_Z': 'f4',
                                'Quaternion_Err_X': 'f4',
                                'Quaternion_Err_Y': 'f4',
                                'Quaternion_Err_Z': 'f4',
                                'Quaternion_Covar_X': 'f4',
                                'Quaternion_Covar_X': 'f4',
                                'Quaternion_Covar_X': 'f4',
                                'Angular_Rate_Covar_X': 'f4',
                                'Angular_Rate_Covar_Y': 'f4',
                                'Angular_Rate_Covar_Z': 'f4',
                            }
                        }
                    },
                    'ADCS_GET_ASGP4': {
                        'subport': 73,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Epoch': 'f4',
                                'Inclination': 'f4',
                                'RAAN': 'f4',
                                'ECC': 'f4',
                                'AOP': 'f4',
                                'MA': 'f4',
                                'MM': 'f4',
                                'Bstar': 'f4',
                            }
                        }
                    },
                    'ADCS_GET_RAW_SENSOR': {
                        'subport': 74,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Cam1_Centroid_X': '>i2',
                                'Cam1_Centroid_Y': '>i2',
                                'Cam1_Capture_Stat': '>u1',
                                'Cam1_Detect_Result': '>u1',
                                'Cam2_Centroid_X': '>i2',
                                'Cam2_Centroid_Y': '>i2',
                                'Cam2_Capture_Stat': '>u1',
                                'Cam2_Detect_Result': '>u1',
                                'Css': '>O20',
                                'MTM_X': 'f8',
                                'MTM_Y': 'f8',
                                'MTM_Z': 'f8',
                                'Rate_X': 'f8',
                                'Rate_Y': 'f8',
                                'Rate_Z': 'f8',

                            }
                        }
                    },
                    'ADCS_GET_RAW_GPS': {
                        'subport': 75,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Sol_Stat': '>u1',
                                'Tracked_Sats': '>u1',
                                'UsedInSol_Sats': '>u1',
                                'Xyz_Lof_Count': '>u1',
                                'Range_Log_Count': '>u1',
                                'Response_Msg': '>u1',
                                'Reference_Week': '>u2',
                                'Time': '>u4',
                                'X_Pos': '>i4',
                                'X_Vel': '>i2',
                                'Y_Pos': '>i4',
                                'Y_Vel': '>i2',
                                'Z_Pos': '>i4',
                                'Z_Vel': '>i2',
                                'Pos_Std_Dev_X': '>f4',
                                'Pos_Std_Dev_Y': '>f4',
                                'Pos_Std_Dev_Z': '>f4',
                                'Vel_Std_Dev_X': '>u1',
                                'Vel_Std_Dev_Y': '>u1',
                                'Vel_Std_Dev_Z': '>u1',
                            }
                        }
                    },
                    'ADCS_GET_STAR_TRACKER': {
                        'subport': 76,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Detected_Stars': '>u1',
                                'Img_noise': '>u1',
                                'Invalid_stars': '>u1',
                                'Identified_stars': '>u1',
                                'Identification_mode': '>u1',
                                'Img_dark_val': '>u1',
                                'flags_arr': '>O20',
                                'Sample_T': '>u2',
                                'Star1_Confidence': '>u1',
                                'Star1_magnitude': '>u2',
                                'Star1_Catalouge_Num': '>u2',
                                'Star1_Centroid_X': '>i2',
                                'Star1_Centroid_Y': '>i2',
                                'Star2_Confidence': '>u1',
                                'Star2_magnitude': '>u2',
                                'Star2_Catalouge_Num': '>u2',
                                'Star2_Centroid_X': '>i2',
                                'Star2_Centroid_Y': '>i2',
                                'Star3_Confidence': '>u1',
                                'Star3_magnitude': '>u2',
                                'Star3_Catalouge_Num': '>u2',
                                'Star3_Centroid_X': '>i2',
                                'Star3_Centroid_Y': '>i2',
                                'Capture_T': '>u2',
                                'Detect_T': '>u2',
                                'Identification_T': '>u2',
                                'Estimated_Rate_X': '>f4',
                                'Estimated_Rate_Y': '>f4',
                                'Estimated_Rate_Z': '>f4',
                                'Estimated_Att_X': '>f4',
                                'Estimated_Att_Y': '>f4',
                                'Estimated_Att_Z': '>f4',
                            }
                        }
                    },
                    'ADCS_GET_MTM2_MEASUREMENTS': {
                        'subport': 77,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Mag_X': '>i2',
                                'Mag_Y': '>i2',
                                'Mag_Z': '>i2',
                            }
                        }
                    },
                    'ADCS_GET_POWER_TEMP': {
                        'subport': 78,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Cubesense1_3v3_I': '>f4',
                                'Cubesense1_CamSram_I': '>f4',
                                'Cubesense2_3v3_I': '>f4',
                                'Cubesense2_CamSram_I': '>f4',
                                'Cubecontrol_3v3_I': '>f4',
                                'cubecontrol_5v_I': '>f4',
                                'Cubecontrol_vBat_I': '>f4',
                                'wheel1_I': '>f4',
                                'wheel2_I': '>f4',
                                'wheel3_I': '>f4',
                                'Cubestar_I': '>f4',
                                'Magnetorquer_I': '>f4',
                                'Cubestar_Temp': '>f4',
                                'MCU_temp': '>f4',
                                'MTM_temp': '>f4',
                                'MTM2_temp': '>f4',
                                'Rate_Sensor_Temp_X': '>i2',
                                'Rate_Sensor_Temp_Y': '>i2',
                                'Rate_Sensor_Temp_Z': '>i2',
                            }
                        }
                    },
                    'ADCS_SET_POWER_CONTROL': {
                        'subport': 79,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                                'Control': '>u1'
                            }
                        }
                    },
                    'ADCS_GET_POWER_CONTROL': {
                        'subport': 80,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Control': '>u1'
                            }
                        }
                    },
                    'ADCS_SET_ATTITUDE_ANGLE': {
                        'subport': 81,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4' ], # xyz type
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_GET_ATTITUDE_ANGLE': {
                        'subport': 82,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'X': '>f4',
                                'Y': '>f4',
                                'Z': '>f4'
                            }
                        }
                    },
                    'ADCS_SET_TRACK_CONTROLLER': {
                        'subport': 83,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4' ], # xyz type
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_GET_TRACK_CONTROLLER': {
                        'subport': 84,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'X': '>f4',
                                'Y': '>f4',
                                'Z': '>f4'
                            }
                        }
                    },
                    'ADCS_SET_LOG_CONFIG': {
                        'subport': 85,
                        'inoutInfo': {
                            'args': ['>O20', '>u2'], # array type?, period
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_GET_LOG_CONFIG': {
                        'subport': 86,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Flag_arr': '>O20',
                                'Period': '>u2',
                                'Dest': '>u1',
                                'Log': '>u1'
                            }
                        }
                    },
                    'ADCS_SET_INERTIAL_REF': {
                        'subport': 87,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_GET_INERTIAL_REF': {
                        'subport': 88,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'X': '>f4',
                                'Y': '>f4',
                                'Z': '>f4'
                            }
                        }
                    },
                    'ADCS_SET_SGP4_ORBIT_PARAMS': {
                        'subport': 89,
                        'inoutInfo': {
                            'args': ['>f8', '>f8', '>f8', '>f8', '>f8', '>f8', '>f8', '>f8'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_GET_SGP4_ORBIT_PARAMS': {
                        'subport': 90,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'Inclination': '>f8',
                                'ECC': '>f8',
                                'RAAN': '>f8',
                                'AOP': '>f8',
                                'Bstar': '>f8',
                                'MM': '>f8',
                                'MA': '>f8',
                                'Epoch': '>f8'
                            }
                        }
                    },
                    'ADCS_SET_SYSTEM_CONFIG': {
                        'subport': 91,
                        'inoutInfo': {
                            'args': None, #TODO: finish args
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_GET_SYSTEM_CONFIG': {
                        'subport': 92,
                        'inoutInfo': {
                            'args': None, 
                            'returns': {
                                'err': '>b',
                                'Acp_Type': '>u1',
                                'Special_Ctrl_Sel': '>u1',
                                'CC_sig_ver': '>u1',
                                'CC_motor_ver': '>u1',
                                'CS1_ver': '>u1',
                                'CS2_ver': '>u1',
                                'CS1_cam': '>u1',
                                'CS2_cam': '>u1',
                                'CubeStar_Ver': '>u1',
                                'GPS': '>u1',
                                'Include_MTM2': '>?',
                                'MTQ_max_dipole_X': '>f4',
                                'MTQ_max_dipole_Y': '>f4',
                                'MTQ_max_dipole_Z': '>f4',
                                'MTQ_ontime_res': '>f4',
                                'MTQ_max_ontime': '>f4',
                                'RW_max_torque_X': '>f4',
                                'RW_max_torque_Y': '>f4',
                                'RW_max_torque_Z': '>f4',
                                'RW_max_moment_X': '>f4',
                                'RW_max_moment_Y': '>f4',
                                'RW_max_moment_Z': '>f4',
                                'RW_inertia_X': '>f4',
                                'RW_inertia_Y': '>f4',
                                'RW_inertia_Z': '>f4',
                                'RW_torque_inc': '>f4',
                                'MTM1_bias_d1_X': '>f4',
                                'MTM1_bias_d1_Y': '>f4',
                                'MTM1_bias_d1_Z': '>f4',
                                'MTM1_bias_d2_X': '>f4',
                                'MTM1_bias_d2_Y': '>f4',
                                'MTM1_bias_d2_Z': '>f4',
                                'MTM1_sens_s1_X': '>f4',
                                'MTM1_sens_s1_Y': '>f4',
                                'MTM1_sens_s1_Z': '>f4',
                                'MTM1_sens_s2_X': '>f4',
                                'MTM1_sens_s2_Y': '>f4',
                                'MTM1_sens_s2_Z': '>f4',
                                'MTM2_bias_d1_X': '>f4',
                                'MTM2_bias_d1_Y': '>f4',
                                'MTM2_bias_d1_Z': '>f4',
                                'MTM2_bias_d2_X': '>f4',
                                'MTM2_bias_d2_Y': '>f4',
                                'MTM2_bias_d2_Z': '>f4',
                                'MTM2_sens_s1_X': '>f4',
                                'MTM2_sens_s1_Y': '>f4',
                                'MTM2_sens_s1_Z': '>f4',
                                'MTM2_sens_s2_X': '>f4',
                                'MTM2_sens_s2_Y': '>f4',
                                'MTM2_sens_s2_Z': '>f4',
                                'CC_Signal_Port': '>u1',
                                'CC_Signal_Pin': '>u1',
                                'CC_Motor_Port': '>u1',
                                'CC_Motor_Pin': '>u1',
                                'CC_Common_Port': '>u1',
                                'CC_Common_Pin': '>u1',
                                'CS1_Port': '>u1',
                                'CS1_Pin': '>u1',
                                'CS2_Port': '>u1',
                                'CS2_Pin': '>u1',
                                'CubeStar_Port': '>u1',
                                'CubeStar_Pin': '>u1',
                                'CW1_Port': '>u1',
                                'CW1_Pin': '>u1',
                                'CW2_Port': '>u1',
                                'CW2_Pin': '>u1',
                                'CW3_Port': '>u1',
                                'CW3_Pin': '>u1',
                            }
                        }
                    },
                    'ADCS_SET_MTQ_CONFIG': {
                        'subport': 93,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b'
                            }
                        }
                    },
                    'ADCS_SET_RW_CONFIG': {
                        'subport': 94,
                        'inoutInfo': {
                            'args': ['>u1'],
                            'returns': {
                                'err': '>b',
                                'RW': '>u1'
                            }
                        }
                    },
                    'ADCS_SET_RATE_GYRO': {
                        'subport': 95,
                        'inoutInfo': {
                            'args': ['>u1', '>u1', '>u1', '>f4', '>f4', '>f4', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_CSS_CONFIG': {
                        'subport': 96,
                        'inoutInfo': {
                            'args': ['>O20', '>O20', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_STAR_TRACK_CONFIG': {
                        'subport': 97,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>u2', '>u2', '>u1', '>u1', '>u1', '>u2', '>u1', '>u1', '>u1', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>u1', '>u1', '>u1', '>?', '>?', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_CUBESENSE_CONFIG': {
                        'subport': 98,
                        'inoutInfo': {
                            'args': None, #TODO: finish args, why does this have so many args ~.~
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_MTM_CONFIG': {
                        'subport': 99,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>O20'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_DETUMBLE_CONFIG': {
                        'subport': 100,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>f4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_YWHEEL_CONFIG': {
                        'subport': 101,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>f4', '>f4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_TRACKING_CONFIG': {
                        'subport': 102,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_MOI_MAT': {
                        'subport': 103,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>f4', '>f4', '>f4'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_ESTIMATION_CONFIG': {
                        'subport': 104,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>u1', '>u1', '>u1', '>u1'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_USERCODED_SETTING': {
                        'subport': 105,
                        'inoutInfo': {
                            'args': ['>O20', '>O20'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_SET_ASGP4_SETTING': {
                        'subport': 106,
                        'inoutInfo': {
                            'args': ['>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>f4', '>u1', '>f4', '>f4', '>u1', '>f4', '>f4', '>u1', '>f4', '>f4', '>u2'],
                            'returns': {
                                'err': '>b',
                            }
                        }
                    },
                    'ADCS_GET_FULL_CONFIG': {
                        'subport': 107,
                        'inoutInfo': {
                            'args': None,
                            'returns': {
                                'err': '>b',
                                'ADCS_config': '>O20'
                            }
                        }
                    },
                }
            }
        }
