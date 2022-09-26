# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.util.environment import EnvironmentModifications


@IntelOneApiPackage.update_description
class IntelOneapiCompilersClassic(IntelOneApiPackage):
    """Relies on intel-oneapi-compilers to install the compilers, and
    configures modules for icc/icpc/ifort.

    """

    maintainers = ["rscohn2"]

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    has_code = False

    phases = []

    for ver, cver in [["2022.1.0", "2021.6.0"]]:
        version(cver)
        depends_on("intel-oneapi-compilers@" + ver, when="@" + cver, type="run")

    @property
    def component_dir(self):
        return "compiler"

    @property
    def component_prefix(self):
        parent = self.spec["intel-oneapi-compilers"]
        return parent.prefix.join(join_path(self.component_dir, parent.version))

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh

        and from setting CC/CXX/F77/FC
        """
        env.extend(
            EnvironmentModifications.from_sourcing_file(
                join_path(self.component_prefix, "env", "vars.sh")
            )
        )

        bin = join_path(
            self.spec["intel-oneapi-compilers"].prefix,
            "compiler",
            self.version,
            "linux",
            "bin",
            "intel64",
        )
        env.set("CC", join_path(bin, "icc"))
        env.set("CXX", join_path(bin, "icpc"))
        env.set("F77", join_path(bin, "ifort"))
        env.set("FC", join_path(bin, "ifort"))
