#!/bin/sh

imagesid=`docker images | grep -i docker-work-manage | awk '{print $3}'`
project=`pwd`

if docker ps -a | grep -i work_manage;then
    docker rm -f work_manage
fi

if [ -n "$imagesid" ];then
    docker rmi $imagesid -f
else
    echo $imagesid "is null"
fi
cd $project

docker build --no-cache -t docker-work-manage .

docker run -it -d -p 8099:8080 --name work_manage docker-work-manage /bin/sh -c "python /work_manage/manage.py runserver 0:8080"