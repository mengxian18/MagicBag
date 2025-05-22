# Git 操作指南
## 一、快捷配置 Git
git config --global user.name "mengxian"
git config --global user.email "mengxian20@qq.com"

### 1.create
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mengxian18/MagicBag.git
git push -u origin main

### 2.existing
git remote add origin https://github.com/mengxian18/test.git
git branch -M main
git push -u origin main
## 二、本地仓库初始化与代码提交
### 1. 切换到项目目录
进入目标文件夹（示例：D盘项目目录）
cd D:/path/to/your/project
### 2. 初始化本地仓库
git init
### 3. 添加文件到暂存区
git add filename.txt
添加多个文件
git add file1.txt file2.txt
添加当前目录所有文件
git add .
### 4. 提交到本地仓库
git commit -m "描述本次提交内容（例如：Initial commit）"
## 三、关联远程仓库并推送代码
### 场景 1：新建远程仓库后首次推送
关联远程仓库（将URL替换为你的仓库地址）
git remote add origin https://github.com/mengxian18/test.git
切换并创建主分支（GitHub默认分支可能为main）
git branch -M main
推送代码到远程仓库，并关联本地分支
git push -u origin main
### 场景 2：已有本地仓库，关联远程仓库并推送
直接关联远程仓库并推送（适用于非首次初始化的仓库）
git remote add origin https://github.com/mengxian18/test.git
git branch -M main
git push -u origin main
## 四、从远程仓库拉取文件
### 场景 1：克隆全新的远程仓库到本地
克隆完整仓库（默认拉取主分支）
git clone https://github.com/mengxian18/test.git
克隆特定分支（例如dev分支）
git clone -b dev https://github.com/mengxian18/test.git
###  场景 2：更新已有本地仓库
bash
拉取远程仓库指定分支的更新（默认远程名为origin，分支为main）
git pull origin main
若本地分支已跟踪远程分支，直接拉取
git pull
### 场景 3：拉取特定标签（Tag）
克隆仓库并切换到标签v1.0
git clone https://github.com/mengxian18/test.git
cd test
git checkout v1.0

## 五、常见问题与注意事项
远程分支名称问题
若远程仓库默认分支为main（如 GitHub 新建仓库），请使用git push -u origin main而非master。
若提示分支不存在，可先通过git checkout -b main创建本地分支再推送。
冲突解决
拉取代码时若遇冲突，需手动修改冲突文件，标记为已解决后重新提交推送。
仓库地址正确性
确保远程仓库地址（如https://github.com/mengxian18/test.git）正确，避免因 URL 错误导致连接失败。

通过以上步骤，可完成从本地仓库创建到远程协作的全流程操作。如需进一步调试或特定场景支持，请提供更多细节。