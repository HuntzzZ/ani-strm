<div align="center">

# Ani-Strm

**一个为 Emby、Jellyfin 服务器提供直链播放的小脚本** 


[关于脚本](#关于脚本) •
[关于Strm](#关于Strm) •
[脚本使用指南](#脚本使用指南) •
[注意事项](#注意事项) •
[TODO LIST](#todo-list) •
[更新日志](#更新日志) •
[特别感谢](#特别感谢)

</div>

<div align="center">
	<img src="./images/emby.png" width="1000px">
</div>

## 关于脚本
- 本项目是一款专为Strm文件处理而设计的 Python 脚本工具集，写本脚本的初衷为实现代替手动生成strm文件供给emby的读取，脚本从原理上来讲适用于一切能取得视频文件直链的方式，但由于本脚本的主要目的是满足本人处理Ani Open项目的番剧地址，故而命名仅仅适配了Ani Open的命名格式。若您由其他命名格式的处理需求可提出issue。
- 本脚本为了应付命名规范与否保留了两版，strm版本仅仅能够处理**output.txt** 内编辑而来的直链地址，txt内的每行的内容写成strm文件，ani_strm.py版本能处理符合命名规范的地址，用户可依特定格式输入视频地址示例及所需生成行数，脚本便能精准创建包含递增集数的多个视频地址，并写入**output.txt**文件。
- 本脚本已在群晖、Debian环境下测试通过。

## 关于Strm


## 脚本使用指南

### 当使用ani-strm.py版本时
一、 把”ani-strm.py“下载下来，导入到你想放的文件夹里面。

二、使用ssh命令cd到ani_strm.py存放的目录，执行 chmod +x ani_strm.py
```
cd /path/ #path为ani-strm.py的存放目录
chmod +x ani-strm.py #调整ani-strm.py的文件权限
```
三、执行./ani_strm.py，按照提示输入Ani open项目内你需要制作strm文件番剧的第一个地址，格式如下：
```
https://openani.an-i.workers.dev/2022-10/BLEACH%20%E6%AD%BB%E7%A5%9E%20%E5%8D%83%E5%B9%B4%E8%A1%80%E6%88%B0%E7%AF%87/%5BANi%5D%20BLEACH%20%E6%AD%BB%E7%A5%9E%20%E5%8D%83%E5%B9%B4%E8%A1%80%E6%88%B0%E7%AF%87%20-%2001%20%5B1080P%5D%5BBaha%5D%5BWEB-DL%5D%5BAAC%20AVC%5D%5BCHT%5D.mp4?a=view
或者
https://openani.an-i.workers.dev/2022-10/BLEACH 死神 千年血戰篇/[ANi] BLEACH 死神 千年血戰篇 - 01 [1080P][Baha][WEB-DL][AAC AVC][CHT].mp4?d=true
或者
https://openani.an-i.workers.dev/2022-10/BLEACH 死神 千年血戰篇/[ANi] BLEACH 死神 千年血戰篇 - 01 [1080P][Baha][WEB-DL][AAC AVC][CHT].mp4?a=view
```
四、按照提示脚本提示生成output.txt文件，确认内容无误后生成strm文件，请自行确认strm文件内的地址有效性。

五、推荐将生成后的strm文件交由Moviepilot整理刮削转移，转移方式推荐复制。

六、推荐使用Emby新插件：StrmAssistant（STRM助手）地址：https://github.com/sjtuross/StrmAssistant
<div align="center">
	<img src="./images/ani_strm.py.png" width="1000px">
</div>

### 当使用strm.py版本时
一、 把”strm.py“下载下来，导入到你想放的文件夹里面。

二、使用ssh命令cd到strm.py存放的目录，执行 chmod +x strm.py
```
cd /path/ #path为strm.py的存放目录
chmod +x strm.py #调整strm.py的文件权限
```
三、执行./strm.py,执行后会提示未找到 input_video_urls.txt 文件，将创建该文件，请自行编辑input_video_urls.txt后重新运行脚本，脚本将直接按照txt内的文本每行的内容写成strm文件。
```
./strm.py
```
四、推荐将生成后的strm文件交由Moviepilot整理刮削转移，转移方式推荐复制。

五、推荐使用Emby新插件：StrmAssistant（STRM助手）地址：https://github.com/sjtuross/StrmAssistant
## 注意事项
### （一）输入格式准确性
严格依要求格式输入视频地址示例，确保方括号、尖括号、中文字符、集数格式（如 01）及文件扩展名等元素准确，错误格式或致处理异常。

### （二）文件编码兼容性
虽脚本尝试多种编码读取 `output.txt`，仍建议保存文件时优先选常见编码（`utf-8`）。若处理非标准编码文件报错，检查编码设置或手动转换格式后再处理。

### （三）链接校验限制
链接校验依赖网络连接与目标服务器响应。网络故障、服务器限制或地址过期可致校验误判或超时，必要时手动检查地址可用性或调整校验策略。

### （四）日志文件管理
脚本按日期生成日志文件（`script_YYYYMMDD.log`），长期运行累积大量日志占用空间，建议定期清理或备份旧日志，依日志排查问题时留意对应日期文件。 

### （五）脚本权限设置与执行
文件权限调整：赋予脚本执行权限，在终端进入脚本所在目录，执行 chmod +x strm.py，使所有者、组及其他用户有执行权，方便从任何目录运行脚本，命令为 ./strm.py

### （六）关于Emby播放异常
- 由于Ani Open的访问需要科学环境，请检查emby服务器是否具备科学能力。
- 部分反向代理的地址可能会导致连不通，请使用原IP:8096或8920的方法访问。


## TODO LIST
- [x] 从地址提取文件名，过滤非法字符后创建 `.strm` 文件并写入对应地址行，记录创建日志（含耗时）
- [x] 脚本读取并解码 `output.txt` 内容，处理每行地址格式后，依番名在当前目录创建子目录分类存储 `.strm` 文件
- [ ] 采用多编码尝试机制（如 utf-8、gbk、latin-1）读取文件，有效规避编码错误困扰，确保不同编码格式的 output.txt 文件皆能准确处理，增强脚本通用性与适应性

## 更新日志
- 2024.11.27：v1.0，创建粗糙的项目

## 特别感谢
- [Ani Open项目](https://openani.an-i.workers.dev/)
- [StrmAssistant](https://github.com/sjtuross/StrmAssistant)
