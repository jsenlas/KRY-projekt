# KRY-projekt

We will send the *loremimsum.txt* to the recepient cyphered by post quantum algorithm. 

```python
python3 kry.py [-c|-d] -a NAME|NUMBER -s NAME|NUMBER -f filename

usage: kry.py [-h] [-c] [-d] [-a ALGORITHM] [-s SIGN] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -c, --cypher          cypher
  -d, --decypher        decypher
  -a ALGORITHM, --algorithm ALGORITHM
                        algorithm
  -s SIGN, --sign SIGN  signing
  -f FILE, --file FILE  Filename

```
Output of the program is cyphered/decyphered file
filename.cypher

e.g. loremimsum.txt.cypher
