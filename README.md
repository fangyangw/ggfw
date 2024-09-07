# 使用说明
## 安装依赖
python -m pip install selenium
## 安装浏览器驱动
先查看自己的浏览器版本，在下载地址：https://registry.npmmirror.com/binary.html?path=chrome-for-testing/中找到对应版本，前三位版本号匹配即可

将下载的包解压到项目目录的chromedriver-win64目录下

## 运行方法
执行：python main.py
执行后会弹出登录页面，请手动登录，并进入到课程列表页面(例如：https://ggfw.hrss.gd.gov.cn/zxpx/hyper/courseDetail?ocid=OC202404290000005581）
保证该列表页面在第一个标签页，等待即可
