# EVE Get MaNei

EVE Get MaNei基于python、open-cv、cnocr、adb等类库

通过大量识图、模拟点击实现eve手游自动挖矿, 且检测蓝加蓝星 拦截 舰船

### 安装说明：
>1.安装python3, 自行百度教程

>2.请手动将脚本文件夹中的 "Polygon"开头的文件中的 两个 "你的py版本" 修改成 你的python版本，通过cmd -> python -V  查看版本，例如：python3.8.x = 38； python3.9.x = 39；python3.10.x = 310

>3.双击主目录下的 '运行一次即可.bat' , 等待依赖库安装完成即可

### 模拟器设置:
>1.目前已知支持的模拟器有雷电、夜神模拟器，<u>原理上，只要支持adb的模拟器均可，可自行百度自己使用的模拟器是否支持adb</u>

>2.请将模拟器分辨率调整为 手机版->540×960，请务必是这个分辨率

### 游戏设置:
>-1.游戏设置-控件缩放比例调整至默认100；；画面设置-性能模式 建议关闭

>0.目前仅支持：所有使用露天的矿船、小鱼

>1.请空间站内运行脚本

>2.请确保  游戏 总览->高级设置->显示分类标签   为勾选

>3.总览使用默认总览；舰船-舰船-全部取消勾选、声望勾选蓝星-驱逐和巡洋，勾选蓝加-驱逐和巡洋；；采矿-天体取消勾选小行星；；天体-天体 只勾选小行星

>4.第一次运行 请将'本地人数列表'移动至游戏左下角后不需要在管

>5.请将本地星系所有的坐标点位全部移除，并为 本地空间站 创建点位

### 脚本设置 & 注意事项:
>1.devices参数设置, ,,有多个模拟器预警机可直接复制以下然后粘贴

    devices = {'kuanggong1': '127.0.0.1:62001','kuanggong2': '127.0.0.1:62002'}

>在确保预警机的模拟器处于运行状态中时，打开cmd  输入adb devices

    C:\Users\sugob\Desktop\evescript\adb_version>adb devices
    List of devices attached
    * daemon not running. starting it now on port 5037 *
    * daemon started successfully *
    127.0.0.1:62001 device

>请复制如 <u>127.0.0.1:62001</u>  的字符串到脚本中对应星系的devices参数中

#### 开启顺序：模拟器 后，进入游戏设置好后，双击 ‘点我运行脚本.bat’即可运行脚本
/

/


作者: Sugobet

QQ: 321355478

脚本开源免费，使用前请先查阅readme.md，有问题请加qq群：924372864



### 感谢使用，觉得好用的话，希望能给个Star


### 捐赠名单 (按时间排序)
<img src="http://a1.qpic.cn/psc?/V12Xu6Mm26x6GL/ruAMsa53pVQWN7FLK88i5jVNuhzjJnHl7ojd6hbq*UE8G0jQ1BzCueV*99qhA275MB5ITIwGAHZqYabkfICXe*lcOd9b*VwaMnJB0Soa3FQ!/c&ek=1&kp=1&pt=0&bo=2gScBtoEnAYDEDU!&tl=1&vuin=1749445382&tm=1660014000&dis_t=1660016830&dis_k=0377483ea5dd3499d7266097d58fe6b3&sce=60-2-2&rf=0-0" width="30%">
<img src="http://a1.qpic.cn/psc?/V12Xu6Mm26x6GL/ruAMsa53pVQWN7FLK88i5jVNuhzjJnHl7ojd6hbq*UHSftihZRfU4QSDMTikpSgT6q9ISwYS*B09oSw*06s7NE0sJdK3DBFo4kowDq5YA4A!/c&ek=1&kp=1&pt=0&bo=OASQBjgEkAYWECA!&t=5&tl=3&vuin=1749445382&tm=1660014000&dis_t=1660016830&dis_k=fd8d61a70b1e3bba2b1a241a0c664653&sce=60-2-2&rf=0-0" width="30%">

>感谢各位老板的捐赠与支持

>1.3v-GEDS死星-海底捞的伟哥空瓶 -> 30RMB ---2022.8.13

>2.3v-GEDS死星-麦克 -> 10RMB ---2022.8.13

>3.3v-GEDS死星-海底捞的伟哥空瓶 -> 30RMB ---2022.8.14

>4.509242333@qq.com -> 50RMB ---2022.8.16
