run:
	@[ -d ./conf ] || mkdir conf
	@[ -d ./data ] || mkdir data
	@[ -d ./import ] || mkdir import
	@[ -d ./logs ] || mkdir logs
	@[ -d ./plugins ] || mkdir plugins
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
