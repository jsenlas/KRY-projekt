# KRY-projekt

We will send the *loremimsum.txt* to the recepient ciphered by post quantum algorithm. 

```
usage: kry.py [-h] [--log] {ntru_g,ntru_e,ntru_d,sphinx_sign,sphinx_verify} ...

positional arguments:
  {ntru_g,ntru_e,ntru_d,sphinx_sign,sphinx_verify}
                        cipher/decipher
    ntru_g              Generating key
    ntru_e              Encrypting message
    ntru_d              Decrypting message
    sphinx_sign         Signing a file
    sphinx_verify       Verifying file signature

optional arguments:
  -h, --help            show this help message and exit
  --log                 Log to separate file in the generated directory.

KRY 2022 project - cipher/decipher or sign a file.

```

### NTRU usage

#### Generate
```
usage: kry.py ntru_g [-h] [-p PARAMETERS PARAMETERS PARAMETERS] private_file public_file

positional arguments:
  private_file          Private key Filename
  public_file           Public key Filename

optional arguments:
  -h, --help            show this help message and exit
  -p PARAMETERS PARAMETERS PARAMETERS, --parameters PARAMETERS PARAMETERS PARAMETERS
                        N p q

```

#### Encrypt
```
usage: kry.py ntru_e [-h] public_key message

positional arguments:
  public_key
  message

optional arguments:
  -h, --help  show this help message and exit
```

#### Decrypt
```
usage: kry.py ntru_d [-h] private_key encrypted_message

positional arguments:
  private_key
  encrypted_message

optional arguments:
  -h, --help         show this help message and exit

```

### SPHINX+ usage
#### Sign
```
usage: kry.py sphinx_sign [-h] file

positional arguments:
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```


#### Verify

```
usage: kry.py sphinx_verify [-h] [-k PUBLIC_KEY] [-n SIGNATURE] file

positional arguments:
  file                  Filename

optional arguments:
  -h, --help            show this help message and exit
  -k PUBLIC_KEY, --public_key PUBLIC_KEY
                        File containing public key.
  -n SIGNATURE, --signature SIGNATURE
                        File containing signature.
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