

lint:
	black src/geomstats_tools
	isort src/geomstats_tools
	flake8 src/geomstats_tools