# 开发简易思路

1.暂不考虑激光采矿（可实现）

2.仅使用于露天矿船、小鱼

3.根据左上角-装配-舰船名字来识别现所驾驶的舰船，后进行对应型号舰船的操作

4.判断是否在空间站堡垒中或外太空

5.自动切换总览 矿区 优先级  集群 > 星群 > 星带

5.1 自动切换总览至  '舰船'  并挖矿全程检测总览有无 ‘蓝加’ 拦截舰

5.2 发现蓝加拦截舰立即截图保留证据，并且尝试激活所有指定装备返回空间站堡垒，如果超时则向游戏指定频道模拟真人发送求救信息

6.全程检测本地红白总数大于1，立即激活所有指定装备返回空间站堡垒， 或待在空间站堡垒不出站

-----------------------------挖矿细节-------------------------------

1.进入矿区后自动开启所需开启的装备 如露天、采矿无人机、主动防御装备等

2.集群、星群自动拉距离

3.检测左上方仓库占用率 大于99%时，激活所有指定装备返回空间站堡垒

4.经上一步后，自动将舰船矿石仓所有矿石移动至 物品仓库，后关闭仓库

5.脚本循环

-------------------------------其他细节------------------------------

1.外太空中按需检测舰船 血量条信息上方的‘动作信息’， 如：准备跃迁、跃迁至、舰船正在停止等细节信息以用于程序判断

2.防检测机制如：自动打开商城浏览、自动查看仓库、自动打开聊天框聊天等


