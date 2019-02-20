#! /usr/bin/env bash
#
# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

builder=docker

script="$( basename "$0" )"
cd "$( dirname "$0" )"

TAG="csc-spack-test"

if [ "$script" '=' 'run-csc-image.sh' ] ; then
    com="${builder} run --rm -ti"

    if [ -z "$DISABLE_MOUNT" ] ; then
        DISABLE_MOUNT=1
        if [ -z "$*" ] ; then
            DISABLE_MOUNT=0
        fi
    fi

    if [ "$DISABLE_MOUNT" '==' 0 ] ; then
        com="${com} --net host --privileged -v \"$( readlink -f ../.. ):/appl/opt/spack\" --security-opt label:disable"
    fi

    eval "exec ${com}" "${TAG}" "$@"
elif [ "$script" '=' 'render-csc-image-template.sh' ] ; then
    ./dpp.bash Dockerfile
elif [ "$script" '=' 'push-csc-image.sh' ] ; then
    ${builder} push "${TAG}"
    for tag in ${EXTRA_TAGS} ; do
        ${builder} push "spack/${BASE_NAME}:${tag}"
    done
else
    # tag_options="-t ${TAG}"
    # for tag in ${EXTRA_TAGS} ; do
    #     tag_options="${tag_options} -t spack/${BASE_NAME}:${tag}"
    # done

    # cache_options=""
    # if podman pull "${TAG}" ; then
    #     cache_options="--cache-from ${TAG}"
    # fi

    tag_options="-t csc-spack-test"
    
    exec cat Dockerfile |
         ${builder} build --build-arg RPM_TEST_REPO=${RPM_TEST_REPO} -f - \
                      ${tag_options} \
                      ../..
fi
