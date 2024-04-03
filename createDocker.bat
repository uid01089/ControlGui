pip freeze > requirements.txt
docker build -t controlgui -f Dockerfile .
docker tag controlgui:latest docker.diskstation/controlgui
docker push docker.diskstation/controlgui:latest