# KRY-project

We will encipher/decipher or sign a file by a post quantum algorithm. 

## Development

For making it easier for development we created a simple Makefile that let's you do first setup, installation, cleanup and meassuring quality of code.

### Setup

```text
python3 -m venv env            # create virtual environment - run only once
source ./env/bin/activate      # go to virtual environment
pip3 install -r requirements.txt  # install python libraries
```

Make sure that you have updated ```pip``` to the latest version. PySPX requires you to install ```openssl```. E.g. ```sudo apt -y install libssl-dev```.



### Example run

Sign a file using SPHINX+.

```text
make sign
```


### Cleanup

```text
make remove_out  # removes all files in ./out directory
make clear_log  # clears content from logfile kry_log.log
```

### Quality

To measure quality of code we use pylint code checker.

```text
make pylint
```
We try to stay as high as possible :) 

- 10/10 is the goal. 
- 8/10 at least please :D


**This checks every python file and prints out collective score I *SUGGEST* to run** ```pylint yourfile.py``` **for you to know score of your file and keep it above 8.0**

### Display documentation

To display documentation you can run it localy and see in your browser using ```make documentation``` or just simply access it on our [Github Pages](https://jsenlas.github.io/KRY-projekt/)

For publishing local changes to the repo run ```make gh_publish```. You will need ssh access to the repo to do this. Changes are applied pretty fast.