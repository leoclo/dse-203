run:
	docker-compose up -d

clean:
	rm -f *~
	rm -f .*~
	rm -f \#*
	rm -f .\#*

nuke:
	rm -rf ./conf
	rm -rf ./data
	rm -rf ./import
	rm -rf ./logs
	rm -rf ./plugins
	rm -rf ./files