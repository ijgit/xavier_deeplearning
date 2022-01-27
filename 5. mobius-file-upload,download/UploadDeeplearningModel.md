

# Upload Trained DeepLearning Model to Mobius Server Platform



**컴퓨터 환경**

- ubunt, windows 관계없이 실행 가능



[TOC]

## System Structure

IoT Server Platform 을 통해 Trained Model File 을 공유하기 위한 시스템 구조는 아래와 같다. `Server for File Upload` 은 파일을 업로드하는 서버이고, Mobius 는 `IoT Server Platform` 이다.

![system](src\system.png)

mobius 의 db 는 sql 이기 때문에, 이미지나 기타 용량이 큰 파일들은 저장이 어렵다. 때문에 mongoDB를 사용하는 서버를 따로 만들어, 해당 서버에 파일들을 저장할 수 있게 하였다. 파일에 접근할 수 있는 url 을 따로 mobius 에 업로드하여 파일을 공유할 수 있다 (현재 get 기능만 구현되어 있음).



### file upload server 설치 / 실행

mongoDB 와 node.js 로 구현되어 있으며, windows 10과 ubuntu 20.04  OS 에서 실행을 확인 하였다. 



#### mongoDB Install

[링크][https://www.mongodb.com/try/download/community ]에서 OS 에 맞는 파일을 다운로드 하여 설치한다.



#### Node.js Install

[링크][https://nodejs.org/ko/download/ ]에서 OS 에 맞는 파일을 다운로드 하여 설치한다. (LTS 버전으로 테스트 되었음)



#### setting

##### package 설치

`Server for File Upload` 코드는 `file_upload_server` 디렉토리 내에 있다. 먼저 `npm install` 명령어를 실행하여 패키지 파일들을 설치해준다.

```bash
cd file_upload_server
npm install
```



##### 환경 설정

`file_upload_server` 디렉토리 내의 `/conf.js` 파일을 수정하여, 변수 설정을 할 수 있다. 컴퓨터 환경에 맞게 변수들을 수정해준다.

```javascript
module.exports = {
    ip: `192.168.50.157`,   // mongodb server ip addr
    port: 3000,
    db_name: 'test',

    // mobius
    mp_url: '203.253.128.161:7579/Mobius',  // mobius ip
    ae: 'jeong'                             // mobius ae name
}
```

- `ip` : 서버를 실행할 컴퓨터의 ip 주소
- `port`: 서버의 포트 번호
- `db_name`: mongodb에 생성한 db 이름
- `mp_url`: mobius 주소와 cse 이름
  - `mobius_ip`:`mobius_port`/`cse_name`  형식을 따른다
- `ae`: mobius 에 생성한 ae 이름



##### 실행

`node app.js`  또는 `npm start`명령어를 입력하여 실행을 확인한다.

```bash
# 실행방법 1
> node .\app.js
203.253.128.161:7579/Mobius/jeong/model
localhost: 3000
app listening on port  3000
```

```bash
# 실행방법 2
> npm start    
Debugger attached.

> file_upload_server@1.0.0 start
> node app.js

Debugger attached.
203.253.128.161:7579/Mobius/jeong/model
localhost: 3000
app listening on port  3000
```



## Upload Trained Model to Mobius

파일을 업로드하는 절차는 아래와 같다.

File Upload Server 는 클라이언트 (`local computing system`) 로부터 파일 업로드 요청을 받으면, 이를 DB 에 저장하고, 파일을 다운로드 할 수 있는 URL 을 CIN (Content INstance)로써 Mobius 에 생성한다.

![file_upload](src\file_upload.png)



아래 그림은 Mobius에 생성된 CIN 을 보여준다.  `url` 이 파일을 다운로드 할 수 있는 url 을 나타내고 있다.

![file_upload_include_cin](src\file_upload_include_cin.png)

```json
{
    "m2m:cin": {
        "pi": "3-20211028110615761263",
        "ri": "4-20211110035101311852",
        "ty": 4,
        "ct": "20211110T035101",
        "st": 22,
        "rn": "4-20211110035101310",
        "lt": "20211110T035101",
        "et": "20231110T035101",
        "cs": 171,
        "cr": "{{aei}}",
        "con": {
            "id": "618b41b083466e82c5e0072e",
            "filename": "frozen_graph.pb",
            "url": "http://localhost:3000/models/download?cnt=model&id=618b41b083466e82c5e0072e&filename=frozen_graph.pb"
        }
    }
}
```



#### upload test

업로드 코드는 `file_upload_client/upload.ipynb` 를 실행하면 된다. 

파일 내의 셀들을 다 실행하고 결과로 나온 download link 를 통해 다운로드가 가능한지 확인한다.

```bash
'{"message":"File uploaded successfully, download link: http://192.168.50.157:3000/models/download?cnt=model&id=61d2a69363daa0519def6b47&filename=frozen_graph.pb"}'
```





## Download Trained Model from Mobius

클라이언트 (`local computing system`)은 Mobius 에 GET Request 를 보내 가장 최근의 CIN 값을 가져온다. 이후 CIN 내의 `url` 값으로 파일 다운로드 요청을 보내 Deep Learning Model 파일을 다운로드한다.  

![download_file](src\download_file.png)



#### download test

업로드 코드는 `file_upload_client/download.ipynb` 를 실행하면 된다.

셀들을 실행했을 때, `CIN` 값을 잘 가져오는 지 확인하고, `CIN` 내의 값들을 통해 파일을 다운로드 할 수 있는 지 확인한다.

