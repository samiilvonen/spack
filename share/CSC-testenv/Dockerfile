FROM centos:latest
MAINTAINER Spack Maintainers <maintainers@spack.io>

ENV SPACK_ROOT=/opt/spack                     \
    FORCE_UNSAFE_CONFIGURE=1                  \
    container=docker

ADD share/CSC-testenv/RPM-GPG-key /tmp

RUN rpm --import /tmp/RPM-GPG-key \
 && yum-config-manager --add-repo https://object.pouta.csc.fi/swift/v1/AUTH_hpc/HPCCentos7Repo

RUN yum install -y epel-release                               \
 && yum update -y                                             \
 && yum --enablerepo epel groupinstall -y "Development Tools" \
 && yum --enablerepo epel install -y                          \
         curl           findutils gcc-c++    gcc              \
         gcc-gfortran   git       gnupg2     hostname         \
         iproute        make      patch      Lmod             \
         openssh-server python    python-pip tcl              \
         patchelf                                             \
 && rm -rf /var/cache/yum                                     \
 && yum clean all

COPY bin   $SPACK_ROOT/bin
COPY etc   $SPACK_ROOT/etc
COPY lib   $SPACK_ROOT/lib
COPY share $SPACK_ROOT/share
COPY var   $SPACK_ROOT/var
RUN mkdir -p $SPACK_ROOT/opt/spack

RUN rm -rf $SPACK_ROOT/.git                                          \
 && pip install boto3                                                \
 && (  echo ". /usr/share/lmod/lmod/init/bash"                       \
    && echo ". $SPACK_ROOT/share/spack/setup-env.sh"                 \
    && echo ". $SPACK_ROOT/share/spack/spack-completion.bash" )      \
        >> /etc/profile.d/spack.sh                                   \
 && ln -s $SPACK_ROOT/share/CSC-testenv/handle-ssh.sh                \
        /etc/profile.d/handle-ssh.sh                                 \
 && ln -s $SPACK_ROOT/share/CSC-testenv/handle-prompt.sh             \
        /etc/profile.d/handle-prompt.sh                              \
 && mkdir -p /root/.spack                                            \
 && rm -rf /root/*.*

WORKDIR /root
ENTRYPOINT ["bash", "/appl/opt/spack/share/CSC-testenv/entrypoint.bash"]
CMD ["docker-shell"]
