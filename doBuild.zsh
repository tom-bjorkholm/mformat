#! /bin/zsh
#
# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License
#
PKG1='mformat'
PKG2='mformat_ext'
set -eE
trap 'printf "\e[31m%s: %s\e[m\n" "Exiting due to error code from command" $?' ERR
pytestflag=""
set -v
if [ ${#} -gt 0 ]; then
    PYTHON=${1}
    if echo ${PYTHON} | grep -v 'python' > /dev/null
    then
        echo ${PYTHON} 'does not look like a python version'
        exit 1
    fi
    if which ${PYTHON} > /dev/null
    then
        echo 'Using PYTHON' ${PYTHON} 
    else
        echo 'Cannot find executable for' ${PYTHON}
        exit 1
    fi
fi
if [[ ! -v PYTHON ]]; then
    PYTHON=`./bestInstalledPython.zsh`
fi
echo 'Using PYTHON' ${PYTHON} 
VENVOKMARK=(./venv/lib/python*/site-packages(NnOn))
DOCOUTDIR=reports
DOCINDEX=${DOCOUTDIR}/index.html
TSUMFILE=${DOCOUTDIR}/test_summary.md
FLAKEOUTDIR=${DOCOUTDIR}/flake_report
MYPYOUTDIR=${DOCOUTDIR}/mypy_report
MYPYOUTFILE=${DOCOUTDIR}/mypy_errors.txt
VER=`grep version < base/setup.py  | sed 'sX.*=.XXg' | sed 'sX.,$XXg'`
BUILDLOG=${DOCOUTDIR}/build_log.txt
PYTESTLOG=${DOCOUTDIR}/pytest_log.txt
if (($#VENVOKMARK == 0)) ; then
  echo "No venv: ${VENVOKMARK}"
  ./setup_build_environment.zsh
fi
. ./venv/bin/activate
rm -rf build dist base/build base/dist extend/build extend/dist
rm -rf ${DOCOUTDIR}
mkdir -p dist
(cd base; ln -sf ../dist dist)
(cd extend; ln -sf ../dist dist)
mkdir -p ${DOCOUTDIR}
mkdir -p ${MYPYOUTDIR}
mkdir -p ${FLAKEOUTDIR}
date +'Build started %Y-%m-%d %H:%M:%S %Z' > ${BUILDLOG}
for dd in base/src base/test extend/src extend/test ; do
  find ${dd} -name __pychache__ -exec rm -rf {} \;
done
${PYTHON} -m build base | tee -a ${BUILDLOG}
WHLBASE1=`echo ${PKG1} | sed 's/_/-/g'`
export WHL1=`ls dist/${PKG1}-*.whl | sed 'sXdist/XXg'`
if [[ ! -a dist/${WHL1} ]] ; then
  echo "Build of wheel ${WHL1} failed." >& 2
  exit 1
fi
WHLBASE2=`echo ${PKG2} | sed 's/_/-/g'`
${PYTHON} -m pip uninstall -y ${WHLBASE1} ${WHLBASE2} 2>&1 | tee -a ${BUILDLOG}
${PYTHON} -m pip install dist/${WHL1} 2>&1 | tee -a ${BUILDLOG}
${PYTHON} -m build extend | tee -a ${BUILDLOG}
export WHL2=`ls dist/${PKG2}-*.whl | sed 'sXdist/XXg'`
if [[ ! -a dist/${WHL2} ]] ; then
  echo "Build of wheel ${WHL2} failed." >& 2
  exit 1
fi
${PYTHON} -m pip uninstall -y ${WHLBASE2} 2>&1 | tee -a ${BUILDLOG}
${PYTHON} -m pip install dist/${WHL2} 2>&1 | tee -a ${BUILDLOG}
date +'Build ready %Y-%m-%d %H:%M:%S %Z' 2>&1 | tee -a ${BUILDLOG}
for i in 1 2 3 4 5 ; do
  echo " "
done
rm -rf ${FLAKEOUTDIR}
mkdir -p ${FLAKEOUTDIR}
set +eE
${PYTHON} -m pylint example/src/*.py example/test/*.py 2>&1 | tee ${PYTESTLOG}
${PYTHON} -m mypy example/src --strict --html-report ${MYPYOUTDIR} 2>&1 | tee ${MYPYOUTFILE}
${PYTHON} -m flake8 --format=html --htmldir=${FLAKEOUTDIR} base/src base/test extend/src extend/test example/src 2>&1 | tee ${FLAKEOUTFILE}
${PYTHON} -m mypy base/src extend/src --strict --html-report ${MYPYOUTDIR} 2>&1 | tee ${MYPYOUTFILE}
set -eE
pytest --pylint ${pytestflag} --pylint-jobs=16 --html=${DOCOUTDIR}/pytest_report.html --cov=${PKG1} --cov=${PKG2} --cov-report=html:${DOCOUTDIR}/coverage 2>&1 | tee ${PYTESTLOG}
testStatus=$?
set +v
rm -rf example/result || true 2>&1 | tee -a ${BUILDLOG}
mkdir -p example/result 2>&1 | tee -a ${BUILDLOG}
(cd example/src; ls *.py | while read file; do ${PYTHON} ${file} -f all -o ../result/${file%.py}; done) 2>&1 | tee -a ${BUILDLOG}
cat > ${DOCINDEX} <<EOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>${PKG} report</title>
</head>
<body>
EOF
date +"<h1>${WHLBASE1} and ${WHLBASE2} ${VER} test report %Y-%m-%d %H:%M </h1> " >> ${DOCINDEX}
echo "<h2>Building version ${VER}</h2>" >> ${DOCINDEX}
echo '## Test summary' > ${TSUMFILE}
echo '' >> ${TSUMFILE}
TRES=`grep 'passed' < ${PYTESTLOG} | tail -1 | sed 's/=//g' | sed 's/^ //g' | sed 's/.[0-9][0-9]s/s/g' | sed 's/ $//g'`
echo ${TRES} >> ${DOCINDEX}
echo '* Test result:' ${TRES} >> ${TSUMFILE}
skipped=`grep 'passed' < ${PYTESTLOG} | tail -1 | grep skipped | wc -l`
failed=`grep 'passed' < ${PYTESTLOG} | tail -1 | grep failed | wc -l`
if [[ ${failed} -ne 0 ]] ; then
  echo "Pytest/pylint errors" >&2
  testStatus=1
fi
if ! grep 'No flake8 errors found' ${FLAKEOUTDIR}/index.html > /dev/null
then
  echo "Flake8 errors/warnings." >&2
  echo "* Flake8 errors/warnings." >> ${TSUMFILE}
  echo "<br>Flake8 errors/warnings<br>" >> ${DOCINDEX}
  testStatus=1
else 
  echo "* No Flake8 warnings." >> ${TSUMFILE}
fi
if grep 'Success: no issues found' < ${MYPYOUTFILE} >/dev/null
then
  echo "No mypy errors found." >&2
  echo "* No mypy errors found." >> ${TSUMFILE}
  echo "<br>No mypy issues found<br>" >> ${DOCINDEX}
else
  echo "mypy errors" >&2
  echo "* mypy errors" >> ${TSUMFILE}
  echo "<br>mypy errors<br>" >> ${DOCINDEX}
  testStatus=1
fi
echo "Build and test using python version:" `${PYTHON} --version` >> ${DOCINDEX}
echo "* ${VER} built and tested using python version:" `${PYTHON} --version` >> ${TSUMFILE}
cat >> ${DOCINDEX} <<EOF
<ul>
<li><a href="pytest_report.html?visible=failed,error,xfailed,xpassed,rerun">pytest report</a></li>
<li><a href="coverage/index.html">coverage report</a></li>
<li><a href="flake_report/index.html">flake8 report</a></li>
<li><a href="mypy_report/index.html">mypy report</a></li>
<li><a href="mypy_errors.txt">mypy errors</a></li>
<li><a href="build_log.txt">build log</a></li>
<li><a href="pytest_log.txt">pytest log</a></li>
</ul>
</body>
</html>
EOF
echo "Build and test using python version:" `${PYTHON} --version`
if [[ ${skipped} -eq 0 ]] ; then
  for i in README.md base/README_pypi.md extend/README_pypi.md ; do
    sed -n '/## Test summary/q;p' < ${i} > ${i}.new
    cat ${i}.new ${TSUMFILE} > ${i}
    rm ${i}.new
  done
fi
exit $testStatus
