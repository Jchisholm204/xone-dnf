#!/usr/bin/env zsh

export REPO_ROOT=$(git rev-parse --show-toplevel)

function setup_build_root() {
	# Setup the RPM root build directory
	local BUILDROOT_DIRS=("BUILD" "BUILDROOT" "RPMS" "SOURCES" "SPECS" "SRPMS")
	local BUILDROOT="$REPO_ROOT/rpm/build"

	if [[ ! -d "$BUILDROOT" ]]; then
		echo "Setting up build folder ./$BUILDROOT"
		mkdir $BUILDROOT
	fi

	for DIR in $BUILDROOT_DIRS; do
		if [[ ! -d "$BUILDROOT/$DIR" ]]; then
			echo "Creating Build Directory $BUILDROOT/$DIR"
			mkdir "$BUILDROOT/$DIR"
		fi
	done
	echo "Finished setting up RPM source directory"
}

function setup_sources() {
	local XONE_VERSION=$1
	tar --exclude="./rpm" \
		--transform "s|^|xone-${XONE_VERSION}/|" \
		-czf "${REPO_ROOT}/rpm/build/SOURCES/xone-${XONE_VERSION}.tar.gz" \
		-C "$REPO_ROOT" .
}

function build_rpm() {
	rpmbuild -bb --noclean "${REPO_ROOT}/rpm/xone.spec" \
		--define "_topdir ${REPO_ROOT}/rpm/build"
}

setup_build_root
setup_sources '0.5.8'
build_rpm
