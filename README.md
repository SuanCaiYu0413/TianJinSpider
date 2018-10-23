# TianJinSpider
天津房产网的分布式爬虫

***

# 使用说明

整个项目包含队列管理和worker

队列管理脚本只需要开启一个

worker可以开启多个

```bash

git clone https://github.com/SuanCaiYu0413/TianJinSpider.git


cd TianJinSpider

pip3 install requirements.txt

# master端

python QueueManage.py

# worker端

python worker.py

```