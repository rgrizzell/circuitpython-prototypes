"""CircuitPython Example -- Encrypted File"""
import aesio
import adafruit_hashlib as hashlib
from binascii import hexlify
import json
import os

try:
    from circuitpython_typing import Union
except ImportError:
    pass


class EncryptedFile:
    """Takes a piece of data, encrypts it, and writes it to a file.

    Utilizes AES library available on most boards.
    """
    def __init__(self, path, key, mode=aesio.MODE_CTR):
        m = hashlib.sha256()
        m.update(key)

        self._path = path
        self._iv = os.urandom(16)
        self._mode = mode
        self._key = m.digest()

    def decrypt(self, encoding="utf-8") -> Union[bytes, str]:
        """Decrypts the volume and returns the decrypted data.

        :param str encoding: Codec used to transform string objects. Defaults to `utf-8`.
        :return: Bytes or string representation of the object.
        :rtype: bytes
        """
        cipher = aesio.AES(self._key, 6, self._iv)
        with open(self._path, 'rb') as volume:
            data_in = volume.read()
        data = bytearray(len(data_in))
        cipher.decrypt_into(data_in, data)
        data = bytes(data)

        if encoding:
            data = data.decode(encoding)

        return data

    def encrypt(self, data: Union[bytes, bytearray, str], encoding: str = "utf-8") -> bytes:
        """Encrypt the provided data and write it out to the file.

        :param data: Data to be encrypted and written to the file.
        :type data: Union[bytes, bytearray, str]
        :param str encoding: Codec used to transform string objects. Defaults to `utf-8`.
        :return: Returns the encrypted data
        :rtype: bytes
        """
        if isinstance(data, str):
            data = bytes(data, encoding)

        cipher = aesio.AES(self._key, 6, self._iv)
        data_out = bytearray(len(data))
        with open(self._path, 'wb') as volume:
            cipher.encrypt_into(data, data_out)
            volume.write(data_out)

        return data_out


if __name__ == "__main__":
    vol = EncryptedFile("/test.txt.aes", "password1")
    test_data = {"foo": "bar"}

    print(test_data)
    print(hexlify(vol.encrypt(json.dumps(test_data))))
    print(vol.decrypt())
