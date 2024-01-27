### Apex Recoils

apex自动识别枪械压枪宏，暂时只完成了脚手架。数据开发中……

### 功能清单

- [x] 自动识别枪械
- [x] 鼠标平滑移动
- [x] 适配 km_box A km_box net,无涯键鼠盒子
- [x] 支持保存配置，多配置切换
- [ ] 枪械数据开发中，规划：
    - [ ] CAR
    - [ ] R99
    - [ ] R301
    - [ ] 平行步枪
    - [ ] 电冲
    - [ ] 转换者
    - [ ] 猎兽
    - [ ] re45
    - [ ] 暴走
    - [ ] L星
    - [ ] 喷火
    - [ ] 哈沃克
    - [ ] 专注
- [x] 支持抖枪，大小写开关
- [x] 自动识别支持ReaSnow s1转换器按键（需要串联km_box net，使用km_box_net的键鼠模式下生效）

### 使用说明

运行main.py

### 参与开发说明

#### 文件结构

```
.
├─config                      启动配置文件
│  ├─ref                        运行配置文件
│  └─specs.json                 压枪数据
├─core                          核心代码
│  ├─Config.py                读取配置类
│  ├─KeyAndMouseListner.py      鼠标和键盘监听
│  ├─RecoildsCore.py            压枪数据处理，并与鼠标意图移动交互
│  ├─SelectGun.py               枪械识别
│  ├─ReaSnowSelectGun.py        S1转换器切换宏
│  ├─KmBoxNetListener.py        kmbox net键鼠监听
│  └─ShakeGun.py                抖枪
├─images                      存放各分辨率枪械图色图片
│  ├─1920x1080
│  ├─………………
│  ├─2560x1440
│  ├─hop_up                     存放即用配件图片
│  └─scope                      存放瞄准镜图片
├─log                         打印日志的窗体定义
├─mouse_mover                 各类移动鼠标的实现
└─tools                       各类工具

```

#### 枪械数据开发

脚手架大概已开发完成，原理为：在开镜开枪时记时，当达到time_point时间（豪秒），会根据相同下标寻找x和y，将鼠标移动到相应位置达到压枪的效果。
由于apex特殊性，枪械在不同弹匣容量的情况下，其实是共享弹道的，所以只需要写出一条曲线即可。

对于有畜力的枪械，后续需要在mods中做其他模式的适配（待开发）

主要的工作量体现在调试开枪持续时间和鼠标移动的数据开发。

pint_points是待定属性。

```json
[
  {
    "name": "car",
    "mags": [
      {
        "size": 20,
        "audio": "car_0"
      },
      {
        "size": 22,
        "audio": "car_1"
      },
      {
        "size": 24,
        "audio": "car_2"
      },
      {
        "size": 27,
        "audio": "car_3"
      }
    ],
    "mods": {},
    "time_points": [],
    "x": [],
    "y": [],
    "ping_points": []
  }
]
```