 ## 돌리는방법

 + url : https://colab.research.google.com/github/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Train_TFLite2_Object_Detction_Model.ipynb

 ## 폴더 배치

  + content
      + images
          + train
          + validation
          + test
          + all
          + raw_label
              + 라벨 데이터 폴더
          + train_labels.csv
          + validation_labels.csv

     + models
         + research
         + mymodel
             + mymodel.py
             + make_config.py
             + pipeline_config.config
             + fine tune 된 모델
         + 기타 등등
         + make_model.py
    
     + create_csv.py
     + create_tfrecord.py
     + file_check.py
     + val.tfrecord
     + train.tfrecord
     + labels.txt
     + labels.pbtxt

 ## 윈도우 세팅
 + proto 를 설치해야됨
     + 참고 url : https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=hong699822&logNo=220785332065
     + install url : https://github.com/protocolbuffers/protobuf/releases?page=5

 + proto 설치
     + pip install protobuf
     + pip install protobuf==3.20.0
     + pip isntall protobuf>=3.19.0
     + pip show protobuf
         + 버전이 3.20.0이여야됨

 + pycocotools를 설치해야됨
     + pip install model/reaserch/ 부분을 하면 pycocotools가 없다고 함
     + 이유는 윈도우에서 pycocotools를 지원안해서 그럼
     + 그래서 깃허브에서 클론해서 새로 pycocotools를 설치해야됨
     + 참고 url : https://eatchu.tistory.com/entry/window%EC%97%90%EC%84%9C-pycocotools-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0-error-Microsoft-Visual-C-140-or-greater-is-required-%ED%95%B4%EA%B2%B0
     + 위의 블로그에서 하라는대로 따라하면됨

 + pycocotools 가 설치 됬으면 pip install model/research/ 해주면되는데, 이때 model/research/ 는 절대결로로 할것

 + 사용할 파웨쉘이나 cmd에서 protoc object_detection/protos/*.proto --python_out=.


 ## 데이터 셋 세팅
 + 다운받은 데이터를 iamges/train/ 위치에 넣는다.
 + 라벨 데이터는 images/raw_labels/train/ 위치에 넣는다.
 + 다운받은 데이터를 iamges/validation/ 위치에 넣는다.
 + 라벨 데이터는 images/raw_labels/validation/ 위치에 넣는다.
 + check_file.py에서 PATH를 수정한다.
 + check_file.py를 실행한다.  ->  데이터 전처리 작업
 + check_file.py를 train과 validastion에 각각 실행해야됨


 + 이제 참고 url이 하라는 대로 한다.
    + create_csv.py 를 실행한다;
    + dataset.csv 파일이 생성되면 train인지 val인지 에 따라서 train_labels.csv 로 만들어 준다.
    + validsation도 똑같이 작업한다.
    + create_tfrecord.py를 시키는 대로 실행한다.
        + python3 create_tfrecord.py --csv_input=./images/train_labels.csv --labelmap=./labelmap.txt --image_dir=./images/train --output_path=./train.tfrecord
        + python3 create_tfrecord.py --csv_input=./images/validation_labels.csv --labelmap=./labelmap.txt --image_dir=./images/validation --output_path=./val.tfrecord


 ## 학습 준비
  + models/make_model.py를 실행한다.
  + mymodel 안에 있는 mymodel.py를 실행한다.
  + mymodel 안에 있는 make_config.py에 PATH 를 수정한다.
  + mymodel 안에 있는 make_config.py를 실행한다.
  + models 안에 있는 make_model.py에 exit()부분을 지우고 그 위를 모두 주석처리한다.
  + models 안에 있는 make_model.py를 실행한다.
  
