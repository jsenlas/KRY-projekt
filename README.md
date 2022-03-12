# KRY-projekt

We will send the *loremimsum.txt* to the recepient cyphered by post quantum algorithm. 

```python
usage: kry.py [-h] [-c ALGORITHM] [-d ALGORITHM] [-s ALGORITHM] [-v ALGORITHM] [-k PUBLIC_KEY] [-n SIGNATURE]
              [--log]
              file

positional arguments:
  file                  Filename

optional arguments:
  -h, --help            show this help message and exit

cypher/decypher files:
  -c ALGORITHM, --cypher ALGORITHM
                        Cypher a file
  -d ALGORITHM, --decypher ALGORITHM
                        Decypher a file

Signing and verifying file signature:
  -s ALGORITHM, --sign ALGORITHM
                        Signing, available options are SPHINXPLUS,
  -v ALGORITHM, --verify ALGORITHM
                        Verify signature using algorithms - SPHINXPLUS,
  -k PUBLIC_KEY, --public_key PUBLIC_KEY
                        File containing public key.
  -n SIGNATURE, --signature SIGNATURE
                        File containing signature.
  --log                 Log to separate file in the generated directory.

KRY 2022 project - cypher/decypher or sign a file.
```

## Examples

Signing file.
```python3 kry.py -s SPHINXPLUS  loremipsum.txt```
And verifying signature.
```python3 kry.py -n ./out/loremipsum.txt_dir_2022-03-12T16_32_54/loremipsum.txt.signature -k ./out/loremipsum.txt_dir_2022-03-12T16_32_54/loremipsum.txt.pbkey -v SPHINXPLUS loremipsum.txt```
