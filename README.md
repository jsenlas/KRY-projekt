# KRY-projekt

We will send the *loremimsum.txt* to the recepient ciphered by post quantum algorithm. 

```
usage: kry.py [-h] [-c ALGORITHM] [-d ALGORITHM] [-s ALGORITHM] [-v ALGORITHM] [-k PUBLIC_KEY] [-n SIGNATURE]
              [--log]
              file

positional arguments:
  file                  Filename

optional arguments:
  -h, --help            show this help message and exit

cipher/decipher files:
  -c ALGORITHM, --cipher ALGORITHM
                        cipher a file
  -d ALGORITHM, --decipher ALGORITHM
                        Decipher a file

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

KRY 2022 project - cipher/decipher or sign a file.
```

## Examples

Signing file.
```python3 kry.py -s SPHINXPLUS  loremipsum.txt```
And verifying signature.
```python3 kry.py -n ./out/loremipsum.txt_dir_2022-03-12T16_32_54/loremipsum.txt.signature -k ./out/loremipsum.txt_dir_2022-03-12T16_32_54/loremipsum.txt.pbkey -v SPHINXPLUS loremipsum.txt```

## Development

For making it easier for development we created a simple Makefile that let's you do first setup, installation, cleanup and meassuring quality of code.

### Setup

```
python3 -m venv kryenv            # create virtual environment - run only once
source ./kryenv/bin/activate      # go to virtual environment
pip3 install -r requirements.txt  # install python libraries
```

### Cleanup

```
make remove_out
make clear_log
````

### Example run
Sign a file using SPHINX+
```
make sign
```

### Quality

We try to stay as high as possible :) 
- 10/10 is the goal. 
- 8/10 at least please :D

```
make pylint
```
**this checks every python file and prints out collective score I *SUGGEST* to run** ``` pylint yourfile.py``` **for you to know score of your file and keep it above 8.0**