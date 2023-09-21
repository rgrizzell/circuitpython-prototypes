# Encrypted File

Takes a piece of data, encrypts it, and writes it to a file.

```python
vol = EncryptedFile("/test.txt.aes", "password1")
test_data = {"foo": "bar"}

print(test_data)
print(hexlify(vol.encrypt(json.dumps(test_data))))
print(vol.decrypt())
```
The test data is encrypted, written to disk, then decrypted again.
```text
Auto-reload is off.
code.py output:
{'foo': 'bar'}
b'19cb196bd4efb0b86a038c68c55d'
{"foo": "bar"}

Code done running.
```
Looking at the file, we see the encrypted data.
```text
$ cat test.txt.aes
\�+�3���BoO⏎ 
```
