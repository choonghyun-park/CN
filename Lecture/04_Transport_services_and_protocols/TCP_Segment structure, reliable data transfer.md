# TCP - Segment structure, reliable data transfer

## TCP: overview RFCs: 793, 1122, 2018, 5681, 7323

- point-to-point
    - 1 sender, 1 receiver
- reliable, in-order byte stream
    - byte stream으로 메시지를 전송하기 때문에, 일련의 데이터를 적당히 잘라서 보낸다. 따라서 메시지의 boundary가 따로 존재하지 않는다.
- full duplex data (전이중 통신, 양방향 통신)
    - 같은 connection 내에서 양방향 통신이 가능하다는 뜻
    - MSS : maximum segment size

## Cumulative ACKs

- 뒤에 나오겠지만, receiver가 받은 패킷의 sequence가 연속적으로 오지 않으면, 오지 않은 seq 의 ACK만 계속 요청한다. rdt에서 `Go-Back-N` 방식이라고 보면 된다.

## Pipelining

TCP 혼잡도를 고려해 flow control을 하여, window size를 적당히 조절한다. (확실히 이해 못함.)

## Connection-oriented

- hand-shaking : data를 서로 교환하기 이전에, control message를 교환하여서 sender와 receiver 의 상태를 initialize 한다.

### Flow controlled

- sender가 receiver를 압도하게 트래픽을 보내서는 안된다.

## TCP segment structure

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled.png)

## TCP sequence numbers, ACKs

### Sequence numbers

TCP 에서 `sequence number`는 전체 데이터가 byte stream으로 이루어져 있을 때, 보내고자 하는 segment 의 첫번째 byte 숫자이다. rdt에서는 sequence number가 0,1,2, … 의 임의의 값으로 설정되었는데, 실제로는 보내는 데이터의 길이도 매번 다르고 해서 그런지(뇌피셜이기 함) 매 자리마다 sequence 값이 정해져있고, 보낼 때는 띄엄띄엄 적어서 보낸다.

### Acknowledgements

다음으로 전송되어야 할 바이트의 sequence #를 적어서 ACK으로 보낸다.

receiver가 받은 마지막 데이터가 seq=100, byte length=20 이었다면, ACK으로는 ACK=120을 보낸다. 

이때 receiver도 seq 값을 보낸다. 이는 뒤에서 알아보자.

## TCP sequence numbers, ACKs

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%201.png)

## TCP round trip time, timeout

> TCP의 timeout 값은 어떻게 잡는게 좋을까?
> 

RTT 값보다는 크게 잡아야 하는데, RTT 값 자체가 다양한 편이다.

- 너무 작게 잡으면 : 성급한 timeout으로 인해 불필요한 retransmission이 발생한다.
- 너무 길게 잡으면 : segment loss 에 대해서 늦게 반응해야 한다.

> 어떻게 RTT를 측정하지?
> 
- Sample RTT
    - segment 를 보내고, ACK이 오기까지의 시간을 측정한다.
    - retransmission은 무시한다.
- Sample RTT는 다양하게 측정되며, 최근 여러개의 RTT 평균값으로 계산한다고 한다.

### RTT 측정 및 그래프

아래 공식처럼 RTT를 계산하여서 순간적으로 값의 변동이 일어나도 더 smooth 하게 값을 측정할 수 있다. 알파 값은 일반적으로 0.125를 쓴다.

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%202.png)

### TimeoutInterval

TimeoutInterval은 EstimatedRTT에 safety margin을 더해서 계산한다. 

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%203.png)

### DevRTT

EWMA sampleRTT에서 estimatedRTT의 분산을 개념이다. 

- [ ]  TODO: 분산인데 왜 베타의 선형합으로 표현되는지는 잘 모르겠다. 시간되면 알아보기.

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%204.png)

### TCP sender (simplified)

## event - data received from application

- seq #를 포함한 segment를 만든다.
- seq #를 지금 보내야 할 segment의 첫번째 byte stream number로 설정한다.
- 만약 timer가 작동되고 있지 않다면, timer를 시작한다.
- timer는 가장 처음에 unACKed segment를 논의했던 때의 timer라고 보면 된다.
    - [ ]  TODO: 그래서 그게 뭔데;; unACKed segment의 timer가

### event - timeout

- timeout을 일으킨 segment를 retransmission 한다.
- restart timer

### event - ACK received

- 전에 unACK이었는데, ACK으로 잘 도착했다면 여기서 얻을 수 있는 정보를 업데이트 해준다.
- unACKed segment가 아직 존재한다면 timer를 다시 시작해준다.

## TCP Reciever: ACK generation [RFC 5681]

아래 표를 일일이 이해해보려 했는데, 그냥 action 설명한 파트를 이해하는게 결국 같은 말인 것 같다. 한글로 대충 정리해놓은 페이지는 [여기](https://velog.io/@lychee/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-3.3-TCP-Flow-Control)를 참고하자.

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%205.png)

## TCP: retransmission scenarios

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%206.png)

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%207.png)

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%208.png)

## TCP fast retransmit

TCP 는 cumulative하게 데이터를 수신하기 때문에, 중간에 gap이 생기면 이후에 도착한 패킷에 대해서는 gap에 해당하는 ACK만 보내게 된다. 그래서 아래 그림처럼 ACK = 100 이 한번 오고나서, 다음으로 안넘어가고 3번이 더 온 것이다. 100번 시퀀스의 패킷을 다음으로 얻어야하기 때문이다.

여기서 duplicate ACK이 3개여서 `triple duplicate ACK` 이라고 굳이 이름붙일 수 있는데, 추가적으로 온 3개를 가리킨다. 이것은 sender가 패킷을 보냈지만, receiver가 받지 않은 패킷의 개수이기도 하다.

TCP는 `fast retransmit` 이라고 해서, `triple duplicate ACKs` 가 발생하면, 앞의 패킷이 유실되었다고 판단하고, 바로 해당 seq의 패킷을 다시 보내주는 정책을 사용한다.

![Untitled](TCP%20-%20Segment%20structure,%20reliable%20data%20transfer%207658274c9c204917a303907592e208e5/Untitled%209.png)
