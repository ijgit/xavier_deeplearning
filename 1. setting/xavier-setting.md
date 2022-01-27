# Install TensorFlow and EdgeTPU in Xavier

- Xavier AGX, NX 보드에 동일하게 설치 가능

- `requirement.txt` 는 패키지 리스트를 포함
  
  - 해당 파일을 사용하여, 가상환경에서 패키지 설치 가능 (오류 발생 )
  
    

[TOC]

## System Information 

- **HW**: Jetson Xavier NX, AGX
- **JetPack version**: `4.6`
  - https://developer.nvidia.com/embedded/jetpack
  - jetpack은 위의 링크에서 sdk manager 을 다운받아 실행 가능
    - 설치방법 참조: 2개 글 실행 (2번째 글: 외장 ssd 를 통해 부팅할 수 있도록 설정하는 방법 기술)
      - 글 1: https://hikwail.tistory.com/22?category=943818
      - 글 2: https://hikwail.tistory.com/26?category=943818
    - TensorRT `8.0.1`
    - cuDNN `8.2.1`
    - CUDA `10.2`
- **TensorFlow version**:  `2.5.0`
- **Ubuntu version**: 18.04
- **Python**: `3.6` (ubuntu 기본 python 버전)





## 2. Install



TensorFlow 설치 전, 먼저 기본적인 시스템, 패키지를 설치한다.

### 2.1. 기본 설정

````bash
### Install virtualenv and Jupyter lab (기본 설정)

# install pip 
sudo apt-get install python3-pip -y

# install virtual env
python3 -m pip install virtualenv

# install jupyter lab
sudo pip3 install jupyterlab
````



설치를 완료하였으면 아래 글에 따라 jupyter lab을 설정한다.

- jupyter lab 설정

  - 아래 명령어를 실행하면, jupyter lab 설정파일이 생성 된다. (`/home/keti/.jupyter/jupyter_lab_config.py`)

    ```bash
    $ keti@keti:~/workspace$ python3 -m jupyterlab --generate-config
    Writing default config to: /home/keti/.jupyter/jupyter_lab_config.py
    ```

  - 아래 명령어를 실행하여 jupyter lab 비밀번호를 생성한다. 비밀번호는 `jupyter_server_config.json` 파일 내에 생성된다.

    ```bash
    $ python3 -m jupyterlab password
    Enter password:
    Verify password:
    [JupyterPasswordApp] Wrote hashed password to /home/keti/.jupyter/jupyter_server_config.json
    
    
    $ keti@keti:~/workspace$ cat ~/.jupyter/jupyter_server_config.json
    {
      "ServerApp": {
        "password": "argon2:$argon2id$v=19$m=10240,t=10,p=8$4d2gAmODPnOKxnxzLvo2OA$PKLhSHAfso/SY0iveln2KF9tOJ4kGR9VsaqMYDzA6jw"
      }
    }
    ```

  - 생성된 패스워드 (`$argon2id$v=19$m=10240,t=10,p=8$4d2gAmODPnOKxnxzLvo2OA$PKLhSHAfso/SY0iveln2KF9tOJ4kGR9VsaqMYDzA6jw`) 를 `.jupyter/jupyter_lab_config.py` 파일 내의 `c.ServerApp.password` 값으로 설정해준다. (line **391**)

    ```python
    #  The string should be of the form type:salt:hashed-password.
    c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$4d2gAmODPnOKxnxzLvo2OA$PKLhSHAfso/SY0iveln2KF9tOJ4kGR9VsaqMYDzA6jw'
    ```
    
  - 기타 설정

    ```python
    '''
    ~/.jupyter/jupyter_lab_config.py
    '''
    
    # 시작시 브라우저 
    c.ExtensionApp.open_browser = False
    
    
    # 외부 접속 허용
    c.ServerApp.allow_origin = '*'
    
    
    #  The string should be of the form type:salt:hashed-password.
    # password: 'qwer1234'
    c.ServerApp.password = 'argon2:$argon2id$v=19$m=10240,t=10,p=8$4d2gAmODPnOKxnxzLvo2OA$PKLhSHAfso/SY0iveln2KF9tOJ4kGR9VsaqMYDzA6jw'
    
    # ip
    c.ServerApp.ip='192.168.50.186'
    
    # port
    c.ServerApp.port=8888
    
    ```
  
    
  
  
  
  **error**
  
  ```bash
  # 아래와 같은 오류 발생 시, 
  Command python setup.py egg_info failed with error code 1 ..
  
  # 아래 코드 실행
  python3 -m pip install --upgrade --ignore-installed pip setuptools
  ```
  
  

