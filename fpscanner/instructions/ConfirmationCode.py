# MIT License
#
# Copyright (c) 2018 Alexey Nikitin
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
class ConfirmationCode:
    def __init__(self, code):
        # type: (int) -> ConfirmationCode
        self.code = code

    def is_success(self):
        # type: () -> bool
        return self.code == 0x00

    def as_str(self):
        # type: () -> str
        if self.code == 0x00:
            return 'Success'
        elif self.code == 0x01:
            return 'Error when receiving data package'
        elif self.code == 0x02:
            return 'No finger on the sensor'
        elif self.code == 0x03:
            return 'Fail to enroll the finger'
        elif self.code == 0x06:
            return 'Fail to generate character file due to the over-disorderly fingerprint image'
        elif self.code == 0x07:
            return 'Fail to generate character file due to lackness of character point or over-smallness of fingerprint image'
        elif self.code == 0x08:
            return 'Finger doesn\'t match'
        elif self.code == 0x09:
            return 'Fail to find the matching finger'
        elif self.code == 0x0A:
            return 'Fail to combine the character files'
        elif self.code == 0x0B:
            return 'Addressing PageID is beyond the finger library'
        elif self.code == 0x0C:
            return 'Error when reading template from library or the template is invalid'
        elif self.code == 0x0D:
            return 'Error when uploading template'
        elif self.code == 0x0E:
            return 'Module can\'t receive the following data packages'
        elif self.code == 0x0F:
            return 'Error when uploading image'
        elif self.code == 0x10:
            return 'Fail to delete the template'
        elif self.code == 0x11:
            return 'Fail to clear finger library'
        elif self.code == 0x15:
            return 'Fail to generate the image for the lackness of valid primary image'
        elif self.code == 0x18:
            return 'Error when writing flash'
        elif self.code == 0x19:
            return 'No definition error'
        elif self.code == 0x1A:
            return 'Invalid register number'
        elif self.code == 0x1B:
            return 'Incorrect configuration of register'
        elif self.code == 0x1C:
            return 'Wrong notepad page number'
        elif self.code == 0x1D:
            return 'Fail to operate the communication port'
        else:
            return 'Unknown error! Help!'
