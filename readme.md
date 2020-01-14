# Python driver for fingerprint sensors by Zhiantec - ZFM-20 series

[![PyPI version](https://badge.fury.io/py/fpscanner.svg)](https://badge.fury.io/py/fpscanner)
[![PDD status](http://www.0pdd.com/svg?name=nikialeksey/fpscanner)](http://www.0pdd.com/p?name=nikialeksey/fpscanner)

## Is your scanner can be managed by this library?
If your scanner is ZFM-20 or his cheap clone then it possible. I made this library inspired by 
[pyfingerprint](https://github.com/bastianraschke/pyfingerprint), so it may also work with ZFM-60, ZFM-70, ZFM-100,
R303 and R305.

## Origin manuals
Fingerprint protocol specs are taken from 
[original ZHM-20 user manual](https://raw.githubusercontent.com/nikialeksey/fpscanner/master/ZFM+user+manualV15.pdf).

## Terminology

**Image**

  Image is a Fingerprint scanned grayscale image. Image can be scanned and stored in volatile image buffer.
   
**Characteristic**

  Characteristic is a fingerprint characteristic. It represented by a bytearray. Characteristic can be created from 
  fingerprint image and stored in volatile characteristic buffer.
  
**Template**

  Template is a registered fingerprint model stored in scanner nonvolatile memory. 
  We can not see or feel the template, we only can ask scanner if characteristic look like some template 
  in scanner memory.
  
## Working with sensor
 
### Handshake
 
First of all you need make a handshake to verify connection:
 ```python
with SerialPort(Serial(port='<COM1 or /dev/ttyUSB0>', baudrate=9600 * 6, timeout=2)) as port:
    rq = RqCommand(port)
    rs = RsSimple(port)
    Handshake(rq, rs).make()
```
As you see you will need to know serial port name of your scanner device. For windows users it may looks like `COM1`,
for unix users it may looks like `/dev/ttyUSB0`.

### Fingerprint image

More complex task - make an image of your fingerprint:
```python
with SerialPort(Serial(port='...', baudrate=9600 * 6, timeout=2)) as port:
    rq = RqCommand(port)
    rs = RsSimple(port)
    print 'Waiting for finger...'
    while not Scan(rq, rs).is_scanned():
        pass
    print 'Finger has been scanned! Downloading the finger image...'
    image = UpImage(rq, rs).image()
    image.show()
```

### Matching characteristics

Another more complex task - match characteristics of two fingerprints. Fingerprint scanner can matching only two 
fingerprints and it has two buffers for that operation - `RqCharBuffer1` and `RqCharBuffer2`.
```python
with SerialPort(Serial(port='...', baudrate=9600 * 6, timeout=2)) as port:
    rq = RqCommand(port)
    rs = RsSimple(port)
    print 'Wait for finger...'
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer1()).execute()

    print 'Once again...'
    while not Scan(rq, rs).is_scanned():
        pass
    Img2Tz(rq, rs, RqCharBuffer2()).execute()

    print 'Score {0}'.format(Match(rq, rs).score())
```

### Enroll fingerprint

Another complex task is enroll a finger.
```python
with SerialPort(Serial(port='...', baudrate=9600 * 6, timeout=2)) as port:
    rq = RqCommand(port)
    rs = RsSimple(port)
    print 'Wait for finger...'
    while not Scan(rq, rs).is_scanned():
        pass

    Img2Tz(rq, rs, RqCharBuffer1()).execute()
    searchResult = Search(rq, rs, start=0, count=TemplateCount(rq, rs).as_int()).execute()

    if searchResult.code() == 0:
        print 'Template already exist'
        exit(1)

    print 'Once again...'
    while not Scan(rq, rs).is_scanned():
        pass

    Img2Tz(rq, rs, RqCharBuffer2()).execute()
    score = Match(rq, rs).score()
    RegModel(rq, rs).execute()
    Store(rq, rs, RqCharBuffer1(), 1).execute()
    print 'Stored success!'
```

@todo #1:30m Add deletion enrolled fingers