### 2.2. System package 설치

Install system packages required by TensorFlow:

```bash
$ sudo apt-get update
$ sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
```



pip install packages

```bash
$ sudo apt-get install python3-pip
$ sudo python3 -m pip install -U pip testresources setuptools==49.6.0 
$ sudo python3 -m pip install Cython
$ sudo env H5PY_SETUP_REQUIRES=0 python3 -m pip install -U h5py==3.1.0
```



Install the Python package dependencies

```bash
$ sudo python3 -m pip install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig

$ sudo env H5PY_SETUP_REQUIRES=0 python3 -m pip install -U h5py==3.1.0
```



### 2.3. 가상환경 생성

```bash
# 가상환경 생성
python3 -m virtualenv <chosen_venv_name>
# python3 -m virtualenv tf_2.5.0 # tf_2.5.0 이름으로 생성

# 가상환경을 활성화
cd tf_2.5.0
source bin/activate
```



### 2.4. tensorflow install

(가상환경 활성화 후 설치)

```bash
# 종속 패키지 설치 
pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast  astor h5py termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta setuptools testresources

# h5py 설치 시, 오류 발생 (libhdf5-dev, cython3 설치 후, h5py 재설치)
sudo apt-get install libhdf5-dev
sudo apt install cython3
pip3 install h5py


# tensorflow 2.5 설치
pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow==2.5.0
```



- tensorflow 를 import 할 때 (core dumped) 오류가 발생한다면, numpy 를 import 해본다.

  numpy import 가 오류가 난다면, 아래 명령어로 numpy 를 다시 설치해준다.

  - https://forums.developer.nvidia.com/t/illegal-instruction-core-dumped/165488/10

  - https://github.com/numpy/numpy/issues/18131

    ```bash
    # 해결: numpy 1.19.4 재설치
    pip install numpy==1.19.4
    ```

- matplot lib  설치

  ```bash
  pip install matplotlib
  ```

  

### 2.5. 커널 생성

(가상환경 활성화 후 설치)

```bash
pip3 install ipykernel

# VENV_NAME (사용자 설정 이름) 으로 가상환경 생성
python3 -m ipykernel install --user --name=VENV_NAME 
# python3 -m ipykernel install --user --name=_tf_2.5.0

```







## 3. Install EdgeTPU 

- TensorFlow Lite 모델을 Edge TPU 와 호환되는 파일로 컴파일하는 명령줄 도구

- Edge TPU 모델은 Coral USB Accelerator와 같은 Edge TPU 장치에서 실행되도록 특별히 컴파일된 TensorFlow Lite 모델



### 3.1. Install TensorFlow Lite, and EdgeTPU compiler

```
시스템 요구사항

- 64비트 버전의 Debian linux
- x86-64 시스템 아키텍처
- Edge TPU 컴파일러는 버전 2.1부터 ARM64 시스템(예: Coral Dev Board)에서 더 이상 사용할 수 없습니다. 보다 강력한 데스크탑에서 모델을 컴파일하는 것이 좋습니다.
```

시스템 요구사항에 따라 ARM64 시스템에 EdgeTPU 컴파일러를 설치하기 위해서는, `2.1` 버전 이하를 설치해야 한다. 

