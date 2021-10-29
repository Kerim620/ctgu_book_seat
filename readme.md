# CTGU图书馆预约位置

本脚本实现了自动预约图书馆位置，配合定时任务，每天定时预约。

~~后续将推出云函数版本，方便各位无服务器同学部署到云端。~~
已推出云函数版本，可自行部署至云端！

## :sparkles:Can do what?

1.考研党不用每天在卡卡的系统里着急的选常去位置了，将脚本设置每天运行，你的位置一直属于你。

2.情侣\室友可以一起学习了，本脚本支持多线程同时抢多个邻近的位置，不用担心不在一起学习了。

3.只想要窗边的位置？备选位置满足你，脚本支持无限备选，总抢得到你要的位置！

## :rocket:How to use?

### 服务器定时任务
1.使用 `git clone https://github.com/zzzjoy-620/ctgu_book_seat.git` 克隆本项目到本地。

2.安装依赖 `pip install -r requirements.txt`。

3.修改config.py的配置，具体看注释。

4.为book_seat.py设置定时任务，具体自行百度。

### 部署至云函数(new~)

1.[注册腾讯云函数](https://console.cloud.tencent.com/)，[新建python空白函数](https://console.cloud.tencent.com/scf/list-create?rid=4&ns=default&keyword=helloworld%20%E7%A9%BA%E7%99%BD%E6%A8%A1%E6%9D%BF%E5%87%BD%E6%95%B0&python3)，直接下一步。

2.配置「函数代码」。复制本项目的 [index.py](https://github.com/zzzjoy-620/ctgu_book_seat/blob/master/index.py) 文件至函数代码栏里。

![image-20211029072424918](https://gitee.com/zzzjoy/My_Pictures/raw/master/202110290724038.png)

3.修改自己的配置。在上一步代码的末尾是相关配置，根据注释说明自行配置。

4.修改「高级配置」。将函数超时时间修改为900秒。	

![image-20211029072601406](https://gitee.com/zzzjoy/My_Pictures/raw/master/202110290726461.png)

5.配置「触发器配置」。将触发方式修改为定时触发，cron表达式为 `45 30 6 * * * *`，代表每天6:30:45运行脚本。

![image-20211029080949163](https://gitee.com/zzzjoy/My_Pictures/raw/master/202110290809230.png)

6.部署完成，可以试试点击右边的 测试 进行测试，在左侧的 日志查询 中查看结果。

![image-20211029073944915](https://gitee.com/zzzjoy/My_Pictures/raw/master/202110290739053.png)



## :memo:Others

本来想在学校的预约网址上套写一套后端项目，用来管理定时任务，通过网页就能新建和取消定时任务，这样就不用每天登录服务器\云函数改配置了
奈何技术不够，暂且写个python脚本吧，等哪天想整了再回来写。

奥对了，这个项目对你有用的话，欢迎打赏我，支持用爱发电。

![image-20211028210639165](https://gitee.com/zzzjoy/My_Pictures/raw/master/202110282106213.png)

免责声明：该项目仅用于交流学习，对使用者不负责任，请勿用于二次收费。

## :see_no_evil:TODO

**To much to do...**
