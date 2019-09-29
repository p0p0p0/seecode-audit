DOC_DIR = docs
SRC_DIR = seecode
MAKE = make
PY_VERSION=`python -c "import sys; v = sys.version_info; sys.stdout.write('py%d%d' % (v[0], v[1]))"`
.PHONY: clean html test unit func lint lintall

all:
	make test
	make html
	make clean

install:
	@pip install -r requirements/dev.txt

lint:
	prospector $(SRC_DIR) --strictness veryhigh

test:
	make unit
	make func

unit:
	export PYTHONPATH=$(SRC_DIR) && nosetests -x -v --nocapture \
	--with-coverage --cover-erase --cover-package=$(SRC_DIR) \
	tests/unit/services/test_dispatch.py

func:
	export PYTHONPATH=$(SRC_DIR) && nosetests -x -v --nocapture tests/functional \
	--logging-config tests/functional/log.conf

runserver:
	export SEECODE_CELERY_BROKER_URL=redis://127.0.0.1:6379/2 && \
	export SEECODE_C_FORCE_ROOT=False && \
	export DJANGO_SETTINGS_MODULE=seecode.settings.dev && python manage.py runserver 0.0.0.0:8080
	
db:
	export DJANGO_SETTINGS_MODULE=seecode.settings.dev && python manage.py makemigrations && python manage.py migrate

superuser:
	export DJANGO_SETTINGS_MODULE=seecode.settings.dev && python manage.py createsuperuser

clean:
	rm -rf *.egg-info dist
	find $(SRC_DIR) tests -type f -name '*.pyc' -delete
