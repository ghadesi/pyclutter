test_files = \
	test_overrides_Color.py

TESTS_ENVIRONMENT = \
	PYTHONPATH=$(PYGI_OVERRIDES_DIR):$(top_builddir):$(top_builddir)/tests:$${PYTHONPATH:+:$$PYTHONPATH} \
	MALLOC_PERTURB_=85 \
	MALLOC_CHECK_=3 \
	G_SLICE=debug-blocks \
	TESTS_BUILDDIR=$(builddir)

check_SCRIPTS = run-tests.py

EXTRA_DIST = run-tests.py $(test_files)
