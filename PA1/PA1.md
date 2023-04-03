# PA1
notes and simple tutorials for PA1

## python 으로 html을 local host에서 실행
과제에서 포트를 1398로 지정하도록 되어있어서, vs code의 포트는 바꾸기가 귀찮기도 하고, python으로 서버를 구동하는 방법을 알아보려 한다.
* python version : 3.9 (3.X)
실행 커멘드 (실행하고자 하는 html 파일이 있는 경로에서 실행해야 함.)
```
python -m http.server 1398
```
이후 chrome 주소창에 `localhost:1398` 을 입력하면 된다. 이번 과제의 test.html을 실행시키고 싶은 경우, `localhost:1398/test.html` 으로 들어가면 된다.
### 문제점
위 방법으로 서버를 열면, get, post하는 목록을 커맨드창에서 볼 수 있다. 하지만, 서버 파일을 추가적으로 실행시키면 데이터가 그 커멘드창의 서버로 가지 않았다. 그래서 이번 과제에서는 이렇게 여는 게 아니라는 말.

### 결론
그냥 크롬으로 열면 잘 돌아가더라.