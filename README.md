# aroundUs API server

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
$ 한 번 세팅이 끝난 이후에는 작업할 때 git에 push 이후에 eb deploy
```

```
Main Libraries
$ django-rest-framework, swagger 사용
$ 파이어베이스 푸쉬 알림 -> firebase_admin 사용
$ 커머스 구현 -> clayful 사용 -> clayful 사용
$ 매거진 구현 -> 어드민 상에서 WYSIWYG 방식으로 구현 -> django-summernote 사용
$ 커뮤니티 -> 직접 구현함.
```