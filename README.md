# RideFlux AI Challenge IDS Team

해당 AI Challenge는 2D 이미지 상에서 물체를 인식하고 트래킹하는 것을 목표로 한다.


라벨은 Pedestrian, Vehicle, Bike가 있으며, Train, Validation, Test 데이터가 제공된다.

이어질 설명에서 `변경한다`라는 말이 있을 경우, 해당 파일에서 `TODO`를 찾으면 된다.

------

## 0. Datasets

데이터셋은 크게 3가지로 구분된다. 주최측에서 제공한 데이터 (이하 Rideflux Data), MSCOCO 그리고 CityScapes 데이터셋이다.

- RideFlux : 주어진 Train, Val, Test 데이터 사용
    - `utils/picsize.py`를 통해 Annotation의 이미지 크기와 실제 이미지 크기와 다른 이미지의 Annotation을 변경한다.
- [MSCOCO](https://cocodataset.org/#download) : 2017 Train, Val, Test 데이터 다운로드
- [CityScapes](https://www.cityscapes-dataset.com) : LeftImg8bit - gtFine 데이터 다운로드

Object Detector에 학습시키기 위하여, 세 종류의 Dataset을 COCO Format으로 변경할 필요가 있다.

------

## 1. Data Preprocessing

### 1.1 Datasets to COCO Format

주어진 파일들을 JSON COCO Format으로 바꾼다. COCO Format은 해당 [웹사이트](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch) 를 참고하길 바란다. 
- RideFlux : `utils/rideflux2coco.py` 파일 실행
    - `rideflux2coco.py` 파일 내에서 파일을 저장할 디렉토리 등을 잘 설정
    - 일반적인 MSCOCO Format과 다르게 Image Annotation에 `VideoId`, `FrameId` 추가
    - 마찬가지로  Instance Annotation에 `TrackId` 추가

```
python rideflux2coco.py 
```

- CityScapes : [CityScapes-to-coco-conversion](https://github.com/TillBeemelmanns/cityscapes-to-coco-conversion) Github Link 참조 


### 1.2 COCO Formats

COCO Format으로 바뀐 파일들을 하나의 파일로 통합한다.
- `utils/mergecocoformat.py`를 통해 통합된 COCO Format Train, Val 파일을 만든다.
    - 1.1 에서 처럼 적절한 디렉토리를 설정해줘야 한다. 단, COCO와 CityScapes를 Val 파일로 쓰지 않을 경우, 코드 내에서 해당 부분을 주석처리 해주면 된다.

- 뒤에 [DynamicHead](https://github.com/monchana/DynamicHead)의 경우, Test 데이터를 Infer하기 위해서는 비어있는 Annotation 파일이라도 필요하다. 따라서 `utils/make_test_anno.py`을 통해 이미지 정보만 가지고 있는 Test Data Annotation 파일을 생성한다.

------

## 2. Object Detection 

Object Detection의 기본적인 형태는 SOTA인 Microsoft의 [DynamicHead](https://github.com/microsoft/DynamicHead)를 이용하였다. 레포 상에 있는 폴더는 작성자가 Fork한 레포로 연결된다. 실행 방법은 해당 레포 내의 `README.md`를 참고하길 바란다. 

Fork된 [DynamicHead](https://github.com/monchana/DynamicHead)에서 생성된 모델 중, Validation를 통해 적정한 모델을 선택하고, 이를 Test Data에 돌린다.


------

## 3. Object Tracking

Tracking의 기본적인 형태는 [ByteTrack](git@github.com:ifzhang/ByteTrack.git)을 이용하였다. 마찬가지로 레포 상에 있는 폴더는 작성자가 Fork한 레포이다. 실행 방법은 해당 레포 내의 `README.md`를 참고하길 바란다. 

Fork된 [ByteTrack](git@github.com:monchana/ByteTrack.git)를 이용해 DyHead로 생성된 Test Data Inference 결과에 Tracking을 돌린다. 

------

## 4. Post Processing

Object Tracking을 완료하면 [MOT](https://motchallenge.net) 형식으로 파일이 생성된다.

`utils/mot2rideflux.py` 파일로 이를 `RideFlux` Format에 맞게 변경해 주면 된다. 마찬가지로 디렉토리 위치 등은 파일 내에서 설정하면 된다. 
