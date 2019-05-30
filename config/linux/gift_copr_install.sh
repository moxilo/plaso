#!/usr/bin/env bash
#
# This file is generated by l2tdevtools update-dependencies.py any dependency
# related changes should be made in dependencies.ini.

# Exit on error.
set -e

# Dependencies for running plaso, alphabetized, one per line.
# This should not include packages only required for testing or development.
PYTHON2_DEPENDENCIES="libbde-python2
                      libesedb-python2
                      libevt-python2
                      libevtx-python2
                      libewf-python2
                      libfsapfs-python2
                      libfsntfs-python2
                      libfvde-python2
                      libfwnt-python2
                      libfwsi-python2
                      liblnk-python2
                      libmsiecf-python2
                      libolecf-python2
                      libqcow-python2
                      libregf-python2
                      libscca-python2
                      libsigscan-python2
                      libsmdev-python2
                      libsmraw-python2
                      libvhdi-python2
                      libvmdk-python2
                      libvshadow-python2
                      libvslvm-python2
                      python2-XlsxWriter
                      python2-artifacts
                      python2-backports-lzma
                      python2-bencode
                      python2-biplist
                      python2-certifi
                      python2-chardet
                      python2-crypto
                      python2-dateutil
                      python2-dfdatetime
                      python2-dfvfs
                      python2-dfwinreg
                      python2-dtfabric
                      python2-elasticsearch
                      python2-future
                      python2-idna
                      python2-lz4
                      python2-pefile
                      python2-psutil
                      python2-pyparsing
                      python2-pysqlite
                      python2-pytsk3
                      python2-pytz
                      python2-pyyaml
                      python2-requests
                      python2-six
                      python2-urllib3
                      python2-yara
                      python2-zmq";

# Additional dependencies for running tests, alphabetized, one per line.
TEST_DEPENDENCIES="python2-funcsigs
                   python2-mock
                   python2-pbr
                   python2-setuptools";

# Additional dependencies for development, alphabetized, one per line.
DEVELOPMENT_DEPENDENCIES="pylint
                          python-sphinx";

# Additional dependencies for debugging, alphabetized, one per line.
DEBUG_DEPENDENCIES="libbde-debuginfo
                    libbde-python2-debuginfo
                    libesedb-debuginfo
                    libesedb-python2-debuginfo
                    libevt-debuginfo
                    libevt-python2-debuginfo
                    libevtx-debuginfo
                    libevtx-python2-debuginfo
                    libewf-debuginfo
                    libewf-python2-debuginfo
                    libfsapfs-debuginfo
                    libfsapfs-python2-debuginfo
                    libfsntfs-debuginfo
                    libfsntfs-python2-debuginfo
                    libfvde-debuginfo
                    libfvde-python2-debuginfo
                    libfwnt-debuginfo
                    libfwnt-python2-debuginfo
                    libfwsi-debuginfo
                    libfwsi-python2-debuginfo
                    liblnk-debuginfo
                    liblnk-python2-debuginfo
                    libmsiecf-debuginfo
                    libmsiecf-python2-debuginfo
                    libolecf-debuginfo
                    libolecf-python2-debuginfo
                    libqcow-debuginfo
                    libqcow-python2-debuginfo
                    libregf-debuginfo
                    libregf-python2-debuginfo
                    libscca-debuginfo
                    libscca-python2-debuginfo
                    libsigscan-debuginfo
                    libsigscan-python2-debuginfo
                    libsmdev-debuginfo
                    libsmdev-python2-debuginfo
                    libsmraw-debuginfo
                    libsmraw-python2-debuginfo
                    libvhdi-debuginfo
                    libvhdi-python2-debuginfo
                    libvmdk-debuginfo
                    libvmdk-python2-debuginfo
                    libvshadow-debuginfo
                    libvshadow-python2-debuginfo
                    libvslvm-debuginfo
                    libvslvm-python2-debuginfo
                    python-guppy";

sudo dnf install dnf-plugins-core
sudo dnf copr -y enable @gift/dev
sudo dnf install -y ${PYTHON2_DEPENDENCIES}

if [[ "$*" =~ "include-debug" ]]; then
    sudo dnf install -y ${DEBUG_DEPENDENCIES}
fi

if [[ "$*" =~ "include-development" ]]; then
    sudo dnf install -y ${DEVELOPMENT_DEPENDENCIES}
fi

if [[ "$*" =~ "include-test" ]]; then
    sudo dnf install -y ${TEST_DEPENDENCIES}
fi
