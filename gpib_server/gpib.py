#!/usr/bin/env python3
#
# Redirect data from a TCP/IP connection to a serial port and vice versa.
#
# (C) 2002-2016 Chris Liechti <cliechti@gmx.net>
#
# SPDX-License-Identifier:    BSD-3-Clause

import sys
import socket
import time
import binascii
import pyvisa
from timeit import default_timer as timer


#class SerialToNet(serial.threaded.Protocol):
#    """serial->socket"""
#
#    def __init__(self):
#        self.socket = None
#
#    def __call__(self):
#        return self
#
#    def data_received(self, data):
#        if self.socket is not None:
#            self.socket.sendall(data)

if __name__ == '__main__':  # noqa
    import argparse

    parser = argparse.ArgumentParser(
        description='Simple Serial to Network (TCP/IP) redirector.',
        epilog="""\
NOTE: no security measures are implemented. Anyone can remotely connect
to this service over the network.

Only one connection at once is supported. When the connection is terminated
it waits for the next connect.
""")


    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress non error messages',
        default=False)

    parser.add_argument(
        '--develop',
        action='store_true',
        help='Development mode, prints Python internals on errors',
        default=False)

#    group = parser.add_argument_group('serial port')
#
#    group.add_argument(
#        "--bytesize",
#        choices=[5, 6, 7, 8],
#        type=int,
#        help="set bytesize, one of {5 6 7 8}, default: 8",
#        default=8)
#
#    group.add_argument(
#        "--parity",
#        choices=['N', 'E', 'O', 'S', 'M'],
#        type=lambda c: c.upper(),
#        help="set parity, one of {N E O S M}, default: N",
#        default='N')
#
#    group.add_argument(
#        "--stopbits",
#        choices=[1, 1.5, 2],
#        type=float,
#        help="set stopbits, one of {1 1.5 2}, default: 1",
#        default=1)
#
#    group.add_argument(
#        '--rtscts',
#        action='store_true',
#        help='enable RTS/CTS flow control (default off)',
#        default=False)
#
#    group.add_argument(
#        '--xonxoff',
#        action='store_true',
#        help='enable software flow control (default off)',
#        default=False)
#
#    group.add_argument(
#        '--rts',
#        type=int,
#        help='set initial RTS line state (possible values: 0, 1)',
#        default=None)
#
#    group.add_argument(
#        '--dtr',
#        type=int,
#        help='set initial DTR line state (possible values: 0, 1)',
#        default=None)

    group = parser.add_argument_group('network settings')

    exclusive_group = group.add_mutually_exclusive_group()

    exclusive_group.add_argument(
        '-P', '--localport',
        type=int,
        help='local TCP port',
        default=7777)

    exclusive_group.add_argument(
        '-c', '--client',
        metavar='HOST:PORT',
        help='make the connection as a client, instead of running a server',
        default=False)

    args = parser.parse_args()

    # connect to gpib port
    rm = pyvisa.ResourceManager()
    gpib = rm.open_resource("GPIB0::1::INSTR")
    #gpib = rm.open_resource('USB0::62700::60986::SDS2XJBD1R2754::0::INSTR')
    #gpib = rm.open_resource('TCPIP::192.168.1.177')

    if not args.quiet:
        sys.stderr.write(
            '--- TCP/IP to GPIB redirect ---\n'
            '--- type Ctrl-C / BREAK to quit\n')

#    try:
#        ser.open()
#    except serial.SerialException as e:
#        sys.stderr.write('Could not open serial port {}: {}\n'.format(ser.name, e))
#        sys.exit(1)

#    ser_to_net = SerialToNet()
#    serial_worker = serial.threaded.ReaderThread(ser, ser_to_net)
#    serial_worker.start()

    if not args.client:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('', args.localport))
        srv.listen(1)
    try:
        intentional_exit = False
        while True:
            if args.client:
                host, port = args.client.split(':')
                sys.stderr.write("Opening connection to {}:{}...\n".format(host, port))
                client_socket = socket.socket()
                try:
                    client_socket.connect((host, int(port)))
                except socket.error as msg:
                    sys.stderr.write('WARNING: {}\n'.format(msg))
                    time.sleep(5)  # intentional delay on reconnection as client
                    continue
                sys.stderr.write('Connected\n')
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                #~ client_socket.settimeout(5)
            else:
                sys.stderr.write('Waiting for connection on {}...\n'.format(args.localport))
                client_socket, addr = srv.accept()
                sys.stderr.write('Connected by {}\n'.format(addr))
                # More quickly detect bad clients who quit without closing the
                # connection: After 1 second of idle, start sending TCP keep-alive
                # packets every 1 second. If 3 consecutive keep-alive packets
                # fail, assume the client is gone and close the connection.
                try:
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                except AttributeError:
                    pass # XXX not available on windows
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            try:
                #ser_to_net.socket = client_socket
                # enter network <-> serial loop
                while True:
                    try:
                        data2gpib = client_socket.recv(65536)
                        if not data2gpib:
                            break
                        
                        start_time = timer()

                        sys.stderr.write('send all: {}\n'.format(data2gpib))

                        if False:
                            gpib.write_raw(data2gpib)
                            data2gpib_str = data2gpib.decode("utf-8").strip()
                            if data2gpib_str.find("?") != -1:
    
                                try:
                                    gpib.timeout = 5000
                                    data = gpib.read_raw(200000000)
                                    sys.stderr.write('DATA: {}, len({})\n'.format(data, len(data)))
                                    if data:
                                        client_socket.sendall(data)
                                except pyvisa.errors.VisaIOError:
                                    pass
                                        #client_socket.sendall(b'')

                        messages = data2gpib.split(b'\n')
                        for m in messages:
                            if m == b'':
                                break;

                            m_str = m.decode("utf-8").strip()
                            sys.stderr.write('send: {}\n'.format(m))
                            gpib.write_raw(m)

                            if m_str.find("?") != -1:

                                try:
                                    gpib.timeout = 5000
                                    data = gpib.read_raw(200000000)
                                    sys.stderr.write('DATA: {}, len({})\n'.format(data, len(data)))
                                    if data:
                                        client_socket.sendall(data)
                                except pyvisa.errors.VisaIOError:
                                    pass
                                        #client_socket.sendall(b'')

                    except socket.error as msg:
                        if args.develop:
                            raise
                        sys.stderr.write('ERROR: {}\n'.format(msg))
                        # probably got disconnected
                        break

#                    data = gpib.read_raw()
#                    sys.stderr.write('DATA: {}\n'.format(data))
#                    if data:
#                        client_socket.sendall(data)

                    elapsed_time = timer() - start_time
                    sys.stderr.write('elapsed time: {}\n'.format(elapsed_time))

            except KeyboardInterrupt:
                intentional_exit = True
                raise
            except socket.error as msg:
                if args.develop:
                    raise
                sys.stderr.write('ERROR: {}\n'.format(msg))
            finally:
                # ser_to_net.socket = None
                sys.stderr.write('Disconnected\n')
                client_socket.close()
                if args.client and not intentional_exit:
                    time.sleep(5)  # intentional delay on reconnection as client
    except KeyboardInterrupt:
        pass

    sys.stderr.write('\n--- exit ---\n')
#    serial_worker.stop()
