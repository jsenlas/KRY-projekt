## General commands

For each of our algorithms we use different commands in format *algoritm*_*action* as can be seen bellow.

```text
usage: kry.py [-h] [--log] [--onedir] {ntru_g,ntru_e,ntru_d,sphinx_sign,sphinx_verify} ...

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
  --onedir              Save signature and public key in directory. This option will overwrite existing files.

KRY 2022 project - cipher/decipher or sign a file.

```

## NTRU usage

### Generate
```text
usage: kry.py ntru_g [-h] [-p PARAMETERS PARAMETERS PARAMETERS] private_file public_file

positional arguments:
  private_file          Private key Filename
  public_file           Public key Filename

optional arguments:
  -h, --help            show this help message and exit
  -p PARAMETERS PARAMETERS PARAMETERS, --parameters PARAMETERS PARAMETERS PARAMETERS
                        N p q

```

### Encrypt
```text
usage: kry.py ntru_e [-h] public_key message

positional arguments:
  public_key
  message

optional arguments:
  -h, --help  show this help message and exit
```

### Decrypt
```text
usage: kry.py ntru_d [-h] private_key encrypted_message

positional arguments:
  private_key
  encrypted_message

optional arguments:
  -h, --help         show this help message and exit

```

## SPHINX+ usage
### Sign
```text
usage: kry.py sphinx_sign [-h] file

positional arguments:
  file        Filename

optional arguments:
  -h, --help  show this help message and exit
```


### Verify

```text
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

You can run this test by running ```make test_sphinx```. It will sign the file and then verify it. To show the functionality we change the original file and try to run verification again with (ecpected) unsuccessful result.

Signing a file.
```text
python3 kry.py --onedir sphinx_sign loremipsum.txt
```

And verifying signature.
```text
python3 kry.py --onedir sphinx_verify -s out/loremipsum.txt.signature -k out/loremipsum.txt.pbkey loremipsum.txt 
```
