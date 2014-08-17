ALBUM=bootstrap/run.py

all: build/run.py build/album build/album/__init__.py build/album/compiler.py build/album/errors.py

build/run.py: src/run.md
	$(ALBUM) build src/run.md build/run.py 
	chmod u+x build/run.py

build/album:
	mkdir build/album || true

build/album/__init__.py: src/album/__init__.md
	$(ALBUM) build $^ $@

build/album/compiler.py: src/album/compiler.md
	$(ALBUM) build $^ $@

build/album/errors.py: src/album/errors.md
	$(ALBUM) build $^ $@

clean:
	rm -fr build/*
