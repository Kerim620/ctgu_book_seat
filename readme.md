# CTGU图书馆预约位置

本脚本实现了自动预约图书馆位置，配合定时任务，每天定时预约。

后续将推出云函数版本，方便各位无服务器同学部署到云端。

脚本开源不收费，如对你有用可以打赏支持我。

<img src="https://gitee.com/zzzjoy/My_Pictures/raw/master/202110282058304.png" alt="img" style="zoom:20%;" />

## Can do what?

1.考研党不用每天在卡卡的系统里着急的选常去位置了，将脚本设置每天运行，你的位置一直属于你。

2.情侣\室友可以一起学习了，本脚本支持多线程同时抢多个邻近的位置，不用担心不在一起学习了。

3.只想要窗边的位置？备选位置满足你，脚本支持无限备选，总抢得到你要的位置！

## How to use?

### 服务器定时任务

1.使用 `git clone https://github.com/zzzjoy-620/ctgu_book_seat.git` 克隆本项目到本地

2.安装依赖 `pip install -r requirements.txt`

3.修改config,py的配置，具体看注释。

4.为book_seat.py设置定时任务，具体自行百度。

### 部署至云函数

**comming soon~**

## Others

本来想在学校的预约网址上套写一套后端项目，用来管理定时任务，通过网页就能新建和取消定时任务，这样就不用每天登录服务器\云函数改配置了
奈何技术不够，暂且写个python脚本吧，等哪天想整了再回来写。

## TODO

**Too much to do...**