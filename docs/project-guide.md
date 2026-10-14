# 初学者项目实操指南

这份指南配合[产品需求文档](product-requirements.md)使用。当前目录还没有 `.git`，也没有应用源码；下面从建仓库开始。命令示例使用 Windows PowerShell。你亲自输入 Git 命令、推送分支，并在 GitHub 网页上创建和合并 PR。Python + Kivy、本地 TXT 和仅本地存储已经由你确认；各阶段的具体实现选型仍需逐项确认。

如果开发中遇到会改变需求、数据或项目结构的问题，先记录现象和可选做法，请你确认后再改。每个里程碑开始前，先说明要新增的技术或依赖、至少一个可行替代及取舍，得到你的选择后执行。普通编译错误和已确认方案内的小修复可以直接处理，并在 PR 中说明。

## 0. 先认识四个位置

| 位置 | 含义 | 常见操作 |
| --- | --- | --- |
| 工作区 | 电脑上正在编辑的文件 | 写代码、改文档、运行应用 |
| 暂存区 | 本次准备提交的改动 | `git add` |
| 本地仓库 | 电脑上的提交历史 | `git commit`、切换分支 |
| GitHub 远程仓库 | GitHub 网站上的历史和 PR | `git push`、创建 PR |

`git pull` 把远程分支更新到本地当前分支；`git push` 把本地提交发送到远程；PR 是请求把一个分支的提交合并到另一个分支。三者是不同动作。

## 1. 准备工具与账号

