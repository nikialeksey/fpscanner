from serial import Serial

from fpscanner.communication import RqCommand
from fpscanner.communication import RsCheckHeader
from fpscanner.communication import RsCheckSum
from fpscanner.communication import RsSimple
from fpscanner.communication.port import SerialPort
from fpscanner.communication.rqbuffer import RqCharBuffer1
from fpscanner.communication.rqbuffer import RqCharBuffer2
from fpscanner.instructions import Handshake
from fpscanner.instructions import Search
from fpscanner.instructions.characteristic import Match
from fpscanner.instructions.characteristic import RegModel
from fpscanner.instructions.image import Img2Tz
from fpscanner.instructions.image import Scan
from fpscanner.instructions.image import UpImage
from fpscanner.instructions.template import Store
from fpscanner.instructions.template import TemplateCount

with SerialPort(Serial(port='COM6', baudrate=9600 * 6, timeout=2)) as port:
    rq = RqCommand(port)
    rs = RsCheckHeader(RsCheckSum(RsSimple(port)))
    Handshake(rq, rs).make()

    print TemplateCount(rq, rs).as_int()

    print 'Waiting for finger...'
    while not Scan(rq, rs).is_scanned():
        pass
    print 'Finger has been scanned! Downloading the finger image...'
    image = UpImage(rq, rs).image()
    image.show()

    # enroll
    print 'Wait for finger...'
    while not Scan(rq, rs).is_scanned():
        pass

    Img2Tz(rq, rs, RqCharBuffer1()).execute()
    searchResult = Search(rq, rs, 0, TemplateCount(rq, rs).as_int(), RqCharBuffer1()).execute()

    if searchResult.code() == 0:
        print 'Template already exist'
        exit(1)

    print 'Once again...'
    while not Scan(rq, rs).is_scanned():
        pass

    Img2Tz(rq, rs, RqCharBuffer2()).execute()
    score = Match(rq, rs).score()
    RegModel(rq, rs).execute()
    Store(rq, rs, RqCharBuffer1(), 2).execute()
    print 'Stored success!'

    # Match score
    print 'Wait for finger...'
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer1()).execute()

    print 'Once again...'
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer2()).execute()

    print 'Score {0}'.format(Match(rq, rs).score())
