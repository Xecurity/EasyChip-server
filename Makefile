.PHONY: default
default:
	dev_appserver.py --address=0.0.0.0 .

.PHONY: clean
clean:
	rm -f *.pyc
