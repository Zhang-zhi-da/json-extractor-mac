#!/usr/bin/env bash
# macOS 打包脚本：把 json_extractor_ui.py 打包成 .app 应用程序
#
# 使用方式（在 macOS 的“终端”里执行）：
#   cd 本目录
#   chmod +x build_mac.sh
#   ./build_mac.sh
#
# 可选环境变量：
#   PYTHON_BIN=python3.11   指定解释器（建议用 python.org 官方 framework 版，Tcl/Tk 最完整）
#   TARGET_ARCH=arm64       x86_64 / arm64 / universal2，默认跟随当前机器
#
# 产物：dist/JSON数据提取工具.app

set -euo pipefail

APP_NAME="JSON数据提取工具"
ENTRY="json_extractor_ui.py"
BUNDLE_ID="com.local.jsonextractor"
PYTHON_BIN="${PYTHON_BIN:-python3}"
TARGET_ARCH="${TARGET_ARCH:-}"

echo "==> 1/5 检查 tkinter（无 GUI 支持的 Python 打出来的 App 会闪退）"
"$PYTHON_BIN" -c "import tkinter, sys; print('tkinter OK, Tcl/Tk =', tkinter.TclVersion)"

echo "==> 2/5 创建虚拟环境并安装依赖"
"$PYTHON_BIN" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "==> 3/5 清理旧构建"
rm -rf build dist ./*.spec

echo "==> 4/5 PyInstaller 打包"
PYI_ARGS=(
  --noconfirm
  --clean
  --windowed          # macOS 上会自动生成 .app 包，不弹终端窗口
  --onedir            # 目录模式，启动快；若想单文件可改成 --onefile
  --name "$APP_NAME"
  --osx-bundle-identifier "$BUNDLE_ID"
  --hidden-import pandas
  --hidden-import openpyxl
  --collect-submodules openpyxl   # to_excel(engine='openpyxl') 是动态导入，必须强制收集
)
if [ -n "$TARGET_ARCH" ]; then
  PYI_ARGS+=(--target-arch "$TARGET_ARCH")
fi
PYI_ARGS+=("$ENTRY")

pyinstaller "${PYI_ARGS[@]}"

echo "==> 5/5 去除隔离属性并做 ad-hoc 签名（避免提示“文件已损坏”）"
APP_PATH="dist/${APP_NAME}.app"
xattr -cr "$APP_PATH"
codesign --force --deep --sign - "$APP_PATH"

echo
echo "打包完成：$(pwd)/$APP_PATH"
echo "双击即可运行；要分发给别人，可把 .app 打成 zip 或 dmg。"
