import struct
import asyncio
import logging


def no_op(*args):
    return


class UDPTrackerProtocol(asyncio.Protocol):
    PROTOCOL = 0x41727101980              #: UDP identification
    MAX_CONNECTIONS = 0xffffffffffffffff  #: unsigned long long

    def __init__(self,
                 server: TrackerServer):
        """ Creates the UDP version of the tracker. """

        self.server = server
        self.logger = server.logger
        self.conn_lost_recv = asyncio.Event()

    def error(self, tid, msg):
        return struct.pack('!II', 3, tid) + msg

    def error_received(self, exc):
        self.logger.error('Error received: '.format(exc))

    def connection_made(self, transport):
        pass

    def connection_lost(self, exc):
        pass

    def data_received(self, data):
        if len(data) < 16:
            self.logger.warning('Datagram smaller than 16 bytes')
            return

        # get the information about our connection
        prefix, suffix = data[:16], data[16:]

        # !QII => unsigned long long, unsigned int, unsigned int
        conn_id, action, transaction_id = struct.unpack('!QII', prefix)

        actions = {
            0: self.process_connect,
            1: self.process_announce
        }

    def process_announce(self, addr, conn, tid, data):
        pass

    def process_connect(self, addr, conn, tid, data):
        pass

    def process_scrape(self):
        pass


class TrackerServer:
    def __init__(self,
                 host: str='localhost',
                 port: int=6880,
                 refresh_interval: int=300,
                 conn_valid_interval: int=120,
                 loop=None):
        """ Creates a new BitTorrent tracker server. """

        self.host = host
        self.port = port
        self.addr = (host, port)

        self.refresh_interval = refresh_interval
        self.connection_valid_period = conn_valid_interval

        # obtain an event loop
        self.loop = loop or asyncio.get_event_loop()

        self.activity = {}
        self.connections = {}
        self.torrents = {}

        # wait for the server to start
        self.started = asyncio.Event()

        # logging anyone?
        self.logger = logging.getLogger(__name__)

    async def start(self):
        pass

    async def stop(self):
        pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
