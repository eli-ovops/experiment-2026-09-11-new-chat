# Pocket Rove · 原生 Today 摄影棚

本版本使用用户提供且来源已注明的原生Today截图。用户此前拒绝的AI重建Welcome界面没有用于本版本。

## 文件

- `pocket-rove-today-native-2160x3840.png`：4K竖版渲染图。
- `pocket-rove-today-native-2160x3840.blend`：可编辑摄影棚，屏幕素材与字体已打包。
- `assets/today-native-1.6.9-debug.png`：原始PNG逐字节副本，1206×2622。
- `assets/SOURCE-README.md`：用户提供的完整来源说明副本。
- `render_today.py`：以原图替换屏幕并复现渲染的脚本。
- `verification.json`：渲染完成后的核验记录。

## 屏幕内容

原图：
`/Volumes/EXTERNAL/app/EarthOnlineGuide/Marketing/Blender-Native-UI-20260911-142950/02-Today-English-1.6.9-build1-Debug-original.png`

SHA-256：`21788cba5245d011fc3eb464c920410f725c01a94e1c534032052b45f513c861`

App 1.6.9(1)，本地Debug，English，iPhone 17 Simulator / iOS 26.5。截图时间2026-09-10 09:10:53；状态栏09:11。历史采集启用了EARTH_GUIDE_SKY_CAPTURE演示模式：天空任务已揭晓、未完成，其他两条核心任务及Bonus未揭晓。

这是真实App渲染的开发演示画面，不能描述为正式版、1.6.10、自然随机任务或真实用户完成记录。

本版本没有图像生成、界面重绘、文案替换、图标重建、补全或美化。源PNG没有裁切、缩放或重编码；手机屏幕通过标准完整UV映射呈现，随3D镜头产生正常透视与采样，屏幕材质不额外加反光、滤镜或调色。4K是最终摄影棚渲染分辨率，不代表原始屏幕素材新增细节。

## 编辑

打开blend：`SCREEN / native Today PNG`为屏幕；`PHONE / master transform`为手机整体；`TYPE / …`为海报外部文案；`LIGHT / …`为光源。屏幕纹理与外部海报文案独立。

F12渲染，或：

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b pocket-rove-today-native-2160x3840.blend -t 6 --python render_today.py
```

该命令会重新输出同名图片和场景，手动编辑后请先另存新版本。

当前为本地视觉待验收交付，未上传或发布。未操作App、修改数据或源码；用户原始PNG和旧摄影棚保持原样。

## 验收与磁盘记录

已核验最终PNG为2160×3840，场景回读及打包图片SHA-256通过；节点链为原始PNG→Emission(1.0)→Surface。成图已目视检查任务原文、未勾选框、问号、日期、状态栏、底部导航及手机边框。用户视觉验收待定。

本次新交付目录约14MB（源图副本、场景、成图、脚本与说明，2026-09-11生成，依赖于后续编辑，保留）；work/studio-today-native约40KB（渲染与核验日志，同日生成，保留）。内盘可用空间由约6.3GiB降到约1.9GiB，渲染期间最低约1.5GiB；差值未归因，不能等同本任务文件大小。渲染进程已结束，没有继续渲染、清理或删除用户文件。用户拒绝的Welcome重建版本仅在其说明中标记停用。
