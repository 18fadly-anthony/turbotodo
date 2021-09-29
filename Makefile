PREFIX ?= ~/.local

all:
	@echo Run \'make install\' to install to ~/.local/bin

install:
	@mkdir -p $(PREFIX)/bin
	@cp -p main.py $(PREFIX)/bin/todo

uninstall:
	@rm -rf $(PREFIX)/bin/todo
