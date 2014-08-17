ALBUM=bootstrap/run.py

all: build/album.py build/album build/album/__init__.py build/album/compiler.py build/album/errors.py

build/album.py: src/album.md
	$(ALBUM) build src/album.md build/album.py 
	chmod u+x build/album.py

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
