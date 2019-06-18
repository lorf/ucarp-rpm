#!/bin/bash

CWD=$(pwd)
VERSION="1.5.2"
SPEC="files/ucarp.spec"
#SOURCE_URL="https://github.com/jedisct1/UCarp.git"
SOURCE_URL="https://github.com/lorf/UCarp.git"

echo "Creating RPM build path structure..."
mkdir -p rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS,tmp}

cp "$SPEC" rpmbuild/SPECS/
cp files/* rpmbuild/SOURCES/

echo "Downloading sources..."
cd rpmbuild/SOURCES
rm -rf ucarp-${VERSION}
git clone "$SOURCE_URL" ucarp-${VERSION}

rm -f "ucarp-$VERSION.tar.bz2" >/dev/null 2>&1 || true
echo "Tarring source tree..."
tar cjf "ucarp-$VERSION.tar.bz2" ucarp-${VERSION}

gitrev=`git log -1 --format=%h`
if [ -f ${CWD}/gpg-env ]; then
  echo "Building RPM with GPG signing..."
  cd ${CWD}

  source gpg-env
  if [ "${gpg_bin}" != "" ]; then
    rpmbuild --define "_topdir ${CWD}/rpmbuild" \
      --define "_signature ${signature}" \
      --define "_gpg_path ${gpg_path}" --define "_gpg_name ${gpg_name}" \
      --define "__gpg ${gpg_bin}" --define "dist git$gitrev" \
      --sign -bb ${SPEC}
  else
    rpmbuild --define "_topdir ${CWD}/rpmbuild" \
      --define "_signature ${signature}" \
      --define "_gpg_path ${gpg_path}" --define "_gpg_name ${gpg_name}" \
      --define "dist git$gitrev" --sign -bb ${SPEC}
  fi
else
  echo "Building RPM..."
  cd ${CWD}
  rpmbuild --define "_topdir ${CWD}/rpmbuild" \
      --define "dist git$gitrev" -bb ${SPEC}
fi

