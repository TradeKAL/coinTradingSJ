## coin-trading

### 테스트 실행환경 구성

#### 1. 환경 구축

* python >= 3.8

* Python Package 설치
    ````shell
    pip install -r requirements.txt
    ````

* RabbitMQ 서버 실행
    ````shell
    docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
    ````
