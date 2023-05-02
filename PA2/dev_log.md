# Development Log
개발 과정과 그 날 한 일. 앞으로 해야할 일 등을 적은 페이지이다.

# PA1
## 230430
* VM Ubuntu18.04 2개 깔았음. 
Ubuntu 18.04.3 iso 파일을 사용하였음. 교안은 18.04.6(가장 최신)을 지시하지만, 용량이 커서 다운받는데 시간 많이 걸려서 그냥 이전에 다운받은 버전을 사용했다. 

```
VM username : chpark
VM passwrod : 231251
```

* P1 ~ 4 까지 포멧은 만들어 놨음.

### VM 다운 링크
* [VirtualBox Download](https://www.virtualbox.org/wiki/Downloads)
* [우분투 18.04 이미지](https://releases.ubuntu.com/18.04/)



### 230501
P1 에서 receiver 측에서 buffer overflow가 발생함. sender에서는 확실하게 buffer_size-1 값으로 보내주고 있음. 왜 overflow가 발생하는 지는 모르겠지만, 일단 해당 오류인 `OSError` 가 발생하는 경우 `buffer overflow!!` 를 출력하고 continue 하도록 해놨음. 근데, 이게 보내고자 하는 데이터 용량이 큰 경우에 간혹 발생하는 것이고, 1KB 의 데이터 크기에서는 문제 없이 작동함.\
결론적으로 과제에서 명시한 사항인 log 파일을 만드는 것은 잘 해결한 것 같은데 시간 나면 수정해 보도록 하자.  


# P2
## Segment format
![udp_segment](https://user-images.githubusercontent.com/78340346/235591670-ccc96ab9-2437-4a52-b3c7-e28cb538e464.png)
![tcp_segment](https://user-images.githubusercontent.com/78340346/235591647-97b7991e-5697-4641-8adc-306a8b2eeb1b.png)


## TODO
* PA_tools 이해하기. [V]
* 서버 두개 구현해서 값 주고받기. [V] 
* 서버 역할까지 구현하기. [V]
* P1 에서 receiver 측에서 overflow가 발생함. 

