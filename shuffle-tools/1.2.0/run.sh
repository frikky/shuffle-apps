# Build testing
NAME=frikky/shuffle:shuffle-tools_1.1.0
docker rmi $NAME --force
docker build . -t frikky/shuffle:shuffle-tools_1.1.0

# Run testing
#docker run -e SHUFFLE_SWARM_CONFIG=run -e SHUFFLE_APP_EXPOSED_PORT=33334 frikky/shuffle:shuffle-tools_1.1.0
echo $NAME
#docker service create --env SHUFFLE_SWARM_CONFIG=run --env SHUFFLE_APP_EXPOSED_PORT=33334 $NAME

#cat walkoff_app_sdk/app_base.py #cat walkoff_app_sdk/app_sdk.py