1. 安装 [Git for Windows](https://git-scm.com/download/win)，注册或登录 [GitHub](https://github.com/)。本机已检测到 Python 3.12.7，可先用它创建项目虚拟环境；Kivy 2.3.1 官方支持 Python 3.8–3.13。如果你的终端找不到 Python，再安装 [Python 3.12](https://www.python.org/downloads/) 并重新打开终端。
2. 打开 PowerShell，逐条确认：

   ```powershell
   git --version
   git config --global user.name "你的 GitHub 显示名"
   git config --global user.email "你的提交邮箱"
   git config --global --get user.name
   git config --global --get user.email
   python --version
   Get-Command python
   ```

3. 第一次通过 HTTPS 推送时，按 Git 弹出的登录流程完成 GitHub 身份验证。不要把密码或令牌写进项目文件。
4. 本阶段只需 Git、Python 和 GitHub。Windows 上运行 Kivy 窗口不需要先安装 Android Studio。到 M2 制作 APK 时，再按确认的打包方案准备 WSL2、Buildozer 和安卓测试设备。

## 2. 创建 GitHub 仓库并上传这批文档（M0）

本地路径是 `D:\develop\github\e_read_tool`。在 GitHub 网页点击右上角 **New repository**，仓库名建议 `e_read_tool`。创建时不要勾选 README、`.gitignore` 或 license，因为本地已有 README；这样两端的初始历史一致。记下页面提供的 HTTPS 地址，形如 `https://github.com/你的用户名/e_read_tool.git`。

在 PowerShell 中进入项目目录，逐条运行：

```powershell
cd D:\develop\github\e_read_tool
git init -b main
git status
git add README.md docs/product-requirements.md docs/project-guide.md .gitignore requirements.txt
git diff --cached --stat
git commit -m "docs: plan Android novel reader project"
git remote add origin https://github.com/你的用户名/e_read_tool.git
git remote -v
git push -u origin main
```

把示例 URL 中的用户名换成自己的。看到 GitHub 仓库首页出现 README 和 `docs/`，M0 就完成了。此时只有 `main` 一个分支，尚无可供比较的第二分支；从 M1 开始练习 PR。

> 如果 `git init -b main` 提示不支持该选项，可改用 `git init`，再执行 `git branch -M main`。如果 `git commit` 要求身份信息，回到第 1 节设置用户名和邮箱。

## 3. 在项目里创建虚拟环境并启动 Kivy（M1）

虚拟环境是放在项目里的独立 Python 包目录。它让这个项目使用自己的 Kivy 依赖。`.venv/` 已写入根目录 `.gitignore`，所以虚拟环境不会上传到 GitHub；其他人可根据 `requirements.txt` 重新安装。

先在干净的 `main` 上拉取远程更新，并创建本阶段的分支。此时尚未创建应用文件，所以 `git status` 应显示没有待提交改动：

```powershell
cd D:\develop\github\e_read_tool
git switch main
git status
git pull --ff-only origin main
git switch -c feature/m1-kivy-starter
```

`--ff-only` 会在无法直接前进时停下来，便于先检查历史，不会自动产生额外合并提交。

在项目根目录的 PowerShell 中逐条输入：

```powershell
cd D:\develop\github\e_read_tool
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip --version
python -m pip install -r requirements.txt
python -c "import sys, kivy; print(sys.executable); print(kivy.__version__)"
```

看到命令行前面出现 `(.venv)`，并且最后一条命令打印的 Python 路径位于项目的 `.venv` 下、Kivy 版本为 `2.3.1`，说明环境准备成功。若 PowerShell 阻止运行 `Activate.ps1`，可先在当前终端运行 `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`，再重新激活；该设置只影响当前 PowerShell 进程。也可以不激活，直接使用 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` 和 `.\.venv\Scripts\python.exe main.py`。

每次打开一个新的 PowerShell 终端，进入项目目录后都需要再次运行 `.\.venv\Scripts\Activate.ps1`。工作结束时输入 `deactivate`，即可退出虚拟环境。不要把 `.venv/` 加入 Git。

M1 编码时，在仓库根目录创建 `main.py`，先做可启动的 Kivy 窗口，再做书架空状态。每完成一步，用 `python main.py` 在 Windows 上运行；窗口正常出现且关闭后进程退出，M1 才算通过。此时先验证桌面原型，安卓设备验证安排在 M2 的首次 APK 中。

`requirements.txt` 当前只列 `kivy[base]==2.3.1`。TXT 解码、路径处理、JSON 和 SQLite 都能使用 Python 标准库；安卓文件选择可能需要平台桥接依赖，M2 确认具体方案后再添加。Windows 的 `.venv` 只供本机开发，Buildozer 需要单独的 Linux 环境，不能把此 `.venv` 复制进去用于 APK 构建。

### 需要安装哪些东西

| 何时需要 | 工具或依赖 | 用途 |
| --- | --- | --- |
| 现在 | Python 3.12.7（本机已有）、Git、`requirements.txt` 中的 Kivy 2.3.1 | 建立虚拟环境、运行 Windows 版原型、管理代码 |
| M2 安卓打包前 | WSL2 与 Linux 发行版、Buildozer（若确认此方案）、Linux 系统构建依赖和 JDK | 在 Windows 电脑上构建安卓 APK；具体安装命令随发行版版本确认 |
| M2 测试时 | 安卓真机或模拟器；安装 APK 可用 ADB，若需要模拟器可安装 Android Studio | 检查手机上的文件选择、中文显示、阅读和进度 |

Kivy 官方推荐新手用 Buildozer 自动化安卓打包。它在 Windows 上需要 WSL2，并建议在 WSL 的 Linux 文件系统中构建；首次构建会下载 Android SDK、NDK 等工具。另一方案是直接使用 python-for-android，配置步骤更多。进入 M2 时，我会先给你两种方案的实际安装步骤和取舍，等你确认再执行。Windows 的 `.venv` 与 WSL 中的 Python 环境各自独立。

## 4. 每个里程碑都亲自走一遍 Git/PR 流程

M1 已在上一节创建分支。完成该阶段的编码与测试后，回到仓库根目录检查并提交：

```powershell
cd D:\develop\github\e_read_tool
git status --short
git diff
git add -A
git diff --cached --stat
git diff --cached
git commit -m "feat: create Kivy starter app"
git push -u origin feature/m1-kivy-starter
```

`git add -A` 前务必确认没有密钥、私人小说、`.venv/` 或构建产物。`git diff --cached` 是最后一次查看将提交内容的机会。

打开 GitHub 仓库页面，点击 **Compare & pull request**（或 **Pull requests → New pull request**）。确认 **base: main**、**compare: feature/m1-kivy-starter**，填写标题与说明，再点击 **Create pull request**。PR 说明建议包含：实现了什么、怎样验证、截图或已知问题。查看 **Files changed**，检查提交范围；确认后在网页点击 **Merge pull request**。这一步也由你操作。

合并后为下一阶段做准备：

```powershell
git switch main
git pull --ff-only origin main
git status
git switch -c feature/m2-import-bookshelf
```

后续分支建议依次用 `feature/m2-import-bookshelf`、`feature/m3-reader-progress`、`feature/m4-settings-delete`、`docs/m5-release-notes`。每个阶段重复“开发 → 运行与验收 → 查看差异 → commit → push → PR → 合并 → pull”。M2 开始前先确认安卓打包环境与文件选择实现方案。

## 5. 各阶段该做什么

| 阶段 | 编码练习 | 交给自己检查的结果 |
| --- | --- | --- |
| M1 | `.venv`、Kivy 窗口、书架空状态 | Windows 上运行 `python main.py`，窗口正常出现 |
| M2 | 首个安卓 APK、手机文件选择与导入、书架；打包和存储方案待确认 | 安卓设备可启动；中文 TXT 导入成功，错误文件有提示 |
| M3 | 段落解析、按需渲染、位置保存与恢复 | 滚动、退出、重启后回到原段落附近 |
| M4 | 设置持久化、主题与字号、删除确认；存储方案待确认 | 设置重启后保留；删除不影响原文件；飞行模式可用 |
| M5 | 整理 README、手测记录、构建 APK | 从 README 能看到运行方法、截图和已知限制；验收表全部通过 |

具体动手顺序：

1. **M2**：先确认 Buildozer/WSL2 打包环境、手机文件选择与本地数据方案；制作首个可安装 APK，尽早在安卓设备验证启动。再做书架列表、文件选择、编码与大小检查、失败清理。Windows 上调试界面，安卓设备上验收文件导入，因为两种系统的文件访问方式可能不同。
2. **M3**：先用短 TXT 做段落解析和纵向滚动；再把真实书籍内容接入阅读页；保存位置时记录书籍 ID、段落索引及偏移，离开和重新打开各测一次；最后用较长 TXT 检查性能。这里适合学习状态与持久化。
3. **M4**：先确认设置存储方案；做字号与主题的界面反馈，再按确认的方案持久化；接着做书架删除菜单、确认弹窗、文件与数据清理；最后开启飞行模式完整操作一次。
4. **M5**：逐项勾选需求文档 F01–F08；在 README 补充运行步骤、截图和已知限制；用确认的 Buildozer 配置重新构建安卓 APK。Buildozer 输出通常在项目的 `bin/` 目录，检查实际文件后再安装到测试设备。

每一阶段先读需求表中对应的 F 编号，写下最小可运行版本，再增加异常处理。一次 PR 尽量只围绕一个里程碑，方便你在 **Files changed** 中理解每一处改动。每完成一个小步骤就运行应用，出错时更容易定位。

## 6. 手工验收记录模板

在每个 PR 的描述里可以复制以下内容并填写：

```markdown
## 本次实现
- 

## 我亲自验证了
- [ ] 模拟器或真机可以启动
- [ ] 本阶段的正常流程通过
- [ ] 本阶段的失败/边界情况有合理提示
- [ ] 已检查 git diff 和 Files changed

## 测试环境
- Android 版本：
- 设备或模拟器：

## 已知问题
- 无 / 具体问题：
```

M5 再做一次完整验收：普通 UTF-8 文件、带 BOM 文件、GB18030 文件、空文件、超过上限的文件、非 TXT 文件；退出重开后的进度；不同字号和主题；删除前取消与确认；飞行模式阅读。测试小说尽量用自己编写或可合法分发的样文，不要把私人或受版权限制的小说提交到 GitHub。

## 7. 常见问题

| 情况 | 先检查什么 | 下一步 |
| --- | --- | --- |
| `git pull --ff-only` 失败 | `git status` 是否干净；`git log --oneline --graph --all -10` 看分支历史 | 先弄清本地是否有未推送提交；不要直接强推或重置 |
| `git push` 提示身份验证失败 | 远程 URL `git remote -v`；GitHub 登录弹窗 | 按 Git Credential Manager 的流程重新登录 |
| PR 按钮没有出现 | 分支是否已 push；base/compare 是否不同 | 在 **Pull requests → New pull request** 手动选分支 |
| `python -m venv .venv` 失败 | `python --version` 和 `Get-Command python`；确认 Python 版本在支持范围内 | 记录完整报错；必要时安装官方 Python 3.12 后重试 |
| `Activate.ps1` 被阻止 | PowerShell 的执行策略错误提示 | 按第 3 节使用当前进程临时设置，或直接调用 `.venv` 中的 `python.exe` |
| `pip install` 找不到 Kivy wheel | Python 版本、Windows 架构、完整 pip 报错 | 先核对 Kivy 官方支持范围，不要盲目安装开发版 |
| `UnicodeDecodeError: 'gbk'` 出现在安装依赖时 | 检查 `requirements.txt` 是否含有当前终端编码无法读取的字符 | 保持依赖文件为纯英文/ASCII 文本，再运行 `python -m pip install -r requirements.txt` |
| Buildozer 构建失败 | 是否在 WSL2 的 Linux 文件系统构建、Buildozer 完整日志 | 依据首个具体错误及官方安装说明处理；不要把 Windows `.venv` 复制进去 |
| APK 能安装但导入乱码 | 文件编码是否与导入时所选一致 | 用 GB18030 重新导入；保存可复现的非版权测试样本 |

遇到问题时，记录“执行了哪一步、完整报错、`git status` 输出、Python/Kivy 版本”，再求助。不要在求助信息中粘贴访问令牌或私人书籍内容。

## 官方参考

- [GitHub：创建新仓库](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub：从远程仓库获取更新](https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository)
- [GitHub：创建 Pull Request](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
- [Python：创建和激活虚拟环境](https://docs.python.org/3/library/venv.html)
- [Kivy：安装、支持的 Python 版本与依赖](https://kivy.org/doc/stable/gettingstarted/installation.html)
- [Kivy：打包安卓应用](https://kivy.org/doc/stable/guide/packaging-android.html)
- [Buildozer：Windows/WSL2 安装要求](https://buildozer.readthedocs.io/en/latest/installation/)
- [Buildozer：生成 APK 的基本流程](https://buildozer.readthedocs.io/en/1.6.0/quickstart/)

