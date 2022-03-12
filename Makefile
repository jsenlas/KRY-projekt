install:
	pip3 install -r requirements.txt

help:
	python3 kry.py -h 

sign:
	python3 kry.py -c SPHINXPLUS loremipsum.txt

remove_out:
	rm -rf out/*

clear_log:
	rm kry_log.log
	touch kry_log.log
