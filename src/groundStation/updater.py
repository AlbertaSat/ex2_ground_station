
import time
import os
import binascii

try:
    from .uTransceiver import uTransceiver
except:
    print("uTranceiver module not built!")

try: # We are importing this file for use on the website (comm.py)
    from ex2_ground_station_software.src.groundStation.groundStation import groundStation, options
    from ex2_ground_station_software.src.groundStation.system import SystemValues
    import libcsp.build.libcsp_py3 as libcsp
except ImportError: # We are using this file directly or through cli.py
    from groundStation.groundStation import groundStation, options
    from groundStation.system import SystemValues
    import libcsp_py3 as libcsp

def crc16(data : bytes):
    if data is None:
        return 0
    return binascii.crc_hqx(data, 0)

class updater(groundStation):
    def __init__(self, opts):
        super(updater, self).__init__(opts)
        self.blocksize = opts.blocksize
        if self.blocksize % 32 != 0:
            raise ValueError("Blocksize must be a multiple of 32")
        self.filename = opts.file
        self.file = open(self.filename, "rb")
        self.filesize = os.path.getsize(self.filename)
        if self.filesize == 0:
            raise ValueError("File size is null")
        if opts.crc == None:
            self.file_crc = self.crc(self.file.read())
        else:
            self.file_crc = opts.crc
        self.file.seek(0)
        self.doresume = opts.resume
        self.address = opts.address
        self.uTrns = None
        if (opts.u):
            self.uTrns = uTransceiver()

    def crc(self, data):
        return crc16(data)

    def transaction(self, buf):
        """ Execute CSP transaction - send and receive on one RDP connection and
        return parsed packet """
        self.handlePipeMode()
        conn = self.get_conn();
        if conn is None:
            print('Error: Could not connection')
            return False
        if conn is None:
            print('Error: Could not connection')
            return {}
        libcsp.send(conn, buf)
        libcsp.buffer_free(buf)
        rxDataList = []
        packet = libcsp.read(conn, 10000)
        if packet is None:
            print('Did not receive response')
            return None
        rxDataList = []
        data = bytearray(libcsp.packet_get_data(packet))
        length = libcsp.packet_get_length(packet)
        rxDataList.append(self.parser.parseReturnValue(
            libcsp.conn_dst(conn),
            libcsp.conn_src(conn),
            libcsp.conn_sport(conn),
            data,
            length))
        return rxDataList

    def get_conn(self):
        server = self.vals.APP_DICT.get(self.satellite)
        port = self.vals.SERVICES.get('UPDATER').get('port')
        return self.__connectionManager__(server,port)

    def get_init_packet(self):
        server, port, toSend = self.getInput(None, inVal="{}.updater.INITIALIZE_UPDATE({},{},{})".format(self.satellite, self.address, self.filesize, self.file_crc))
        return toSend

    def get_block_update_packet(self, data):
        subservice = self.vals.SERVICES.get('UPDATER').get('subservice').get('PROGRAM_BLOCK').get('subPort')
        out = bytearray()
        out.extend(subservice.to_bytes(1, byteorder='big'))
        out.extend(self.address.to_bytes(4, byteorder='big'))
        out.extend(len(data).to_bytes(2, byteorder='big'))
        out.extend(crc16(data).to_bytes(2, byteorder='big'))
        out.extend(data)
        #print(out)
        toSend = libcsp.buffer_get(len(out))
        libcsp.packet_set_data(toSend, out)
        return toSend

    def get_resume_packet(self):
        server, port, toSend = self.getInput(None, inVal="{}.updater.GET_PROGRESS()".format(self.satellite))
        return toSend

    def send_update(self):
        skip = 0;
        print("here")
        if self.doresume:
            resume_packet = self.get_resume_packet()
            data = self.transaction(resume_packet);
            if (len(data) == 0):
                print("Could not initialize connection")
                return False
            if data[0]['err'] == -1:
                print("Error response from resume packet")
                return False
            d = data[0]
            print(d);
            if self.file_crc != d['crc'] :
                print("Crc of input file differs from CRC of file the satellite is expecting")
                exit(1)
            self.address = int(d['next_addr'])
            skip = int(d['next_addr'] - d['start_addr']);
            print("Skip: {}".format(skip))
            self.file.read(skip) # move the filepointer ahead by the size already sent
        else:
            init_packet = self.get_init_packet()
            data = self.transaction(init_packet)
            if (len(data) == 0):
                print("Could not initialize connection")
                return False
            if data[0]['err'] == -1:
                print("Error response from init packet")
                return False

        b = bytearray()
        total_blocks = self.filesize // self.blocksize;
        current_block = skip // self.blocksize
        while True:
            b = self.file.read(self.blocksize)
            if len(b) == 0:
                break
            update_packet = self.get_block_update_packet(b)
            print("Sending block {}/{}".format(current_block, total_blocks));
            current_block += 1;
            data = self.transaction(update_packet)
            if (len(data) == 0):
                print("Did not receive response from data packet")
                return False
            if data[0]['err'] != 0:
                print("error from data packet")
                return False;
            self.address += len(b)
        
        return True



class update_options(options):
    def __init__(self):
        super().__init__();

    def getOptions(self):
        self.parser.add_argument(
            '-f',
            '--file',
            type=str,
            help='Binary to upload')
        self.parser.add_argument(
            '-b',
            '--blocksize',
            type=int,
            default='512',
            help='Number of bytes to send at a time')
        self.parser.add_argument(
            '-a',
            '--address',
            type=lambda x: int(x,0),
            default='0x00200000',
            help='address to flash update on OBC')
        self.parser.add_argument(
            '-r',
            '--resume',
            action='store_true',
            help="Attempt to resume update if possible"
        )
        self.parser.add_argument(
            '-c',
            '--crc',
            type=lambda x: int(x,0),
            default=None,
            help="Provide file CRC. Can be hex or decimal"
        )

        return super().getOptions();


    