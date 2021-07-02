# Python DRF example

## Quick start

```
Make directory in Pycharm
$ git clone https://github.com/flame-change/change.git
$ pip install -r requirements.txt
$ python manage.py runserver
$ ebs-cli 프로필 설정 : .aws 폴더 생성 > .config 파일 생성 후 aws 프로필 내용 작성
```

```
How To Deploy
$ eb init --profile '프로필 이름' -> ebs 관련 폴더가 로컬에 생성됩니다.
$ eb deploy '환경 이름' -> 해당 환경에 변경사항을 배포합니다.
$ eb open
```