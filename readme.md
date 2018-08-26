# Python driver for fingerprint sensors by Zhiantec - ZFM-20 series

## Is your scanner can be managed by this library?
If your scanner is ZFM-20 or his cheap clone then it possible. I made this library inspired by 
[pyfingerprint](https://github.com/bastianraschke/pyfingerprint), so it may also work with ZFM-60, ZFM-70, ZFM-100,
R303 and R305.

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