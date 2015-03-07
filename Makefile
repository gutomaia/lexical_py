PROJECT_NAME=lexical
PROJECT_TAG=lexical
PYTHON_MODULES=lexical

PYTHON_APP_SOURCES = ${shell find ${PYTHON_MODULES} -type f -iname '*.py' | grep -v ${PYTHON_MODULES}/tests }

WGET=wget -q

default: python.mk github.mk
	@$(MAKE) -C . test

ifeq "true" "${shell test -f python.mk && echo true}"
include python.mk
endif

ifeq "true" "${shell test -f github.mk && echo true}"
include github.mk
endif


python.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/python.mk && touch $@

github.mk:
	@${WGET} https://raw.githubusercontent.com/gutomaia/makery/master/github.mk && touch $@

dependencies: ${REQUIREMENTS}

build: dependencies python_build

test: build ${REQUIREMENTS_TEST}
	${VIRTUALENV} nosetests ${NOSETEST_ARGS} ${PYTHON_MODULES}

tdd: ${REQUIREMENTS_TEST}
	@${eval export IGNORE=${shell ls -d */ | grep -v --regex "^${PYTHON_MODULES}/$$" | xargs echo | sed 's/\///g' | sed 's/ /,/g'}}
	${VIRTUALENV} tdaemon --ignore-dirs="${IGNORE}" --custom-args="--with-notifyplugin --no-start-message --processes=4"

dist: python_egg python_wheel

clean: python_clean
	@rm -rf build dist
	@rm -rf plugins

register:
	${VIRTUALENV} python setup.py register -r pypi

distribute: dist
	${VIRTUALENV} python setup.py sdist bdist_wheel upload -r pypi

purge: clean python_purge
	@rm python.mk

.PHONY: venv dependencies python_dependencies build run dist egg wheel docker clean
