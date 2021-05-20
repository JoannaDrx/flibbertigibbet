.PHONY: clean clean-build clean-pyc update-lambda release

clean: clean-build clean-pyc  ## remove all artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove python3 file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

dist: clean ## builds source
	mkdir lambda-function
	cp -r httplib2/ lambda-function/httplib2/
	cp flibbertigibbet/flibbertigibbet.py lambda-function/
	zip -j lambda-function.zip lambda-function/

update-lambda: ## publish the updated lambda pkg
	aws lambda update-function-code --function-name arn:aws:lambda:$(AWS_REGION):$(AWS_ACCOUNT_ID):function:flibbertigibbet --publish --zip-file  fileb://lambda-function.zip

release: dist update-lambda
	echo Succesfully updated lambda function Flibbertigibbet in AWS account $(AWS_ACCOUNT_ID)