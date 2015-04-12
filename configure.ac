AC_PREREQ([2.63])

# clutter package version number, (as distinct from shared library version)
# An odd micro number indicates in-progress development, (eg. from svn)
# An even micro number indicates a released version.
m4_define(pyclutter_version_major, 1)
m4_define(pyclutter_version_minor, 99)
m4_define(pyclutter_version_micro, 1)
m4_define(pyclutter_version, pyclutter_version_major.pyclutter_version_minor.pyclutter_version_micro)

m4_define(clutter_required_version,     1.0.0)
m4_define(py2cairo_required_version,    1.2.0)
m4_define(py3cairo_required_version,    1.10.0)
m4_define(pygobject_required_version,   3.0.0)
m4_define(python_min_ver,               2.7)
m4_define(python3_min_ver,              3.1)

AC_INIT([pyclutter], [pyclutter_version],
        [],
        [pyclutter],
        [http://www.clutter-project.org])

AC_CONFIG_MACRO_DIR([build/autotools])
AC_CONFIG_HEADERS([config.h])

AM_INIT_AUTOMAKE([1.11 foreign -Wno-portability no-define no-dist-gzip dist-xz tar-ustar subdir-objects])

AM_SILENT_RULES([yes])

AM_MAINTAINER_MODE([enable])

LT_PREREQ([2.2.6])
LT_INIT([dlopen win32-dll disable-static])

dnl put the ACLOCAL flags in the makefile
ACLOCAL="$ACLOCAL $ACLOCAL_FLAGS"

AC_CANONICAL_BUILD
AC_CANONICAL_HOST

# check that we have the minimum version of python necessary to build
JD_PATH_PYTHON(python_min_ver)

# check if we are building for python 3
AM_PYTHON_CHECK_VERSION([$PYTHON], [3.0], build_py3k=true, build_py3k=false)

# if building for python 3 make sure we have the minimum version supported
AS_IF([ test $build_py3k = true ],
      [ AC_MSG_CHECKING([for $PYTHON >=] python3_min_ver) ],
      [
        AM_PYTHON_CHECK_VERSION([$PYTHON], python3_min_ver,
                                [AC_MSG_RESULT(yes)],
                                [AC_MSG_ERROR(too old)])
      ])

PLATFORM=`$PYTHON -c "import sys; from distutils import util; sys.stdout.write(util.get_platform())"`
AC_SUBST(PLATFORM)

PYTHON_BASENAME=`basename $PYTHON`
AC_SUBST([PYTHON_BASENAME])

dnl check for pygobject
PKG_CHECK_MODULES(PYGOBJECT, [pygobject-3.0 >= pygobject_required_version])
AC_SUBST(PYGOBJECT_CFLAGS)
AC_SUBST(PYGOBJECT_LIBS)

dnl check for pycairo
AS_IF([ test $build_py3k = true ],
      [
        PKG_CHECK_MODULES(PYCAIRO, py3cairo >= py3cairo_required_version)
      ],
      [
        PKG_CHECK_MODULES(PYCAIRO, pycairo >= py2cairo_required_version)
      ])

dnl check for clutter
PKG_CHECK_MODULES(CLUTTER, clutter-1.0 >= clutter_required_version)

dnl and set the override directory
AC_ARG_WITH([pygi_overrides_dir],
            [AC_HELP_STRING([--with-pygi-overrides-dir], [Path to pygobject overrides directory])])

AC_MSG_CHECKING(for pygobject overrides directory)
AS_IF([ test "x$with_pygi_overrides_dir" = x ],
      [
        overrides_dir="`$PYTHON -c 'import gi; print(gi._overridesdir)' 2>/dev/null`"
        # fallback if the previous failed
        AS_IF([ test "x$overrides_dir" = x ], [ overrides_dir="${pyexecdir}/gi/overrides" ])
      ],
      [ overrides_dir="$with_pygi_overrides_dir" ])

PYGI_OVERRIDES_DIR="$overrides_dir"
AC_SUBST(PYGI_OVERRIDES_DIR)
AC_MSG_RESULT($PYGI_OVERRIDES_DIR)

AC_CONFIG_FILES([
    Makefile
    build/Makefile
    build/autotools/Makefile
    gi/Makefile
    gi/overrides/Makefile
    examples/Makefile
])

AC_OUTPUT

AC_MSG_RESULT([
        pyclutter $VERSION

        Python: $PYTHON
        Building with Python 3: $build_py3k
        PyGObject overrides directory: $overrides_dir
])
