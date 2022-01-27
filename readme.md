# 자료 정리




## 1.setting

xavier 보드에 설치한 소프트웨어 사양과 설치방법 등을 포함하고 있다. 

`xavier-setting.md` 파일의 내용과 참조 링크들을 참고하여 설치가능하다. 


</br>

-----



## 2. TF-tensorRT (TF-TRT)

 Tensorflow 와 TensorRT 를 사용하여 모델을 변환하고 추론하는 예제이다.  `tftrt-classification.ipynb` 파일부터 보면 된다.

saved model 형식의 모델을 사용하는 코드부터, saved model을 frozen graph로 변환하고 frozen graph를 통해 추론을 하는 코드가 있다.

- saved model : SavedModel에는 가중치 및 연산을 포함한 완전한 텐서플로 프로그램이 포함된다. 모델 코드를 공유하고 배포할 때 주로 사용한다.
- frozen graph: 더 이상 학습이 불가하도록 가중치와 모델 구조를 결합한 형태이다. 디바이스에 포팅할 때 주로 사용한다.


</br>

-----




## 3. TFLite-edge tpu

 Tensorflow Lite 와 Edge TPU 를 사용하여 모델을 변환하고 추론하는 예제이다.  `edgetpu_classifier.ipynb` 파일부터 보면 된다.


</br>

-----



## 4.



### 4.1. run tf-trt, lite

- `function_devide_running_model.ipynb` 파일 존재
- TF-TRT (TensroFlow - TensorRT) 와 TFLite (edgeTPU) 모델을 사용하여 추론하는 예제이다.

</br>

### 4.2. model test

- `./saved_models`: 학습시킨 모델의 weight 를 저장한 폴더로 `h5`으로 되어있는 파일들을 `saved_model` 형식으로 converting 해주어야 한다.
- `./dataset`: 테스트를 위해 클래스별로 100개씩 추출한 데이터 셋
- `./testdata`: 테스트를 위해 클래스별로 10개씩 추출한 데이터 셋 
- `./test-code`: 참조 테스트 코드 
- `./1. converting_models`: `saved_models` 내의 모델 weight들을 `saved_model` 형식으로 변환해주는 코드로 먼저 실행해야한다.
- `./2. tftrt_test`: TF-TRT 모델을 변환하고 테스트하는 코드 
- `./3. tflite_test`: TF-LITE 모델을 변환하고 테스트하는 코드



#### 실행순서

1. converting
   - `1. converting_models` 내의 `converting_model.ipynb` 를 실행한다. `converting_model.ipynb` 은 `h5` 형식으로 저장된 모델을 `saved_model` 형식으로 변환한다. model 경로를 알맞게 수정한 뒤 셀을 실행하면 된다.
2. TF-TRT
   - saved_model 을 TensorRT 로 변환한뒤, 정확도와 속도 등을 측정한다. 소스코드는 `2. tftrt_test` 디렉토리 내에 있다.
   - 첫 번째로 `converting.ipynb` 내의 코드를 이용하여 모델을 TensorRT 에 맞는 모델로 변환한다. Import Libraries, Define, converting 파트까지만 수행해도 괜찮다.
   - 두 번째로, Tensorflow, TF-TRT를 테스트 하기 위해, `2. tftrt_test` 내의 `tftrt_classifier_test.ipynb` 를 실행한다. 해당 파일은 테스트 데이터셋을 사용하여 모델을 테스트하는 코드이다. `tftrt_classifier_test-debug.ipynb` 도 테스트 데이터를 사용해 모델을 테스트하는 코드이며 추가로, 표에 어떠한 사진을 어떤 클래스로 추론했는지를 표시한다.  `4.2. model test/dataset` 에는 클래스 별 100개의 데이터가, `4.2. model test/Test_data` 에는 클래스 별 10개의 데이터가 있다. 
3. TF-Lite
   - 세 번째로 `3. tflite_test`에는  Tensorflow lite 를 테스트하는 코드가 있다. 기능은 TF-TRT 와 동일하며, 다른점은 TF-TRT 가 아니라 TF-Lite 로 변환한 모델을 테스트한다. Edge TPU 가 있어야 실행할 수 있다.
4. loading term
   - 모델을 로딩하는 예제이다. keras.models.load_model 함수를 사용하는 것과, 저장된 모델구조와 가중치로부터 모델을 구성하는 시간을 비교한다.



</br>

-----


## 5. mobius-file-upload, download

파일 업로드 서버코드 (node.js) 와 파일 업로드/다운로드 클라이언트 (python) 코드를 포함하고 있다.

`UploadDeeplearningModel.md` 파일을 참고하여 실행하면 된다 