[링크](https://github.com/google-coral/edgetpu/tree/657d2b654101540164af240eacb31440ff6f535d) 에서 이전 버전 arm64 용 컴파일러가 있는 버전을 다운로드한다.

- reference
  - https://github.com/google-coral/edgetpu/issues/311
  - https://github.com/google-coral/edgetpu/tree/657d2b654101540164af240eacb31440ff6f535d



**Run `cd packages/edgetpu/` to switch current working directory**

```bash
$ mv 로 edgetpu-xxxxx 를 edgetpu 로 이름 변경
$ cd edgetpu/
```



**Run `scripts/runtime/install.sh` to install Edge TPU runtime**

```bash
$ sudo scripts/runtime/install.sh

....
................................................................................
Would you like to enable the maximum operating frequency for your Coral USB device? Y/N
y
Using the maximum operating frequency for Coral USB devices.
Installing device rule file [/etc/udev/rules.d/99-edgetpu-accelerator.rules]...
Done.
Installing Edge TPU runtime library [/usr/lib/aarch64-linux-gnu/libedgetpu.so.1.0]...
Done.

```



Run `make wheel` to generate python wheel and then `pip3 install $(ls dist/*.whl)` to install it

```bash
$ make wheel 
$ pip3 install $(ls dist/*.whl)
Successfully installed edgetpu-2.13.0
```



### 3.2. Add EdgeCompiler to PATH

아래 명령어를 실행하거나 `.bashrc` 파일에 추가하여, 컴파일러 파일이 있는 경로를 환경변수에 추가한다.

컴파일러는 압축을 푼 edgetpu 아래 /compiler/aarch64 (os) 에 존재한다.

`pwd` 명령어로 현재 경로 확인 가능

```bash
# export PATH=$PATH:EDGE_TPU_COMPILER_PATH
export PATH=$PATH:/home/keti/tf_2.5.0/src/edgetpu/compiler/aarch64
```

- `.bashrc` 파일에 추가하는 경우 `source .bashrc` 명령어를 실행해준다.



edgetpu_compiler 가 위치해 있지 않은 디렉토리에서 아래 명령어를 실행해, 환경변수가 잘 추가되었는지 확인한다.

```bash
$ edgetpu_compiler -v
Edge TPU Compiler version 2.0.291256449
```



edgetpu_compiler 로 resnet50.tflite 모델을 변환한다.

성공적으로 변환되었으면 resnet50_edgetpu.tflite 파일이 생성된다. 

```bash
$ edgetpu_compiler resnet50.tflite 
Edge TPU Compiler version 2.0.291256449

Model compiled successfully in 2356 ms.

Input model: resnet50.tflite
Input size: 25.08MiB
Output model: resnet50_edgetpu.tflite
Output size: 24.87MiB
On-chip memory available for caching model parameters: 6.25MiB
On-chip memory used for caching model parameters: 6.25MiB
Off-chip memory used for streaming uncached model parameters: 18.43MiB
Number of Edge TPU subgraphs: 1
Total number of operations: 77
Operation log: resnet50_edgetpu.log
See the operation log file for individual operation details.
keti@keti:~/workspace/tf_2.5.0/src/edgetpu-classification$ 
```





### 3.3. Install tflite_runtime

`tf.lite.Interpreter` 를 사용하면 edgetpu_compiled 모델 로드 오류 발생

- reference: https://www.tensorflow.org/lite/guide/python?hl=ko

python 3.6 기준 아래 명령어 실행

```
python3 -m pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_aarch64.whl
```



인터프리터 생성은 아래 코드 사용 (usb accelerator 가 연결되어 있어야 한다.)

```python
import tflite_runtime.interpreter as tflite

interpreter = tflite.Interpreter('resnet50_edgetpu.tflite' , 
                          experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
interpreter.allocate_tensors()
```







