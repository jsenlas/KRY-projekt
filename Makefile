env:
	@echo "CREATING VIRTUAL ENVIRONMENT..."
	python3 -m venv env
	source ./env/bin/activate

install:
	@echo "INSTALLING REQUIREMENTS..."
	pip3 install -r requirements.txt

help:
	python3 kry.py -h 

sign_code_based:
	@echo "Example of signing a file using SPHINX+ algorithm."
	python3 kry.py --onedir code_sign loremipsum.txt

	
sign_sphinx:
	@echo "Example of signing a file using SPHINX+ algorithm."
	python3 kry.py --onedir sphinx_sign loremipsum.txt

test_sphinx:
	@echo "TEST START"
	@echo "In this test we sign a document, change and verify it successfully, then we changed the file and verified again with unsuccessfull result."
	@echo "@@@@@@ Signing @@@@@@"
	python3 kry.py --onedir sphinx_sign loremipsum.txt
	@echo "@@@@@@ Verification should SUCCEED: @@@@@@"
	python3 kry.py --onedir sphinx_verify -s out/loremipsum.txt.signature -k out/loremipsum.txt.pbkey loremipsum.txt 
	@echo "Modifying original file"
	@echo "loremipsum" >> loremipsum.txt
	@echo "@@@@@@ Verification should FAIL: @@@@@@"
	python3 kry.py --onedir sphinx_verify -s out/loremipsum.txt.signature -k out/loremipsum.txt.pbkey loremipsum.txt 
	make loremipsum

remove_out:
	rm -rf out/*

clear_log:
	rm kry_log.log
	touch kry_log.log

pylint:
	pylint kry.py ./src

loremipsum:
	@echo "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum." > loremipsum.txt

documentation:
	mkdocs serve

gh_publish:
	mkdocs gh-deploy
