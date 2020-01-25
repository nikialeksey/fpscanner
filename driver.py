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
from fpscanner.instructions.characteristic import LoadChar
from fpscanner.instructions.characteristic import Match
from fpscanner.instructions.characteristic import RegModel
from fpscanner.instructions.image import Img2Tz
from fpscanner.instructions.image import Scan
from fpscanner.instructions.image import UpImage
from fpscanner.instructions.template import Store
from fpscanner.instructions.template import TemplateCount

with SerialPort(Serial(port='COM5', baudrate=9600 * 6, timeout=2)) as port:
    rq = RqCommand(port)
    rs = RsCheckHeader(RsCheckSum(RsSimple(port)))
    Handshake(rq, rs).make()

    print('Registered fingers count: {0}'.format(TemplateCount(rq, rs).as_int()))

    print('\n### Show the fingerprint:')
    print('Waiting for finger...')
    while not Scan(rq, rs).is_scanned():
        pass
    print('Finger has been scanned! Downloading the finger image...')
    image = UpImage(rq, rs).image()
    image.show()

    print('\n### Enroll new finger:')
    print('Wait for finger...')
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer1()).execute()
    searchResult = Search(rq, rs, start=0, count=TemplateCount(rq, rs).as_int()).execute()
    if searchResult.code() == 0:
        print('Template already exist')
    else:
        print('Once again...')
        while not Scan(rq, rs).is_scanned():
            pass
        Img2Tz(rq, rs, RqCharBuffer2()).execute()
        print('Score {0}'.format(Match(rq, rs).score()))
        RegModel(rq, rs).execute()
        newFingerIndex = TemplateCount(rq, rs).as_int()
        Store(rq, rs, RqCharBuffer1(), newFingerIndex).execute()
        print('Stored success!')

    print('\n### Match two fingers:')
    print('Wait for finger...')
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer1()).execute()

    print('Once again...')
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer2()).execute()

    print('Score {0}'.format(Match(rq, rs).score()))

    print('\n### Match scanned finger with it db version:')
    print('Wait for finger...')
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer1()).execute()  # save scanned finger to the buffer 1

    templatesCount = TemplateCount(rq, rs).as_int()  # get all templates count
    searchResult = Search(rq, rs, start=0, count=templatesCount).execute()  # find finger in the db

    if searchResult.code() != 0:
        print('Finger has not been saved!')
    else:
        number = searchResult.number()  # finger index in the db
        print('Finger found in index {0}'.format(number))
        LoadChar(rq, rs, RqCharBuffer2(), number).execute()  # extract original template to the buffer 2

        print('Score {0}'.format(Match(rq, rs).score()))  # Match it!
