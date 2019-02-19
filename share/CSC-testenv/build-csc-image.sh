#! /usr/bin/env bash
#
# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

script="$( basename "$0" )"
cd "$( dirname "$0" )"

TAG="csc-spack-test"

if [ "$script" '=' 'run-csc-image.sh' ] ; then
    com="podman run --rm -ti"

    if [ -z "$DISABLE_MOUNT" ] ; then
        DISABLE_MOUNT=1
        if [ -z "$*" ] ; then
            DISABLE_MOUNT=0
        fi
    fi

    if [ "$DISABLE_MOUNT" '==' 0 ] ; then
        com="${com} --privileged --net=host -v \"$( readlink -f ../.. ):/appl/opt/spack\""
    fi

    eval "exec ${com}" "${TAG}" "$@"
elif [ "$script" '=' 'render-csc-image-template.sh' ] ; then
    ./dpp.bash Dockerfile
elif [ "$script" '=' 'push-csc-image.sh' ] ; then
    podman push "${TAG}"
    for tag in ${EXTRA_TAGS} ; do
        podman push "spack/${BASE_NAME}:${tag}"
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
         podman build -f -           \
                      ${tag_options} \
                      ../..
fi
