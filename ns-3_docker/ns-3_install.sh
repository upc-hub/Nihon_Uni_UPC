#!/bin/bash

#Ubuntu
sudo apt-get install -y g++ python3
sudo apt-get install -y g++ python3 cmake
sudo apt-get install -y g++ python3 python3-dev pkg-config sqlite3 cmake
sudo apt-get install -y qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools
sudo apt-get install -y qt5-default
sudo apt-get install -y gir1.2-goocanvas-2.0 python3-gi python3-gi-cairo python3-pygraphviz gir1.2-gtk-3.0 ipython3
sudo apt-get install -y python-pygraphviz python-kiwi python-pygoocanvas libgoocanvas-dev ipython
sudo apt-get install -y autoconf cvs bzr unrar #bike build tool
sudo apt-get install -y gdb valgrind
sudo apt-get install -y uncrustify
sudo apt-get install -y doxygen graphviz imagemagick
sudo apt-get install -y texlive texlive-extra-utils texlive-latex-extra texlive-font-utils dvipng latexmk
sudo apt-get install -y python3-sphinx dia #ns-3 manual and tutorial
sudo apt-get install -y tcpdump
sudo apt-get install -y sqlite sqlite3 libsqlite3-dev
sudo apt-get install -y libxml2 libxml2-dev
sudo apt-get install -y cmake libc6-dev libc6-dev-i386 libclang-dev llvm-dev automake python3-pip
python3 -m pip install --user cxxfilt
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y vtun lxc uml-utilities
sudo apt-get install -y libxml2 libxml2-dev libboost-all-dev

#Manual installation
sudo apt-get install -y git
rm -r /root/repos
cd
mkdir repos

cd repos
git clone https://gitlab.com/nsnam/ns-3-allinone.git

cd ns-3-allinone
./download.py -n ns-3.30

cd ns-3.30
./build.py

CXXFLAGS="-O3" ./waf configure #コンパイルに使用されるフラグを変更

#test
#./test.py
./waf --run scratch/scratch-simulator

echo "ns-3 install done"

cp /tmp/gunji_olsr-randam.cc /root/repos/ns-3-allinone/ns-3.30/scratch/

rm -r /root/repos/ns-3-allinone/ns-3.30/src/olsr/*

cp -r /tmp/olsr/* /root/repos/ns-3-allinone/ns-3.30/src/olsr/

echo "****Successful****"
