#!/bin/bash
# Fomenko A V  2025 (c)

# ========== BUILD DEB ==========
mkdir -pv deb/ms55dd/{DEBIAN/,opt/MS55DD/,usr/bin/,usr/share/applications}

cp -vf *.py MS55DD upgradeMS55DD MS55DD.png deb/ms55dd/opt/MS55DD
chmod +x deb/ms55dd/opt/MS55DD/MS55DD

cp -vf ms55dd deb/ms55dd/usr/bin
chmod +x deb/ms55dd/usr/bin/ms55dd

cp -vf ms55dd.desktop deb/ms55dd/usr/share/applications

echo "Previous version $(ls *.deb | grep -o '[0-9]*.[0-9]*-[0-9]*.[0-9]*')"
read -p "Enter Version (x.x-x.x): " VERSION

rm -rfv *.deb

CONTROL_FILE="Package: MS55DD
Version: $VERSION
Section: system
Architecture: all
Priority: optional
Depends: python3, python3-pyqt5 (>= 5.12.2), python3-sh, util-linux, coreutils
Maintainer: Alex <alexfomg@gmail.com>
Description: Upgrade Surdial 55 and Malahit machine
Installed-Size: $(du -sb deb/ms55dd | grep -o '^[0-9]*')" 

echo "$CONTROL_FILE" > deb/ms55dd/DEBIAN/control 

cd deb/

fakeroot dpkg-deb --build ms55dd .

mv *.deb ..

cd ..

rm -rf deb
# ========== END BUILD DEB ==========

# ========== BUILD FOR REST DISTRO ==========
mkdir -pv ms55dd_INSTALL/MS55DD

cp -vf *.py MS55DD upgradeMS55DD MS55DD.png ms55dd_INSTALL/MS55DD
chmod +x ms55dd_INSTALL/MS55DD/MS55DD

sed -i 's/\/usr\/bin\/python3/\/opt\/MS55DD\/venv_ms55dd\/bin\/python/' ms55dd_INSTALL/MS55DD/*.py
sed -i 's/\/usr\/bin\/python3/\/opt\/MS55DD\/venv_ms55dd\/bin\/python/' ms55dd_INSTALL/MS55DD/MS55DD

cp -vf install.sh ms55dd ms55dd.desktop ms55dd_INSTALL/

sed -i 's/exec .\/upgradeMS55DD/exec \/opt\/MS55DD\/upgradeMS55DD/' ms55dd_INSTALL/ms55dd
sed -i 's/exec .\/MS55DD/exec \/opt\/MS55DD\/MS55DD/' ms55dd_INSTALL/ms55dd

chmod +x ms55dd_INSTALL/ms55dd

tar -cvJf ms55dd_${VERSION}_all.tar.xz ms55dd_INSTALL/

rm -rvf ms55dd_INSTALL/
# ========== END BUILD FOR REST DISTRO ==========
