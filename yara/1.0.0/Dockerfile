# Base our app image off of the WALKOFF App SDK image
FROM frikky/shuffle:app_sdk as base

# We're going to stage away all of the bloat from the build tools so lets create a builder stage
FROM base as builder

# Install all alpine build tools needed for our pip installs
RUN apk --no-cache add --update alpine-sdk libffi libffi-dev musl-dev openssl-dev

# Install all of our pip packages in a single directory that we can copy to our base image later
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix="/install" -r /requirements.txt

### Switch back to our base image and copy in all of our built packages and source code
FROM base
COPY --from=builder /install /usr/local
COPY src /app

# Install any binary dependencies needed in our final image
# RUN apk --no-cache add --update my_binary_dependency
ENV YARA_VERSION 4.0.2
ENV YARA_PY_VERSION 4.0.2
#RUN apk add --no-cache openssl file jansson bison python3 tini su-exec wget
#RUN apk add --no-cache -t .build-deps py3-setuptools openssl-dev jansson-dev python3-dev build-base libc-dev file-dev automake autoconf libtool flex git

### INSTALLING EVERYTHING REQUIRED
RUN apk add openssl file jansson bison python3 tini su-exec wget
RUN apk add -t .build-deps py3-setuptools openssl-dev jansson-dev
RUN apk add python3-dev build-base libc-dev file-dev automake
RUN apk add autoconf libtool flex git

### SETTING UP YARA
RUN set -x
RUN echo "Install Yara from source..."
RUN git clone --recursive --branch v$YARA_VERSION https://github.com/VirusTotal/yara.git /tmp/yara
RUN cd /tmp/yara
WORKDIR /tmp/yara
RUN ./bootstrap.sh
RUN sync
RUN ./configure --with-crypto --enable-magic --enable-cuckoo --enable-dotnet
RUN make
RUN make install
RUN echo "Install yara-python..."

### SETTING UP YARA PYTHON
RUN git clone --recursive --branch v$YARA_PY_VERSION https://github.com/VirusTotal/yara-python /tmp/yara-python
RUN cd /tmp/yara-python
WORKDIR /tmp/yara-python
RUN python3 setup.py build --dynamic-linking
RUN python3 setup.py install
RUN apk del --purge .build-deps

### SETTING UP YARA RULES
RUN git clone https://github.com/Yara-Rules/rules /rules

# Finally, lets run our app!
WORKDIR /app
CMD python app.py --log-level DEBUG
