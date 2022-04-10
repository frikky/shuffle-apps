# Base our app image off of the WALKOFF App SDK image
FROM frikky/shuffle:app_sdk as base

RUN apk update && \
    apk upgrade

# We're going to stage away all of the bloat from the build tools so lets create a builder stage

FROM base as builder
RUN apk add --no-cache build-base gcc musl-dev python3-dev libffi-dev libxml2-dev libxslt-dev alpine-sdk openssl-dev libc-dev ca-certificates
RUN pip install --no-cache-dir -U pip && \
    pip wheel --no-cache-dir --wheel-dir=/root/lxml_wheel lxml

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix="/install" -r /requirements.txt


FROM base
COPY --from=builder /root/lxml_wheel /root/lxml_wheel

# lxml binary dependencies
COPY --from=builder /usr/lib/libxslt.so.1 /usr/lib/libxslt.so.1
COPY --from=builder /usr/lib/libexslt.so.0 /usr/lib/libexslt.so.0
COPY --from=builder /usr/lib/libxml2.so.2 /usr/lib/libxml2.so.2
COPY --from=builder /usr/lib/libgcrypt.so.20 /usr/lib/libgcrypt.so.20
COPY --from=builder /usr/lib/libgpg-error.so.0 /usr/lib/libgpg-error.so.0

RUN python -OO -m pip install --no-cache --no-index --find-links=/root/lxml_wheel/* /root/lxml_wheel/*

COPY --from=builder /install /usr/local
COPY src /app

## Ensuring we can handle OLD exchange servers
RUN echo "MinProtocol = TLSv1/" >> /etc/ssl/openssl.cnf
run echo "CipherString = DEFAULT@SECLEVEL=1/" >> /etc/ssl/openssl.cnf
RUN cat /etc/ssl/openssl.cnf

# Finally, lets run our app!
WORKDIR /app
CMD python app.py --log-level DEBUG
