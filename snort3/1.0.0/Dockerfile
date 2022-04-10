# Base our app image off of the WALKOFF App SDK image
FROM frikky/shuffle:app_sdk as base

FROM base

# Install all alpine build tools needed for our pip installs
RUN echo 'https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories && \
  apk add --no-cache --update \
    libffi \
    abuild \
    build-base \
    cmake \
    flex \
    linux-headers \
    # Library
    libffi-dev \
    musl-dev \
    libunwind-dev \
    libpcap-dev \
    libdnet-dev \
    hwloc-dev \
    luajit-dev \
    openssl-dev \
    pcre-dev \
    libtirpc-dev \
    flatbuffers-dev \
    vectorscan-dev \
    flex-dev

ENV SRC_HOME=/snort_src
WORKDIR ${SRC_HOME}

ARG SAFEC_VER=02092020
ADD https://github.com/rurban/safeclib/releases/download/v${SAFEC_VER}/libsafec-${SAFEC_VER}.tar.gz ${SRC_HOME}/libsafec-${SAFEC_VER}.tar
ARG GPERF_VER=2.9.1
ADD  https://github.com/gperftools/gperftools/releases/download/gperftools-${GPERF_VER}/gperftools-${GPERF_VER}.tar.gz ${SRC_HOME}/gperftools-${GPERF_VER}.tar
ARG DAQ_VER=3.0.2
ADD https://github.com/snort3/libdaq/releases/download/v${DAQ_VER}/libdaq-${DAQ_VER}.tar.gz $SRC_HOME/libdaq-${DAQ_VER}.tar
ARG SNORT_VER=3.1.3.0
ADD https://github.com/snort3/snort3/archive/${SNORT_VER}.tar.gz ${SRC_HOME}/snort3-${SNORT_VER}.tar

RUN echo "Build libsafec" && \
  tar -xzvf libsafec-${SAFEC_VER}.tar && \
  cd libsafec-${SAFEC_VER}.0-g6d921f && \
  ./configure && \
  make -j 4 && \
  make install && \
  echo "Build gperftools" && \
  cd ${SRC_HOME} && \
  tar -xvf gperftools-$GPERF_VER.tar && \
  cd ${SRC_HOME}/gperftools-$GPERF_VER && \
  ./configure && \
  make -j 4 && \
  make install && \
  echo "Build libdaq" && \
  cd ${SRC_HOME} && \
  tar xvf libdaq-${DAQ_VER}.tar && \
  cd ${SRC_HOME}/libdaq-${DAQ_VER} && \
  ./configure && \
  make -j 4 && \
  make install && \
  echo "Build Snort3" && \
  cd ${SRC_HOME} && \
  tar xvf snort3-${SNORT_VER}.tar && \
  cd ${SRC_HOME}/snort3-${SNORT_VER} && \
  ./configure_cmake.sh --prefix=/usr/local --enable-tcmalloc && \
  cd build && \
  make -j 4 && \
  make install && \
  # Cleanup compilation
  cd / && \
  rm -rf ${SRC_HOME} && \
  apk del \
    build-base \
    cmake
# Install all of our pip packages in a single directory that we can copy to our base image later
RUN mkdir /install && \
  mkdir /rules
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN addgroup snort3 && \
  adduser -h /app -G snort3 -D snort3
COPY src /app
RUN chown -R snort3:snort3 /app && \
  chmod 755 /app/app.py
USER snort3
WORKDIR /app

CMD ["python", "app.py", "--log-level", "DEBUG"]
