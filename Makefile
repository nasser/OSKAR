SRC_FILES = $(shell find src -type f)

.PHONY: windows release debug changelog deliver

.ONESHELL:

all: windows release

windows: target/x86_64-pc-windows-gnu/release/oskar.exe

release: target/release/oskar

debug: target/debug/oskar

target/x86_64-pc-windows-gnu/release/oskar.exe: $(SRC_FILES)
	@echo "cross-compiling windows release build"
	@cargo build --release --target x86_64-pc-windows-gnu

target/release/oskar: $(SRC_FILES)
	@echo "compiling release build"
	@cargo build --release

target/debug/oskar: $(SRC_FILES)
	@echo "compiling debug build"
	@cargo build

deliver: changelog version-bump windows
	@echo "delivering binary"
	tag=`git describe --tags --abbrev=0`
	source="target/x86_64-pc-windows-gnu/release/oskar.exe"
	destination="/home/nasser/Dropbox/Oskar Project/Oskar/System03/$$tag/"
	mkdir -p "$$destination"
	cp "$$source" "$$destination"
	mv changes.txt "$$destination"
	echo "$$source -> $$destination"

version-bump:
	@echo "bumping version"
	new_tag=`git describe --tags --abbrev=0 | awk -F. '{OFS="."; $$NF+=1; printf("%d.%04d\n", $$1, $$2)}'`
	git tag $$new_tag
	echo "bumped to $$new_tag"

changelog:
	@echo "writing changelog"
	echo -n "" > changes.txt
	most_recent_tag=`git describe --abbrev=0 --tags`
	commits=`git rev-list $$most_recent_tag..HEAD`
	for commit in $$commits
	do
	    message=`git log --pretty=format:"- %s (%as, %h)" -n 1 $$commit`
	    if [[ $$message != *chore* ]]; then
	        echo $$message >> changes.txt
	    fi
	done
