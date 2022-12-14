run:
	docker-compose up -d

deps:
	python3 -m spacy download en

clean:
	rm -f *~
	rm -f .*~
	rm -f \#*
	rm -f .\#*
	find -iname "__pycache__" | xargs rm -rf

nuke:
	rm -rf ./conf
	rm -rf ./data
	rm -rf ./import
	rm -rf ./logs
	rm -rf ./plugins
	rm -rf ./files