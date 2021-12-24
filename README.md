# RideFlux AI Challenge IDS Team

해당 AI Challenge는 2D 이미지 상에서 물체를 인식하고 트래킹하는 것을 목표로 한다.


라벨은 Pedestrian, Vehicle, Bike가 있으며, Train, Validation, Test 데이터가 제공된다.

____

## Datasets

데이터셋은 크게 3가지로 구분된다. 주최측에서 제공한 데이터 (이하 Rideflux Data), MSCOCO 그리고 CityScapes 데이터셋이다.

- RideFlux : 주어진 Train, Val, Test 데이터 사용
- [MSCOCO](https://cocodataset.org/#download) : 2017 Train, Val, Test 데이터 다운로드
- [CityScapes](https://www.cityscapes-dataset.com) : LeftImg8bit - gtFine 데이터 다운로드

Object Detector에 학습시키기 위하여, 세 종류의 Dataset을 COCO Format으로 변경할 필요가 있다.

#### RideFlux : `utils/rideflux2coco.py` 파일 실행

```
utils 내부에서 
python rideflux2coco.py 실행
```

#### CityScapes : [CityScapes-to-coco-conversion](https://github.com/TillBeemelmanns/cityscapes-to-coco-conversion) Github Link 참조 


