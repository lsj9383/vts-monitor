# VTS Monitor
[VTS](https://github.com/vozlt/nginx-module-vts)是一个Nginx第三方模块，可以统计到Nginx的流量、key的触发次数、集群的健康状态。该模块只提供了全量的统计，即从统计开始到当前时刻的所有数据。当希望获得服务的QPS、不同时间的服务器状态分布情况时，VTS就无能为力。`VTS Monitor`提供一个通用化方案，在一个VTS可用的情况下，通过简单的配置，就能获得服务器在不同时间的状态。

* 特征
    * 统计每分钟的接口调用次数
    * 获得指定某天的接口调用次数的时间分布, 粒度(天)

## 一、部署
### 1.环境及依赖:
* Linux
* Python3.x
* pip

### 2.虚拟环境初始化
```sh
$ virtualenv --no-site-packages venv
$ source venv/bin/activate

# 在虚拟环境中安装依赖关系
(venv)$ pip install -r requirements.txt

# 退出虚拟环境
(venv)$ deactive
```

### 3.数据源更新脚本
接口调用的数据需要每分钟到vts进行获取和更新，以计算每个时间段的调用情况:
```sh
# 进行一次的数据源更新
(venv)$ cd update
(venv)$ python update_shelve.py

# 通过crontab进行定期触发
$ crontab -e

* * * * * cd <脚本路径> && <虚拟环境的python解释器> update_shelve.py
```

## 二、使用

## 三、原理