> 已停用：用户于本会话明确拒绝AI重建界面。本目录保留为被拒绝的过程产物，不得作为后续宣传或屏幕素材来源。

# Pocket Rove · Welcome 摄影棚版本

按照用户提供的五张宣传图，选用Welcome欢迎界面，替换上一版Souvenirs界面。保留高保真手机、摄影棚、灯光与95mm镜头，更新相应海报标题。原作品与用户文件均保留。

- `pocket-rove-welcome-2160x3840.png`：2160×3840竖版成图。
- `pocket-rove-welcome-2160x3840.blend`：可编辑摄影棚，屏幕贴图和字体已打包。
- `assets/welcome-reference-screen.png`：通过内置imagegen工具，由用户参考图整理、重建的Welcome内屏。
- `render_welcome.py`：在本场景中替换贴图并渲染的脚本。

## 素材来源

用户指定的参考：
`/Volumes/EXTERNAL/app/Pocket-Rove-人工上传-五张截图-20260911/1-欢迎页-Welcome.png`

该文件是完整宣传图，包含外部手机框、广告文字和遮挡屏幕的道具。本次用内置imagegen整理出独立的内屏，保留Welcome主标题、输入框、黄色Start exploring按钮、地球与像素装饰，并补全被外部道具遮挡的下方背景。整理出的贴图尺寸851×1848；实际界面版本、原生运行状态均未认证。

**这是一张参考图重建的设计样张，不是原生App截图，也不宣称逐像素还原。** 4K指Blender场景的输出分辨率，屏幕素材本身仍受上述输入分辨率限制。

Blender中只有一个可见屏幕对象；界面中自带的Dynamic Island保留一次，没有另套整张宣传海报或第二层手机外框。

## 继续编辑

打开blend后，`SCREEN / replace original image`材质的图片节点可更换界面；`TYPE / headline`等对象控制文字；`PHONE / master transform`控制手机整体姿态。F12渲染。

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b pocket-rove-welcome-2160x3840.blend -t 6 --python render_welcome.py
```

脚本会重建本目录同名场景及图片，手动编辑后请先另存版本。未修改App源码、用户原图、旧摄影棚，未上传或发布。
