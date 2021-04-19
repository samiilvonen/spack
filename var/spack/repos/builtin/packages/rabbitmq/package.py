# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rabbitmq(Package):
    """
    RabbitMQ is lightweight and easy to deploy on premises and in the cloud.
    It supports multiple messaging protocols. RabbitMQ can be deployed in
    distributed and federated configurations to meet high-scale,
    high-availability requirements.
    """

    homepage = "http://www.rabbitmq.com/"

    version('3.8.14', sha256='c9b154ea42bb0cfd1caef4869cfae3ed0fc3579794dd08bd555057af5736c06e')
    version('3.6.15', sha256='04e6a291642f80e87fc892d5e8ea309fb3fab85ebb64a79a70dfe6c6cfde36fb')

    def url_for_version(self, version):
        url = "https://github.com/rabbitmq/rabbitmq-server/releases/download/v{0}/rabbitmq-server-generic-unix-{0}.tar.xz"
        return url.format(version)

    def install(self, spec, prefix):
        install_tree('.', prefix)
