# Pocket Rove 产品摄影棚 · 首版构图样张

## 文件

- `pocket-rove-studio-1080x1920.png`：1080×1920 竖版渲染图。
- `pocket-rove-studio.blend`：可编辑的 Blender 场景，屏幕贴图和字体已打包。
- `build_studio.py`：可复现建模与渲染脚本。
- `assets/screen-souvenirs-1.6.3.png`：原始截图的副本，未修改屏幕文字与藏品状态。
- `preview*.png` / `studio-preview*.blend`：本任务前两版预览，保留供比较，不是最终交付图。

## 修改方法

在 Blender 打开 `pocket-rove-studio.blend`：

1. `PHONE | rotate or reposition entire device` 控制整部手机的位置与旋转。
2. `SCREEN | replace image texture here` 的材质图片节点用于更换截图。贴图比例为 1206:2622；其他比例需同步调整屏幕几何，避免拉伸。
3. `Brand`、`Headline`、`Subheading`、`Footer left` 为可编辑文字对象。
4. `KEY`、`FILL`、`RIM` 三个灯光可分别调整；`Portrait camera` 为正交摄影机。
5. F12 渲染。首版为 1080×1920、Cycles 64 samples、降噪开启。

也可以通过脚本替换截图并重建场景：

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b -t 6 --python build_studio.py -- --screen /absolute/path/to/screenshot.png
```

注意：脚本重建会重新生成本目录的同名场景和渲染图；如已在 Blender 内手动修改，请先另存为新版本，再重建。脚本不改变 App 源码、模拟器或原素材。

## 素材真实性与验收范围

当前屏幕来自：
`/Volumes/EXTERNAL/app/EarthOnlineGuide/Marketing/PocketRove-UI-1.6.3-b1-20260909/04-souvenirs-original.png`

原素材索引记载：2026-09-09，Pocket Rove 1.6.3(1)，iPhone 17 Simulator，1206×2622；属于开发预览，不是已认证的当前 App Store 版本。背包和茶杯为原截图中的已解锁状态，其他灰色藏品保持原样。既有 QA 数据的最初来源及完整运行 flags 未全部核实。

本交付用于摄影棚构图与风格验收。正式宣传前应换成目标正式版本、同语言的确认截图。文案为本次拟定草稿。深绿色手机为自建通用设备外形，不声称精确复刻某一 iPhone 型号。未上传 App Store、未发布广告。

## 安装与渲染

Blender 4.5.13 LTS，macOS arm64，安装于 `/Applications/Blender.app`。
官方来源：https://download.blender.org/release/Blender4.5/blender-4.5.13-macos-arm64.dmg
官方 SHA-256 清单：https://download.blender.org/release/Blender4.5/blender-4.5.13.sha256

安装包 SHA-256 比对通过；codesign 深度严格校验通过；spctl 返回 `accepted / Notarized Developer ID`；命令行启动及实际 Cycles 渲染通过。未安装第三方 MCP、插件、依赖或付费素材。

## 本任务磁盘记录（2026-09-11）

内置盘可用空间：任务前约17 GiB，任务后约15 GiB（df四舍五入；其他并行活动可能影响差值）。未删除任何文件。仅检查本任务新增目录。

| 路径 | 大小 | 时间 | 来源、用途与依赖 | 保留/可释空间 |
| --- | --- | --- | --- | --- |
| `/Applications/Blender.app` | 814 MB | 包内mtime 2026-08-25 09:31；本次安装2026-09-11 | 官方签名应用；编辑、渲染必需 | 保留；删除会失去运行环境 |
| `../../work/blender-install/` | 305 MB | 安装包下载2026-09-11 13:58 | 官方DMG、SHA清单和API参考；复装/核验使用 | 不影响已安装应用运行；经用户批准清理可释约305 MB，当前保留 |
| 当前交付目录 | 24 MB | 主场景2026-09-11 14:03 | 自建场景、原图副本、预览、最终图和脚本 | 保留；为可编辑交付及迭代依据 |

安装镜像已正常卸载。未清理系统、其他项目、缓存或未知文件。
