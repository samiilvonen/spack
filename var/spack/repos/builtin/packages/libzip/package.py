# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libzip(CMakePackage):
    """libzip is a C library for reading, creating,
    and modifying zip archives."""

    homepage = "https://nih.at/libzip/index.html"
    url      = "https://github.com/nih-at/libzip/archive/refs/tags/v1.10.1.tar.gz"

    version('1.10.1', sha256='d56d857d1c3ad4a7f3a4c01a51c6a6e5530e35ab93503f62276e8ba2b306186a')
    # version('1.2.0', sha256='6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f')

    depends_on('zlib@1.1.2:')

    @property
    def headers(self):
        # Up to version 1.3.0 zipconf.h was installed outside of self.prefix.include
        return find_all_headers(
            self.prefix if self.spec.satisfies("@:1.3.0") else self.prefix.include
        )
