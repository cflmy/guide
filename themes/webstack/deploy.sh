#!/bin/bash 

# 部署脚本：将public文件夹作为单独的public分支推送到远程存储库 

# 配置参数 
BUILD_DIR="public" 
BRANCH_NAME="public" 
REMOTE_NAME="origin" 

# 确保脚本健壮性的函数 
function error_exit { 
    echo "错误: $1" >&2 
    popd > /dev/null 2>&1 || true 
    exit 1 
} 

# 检查public文件夹是否存在 
if [ ! -d "$BUILD_DIR" ]; then 
    error_exit "public文件夹不存在" 
fi 

# 检查是否在git仓库中 
if [ ! -d ".git" ]; then 
    error_exit "当前目录不是git仓库，请在有效的git仓库中运行此脚本" 
fi 

# 获取主仓库的远程URL 
MAIN_REMOTE_URL=$(git config --get remote."$REMOTE_NAME".url) 
if [ -z "$MAIN_REMOTE_URL" ]; then 
    error_exit "无法获取当前git仓库的远程URL，请确保$REMOTE_NAME远程已配置" 
fi 

# 记录当前目录 
ORIGINAL_DIR="$(pwd)" 

# 进入public目录 
cd "$BUILD_DIR" || error_exit "无法进入public目录" 

# 初始化git（如果需要） 
if [ ! -d ".git" ]; then 
    git init || error_exit "初始化git失败" 
    echo "已在public目录初始化git仓库" 
    
    # 使用主仓库的远程URL 
    git remote add "$REMOTE_NAME" "$MAIN_REMOTE_URL" || error_exit "添加远程仓库失败" 
    echo "已添加远程仓库: $MAIN_REMOTE_URL" 
else 
    # 检查远程仓库是否存在且URL是否匹配 
    EXISTING_REMOTE_URL=$(git config --get remote."$REMOTE_NAME".url 2>/dev/null) 
    if [ -z "$EXISTING_REMOTE_URL" ]; then 
        # 添加远程仓库 
        git remote add "$REMOTE_NAME" "$MAIN_REMOTE_URL" || error_exit "添加远程仓库失败" 
        echo "已添加远程仓库: $MAIN_REMOTE_URL" 
    elif [ "$EXISTING_REMOTE_URL" != "$MAIN_REMOTE_URL" ]; then 
        # 更新远程仓库URL 
        git remote set-url "$REMOTE_NAME" "$MAIN_REMOTE_URL" || error_exit "更新远程仓库URL失败" 
        echo "已更新远程仓库URL为: $MAIN_REMOTE_URL" 
    fi 
    
    # 拉取最新更改（如果存在） 
    if git ls-remote --exit-code --heads "$REMOTE_NAME" "$BRANCH_NAME" >/dev/null 2>&1; then 
        echo "正在拉取远程$BRANCH_NAME分支的最新更改..." 
        git fetch "$REMOTE_NAME" "$BRANCH_NAME" || error_exit "拉取远程分支失败" 
        git checkout -B "$BRANCH_NAME" "$REMOTE_NAME/$BRANCH_NAME" || error_exit "切换到远程分支失败" 
    fi 
fi 

# 检查当前是否已在正确的分支上 
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null) 
if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then 
    echo "当前已在$BRANCH_NAME分支上" 
else 
    # 尝试切换到已有的分支，如果不存在则创建 
    git checkout "$BRANCH_NAME" 2>/dev/null || git checkout -b "$BRANCH_NAME" 
    if [ $? -ne 0 ]; then 
        error_exit "切换或创建$BRANCH_NAME分支失败" 
    fi 
fi 

# 添加所有文件 
git add . || error_exit "添加文件失败" 

# 提交更改 
COMMIT_MESSAGE="Update public at $(date '+%Y-%m-%d %H:%M:%S')" 
git commit -m "$COMMIT_MESSAGE" || { 
    # 如果没有更改，继续执行 
    if [ $? -eq 1 ]; then 
        echo "没有更改需要提交" 
    else 
        error_exit "提交更改失败" 
    fi 
} 

# 推送更改到远程仓库 
echo "正在推送$BRANCH_NAME分支到远程仓库..." 
git push -u "$REMOTE_NAME" "$BRANCH_NAME" -f || error_exit "推送失败" 

# 返回原始目录 
cd "$ORIGINAL_DIR" || error_exit "无法返回原始目录" 

echo "成功: public文件夹已作为$BRANCH_NAME分支推送到远程仓库" 
exit 0
\