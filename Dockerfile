FROM python:3.5.1
RUN apt-get install git -y
RUN git clone http://zjr-test:12345678@30.207.40.196:8080/shiqh/work_manage.git /work_manage
RUN pip install -r /work_manage/requirements.txt
RUN python /work_manage/manage.py makemigrations
RUN python /work_manage/manage.py migrate
RUN python /work_manage/manage.py loaddata /work_manage/rbac/fixtures/menu.json
RUN python /work_manage/manage.py loaddata /work_manage/rbac/fixtures/superadmin.json
RUN python /work_manage/manage.py loaddata /work_manage/users/fixtures/post.json
RUN python /work_manage/manage.py loaddata /work_manage/workbench/fixtures/plan.json

EXPOSE 8080