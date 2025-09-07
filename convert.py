import yaml
import os
import shutil
import yaml

# 确保public文件夹存在
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 复制文件到目标目录
def copy_file(source, destination):
    if os.path.exists(source):
        shutil.copy2(source, destination)
        print(f"已复制: {source} -> {destination}")

# 读取模板文件
def read_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# 生成HTML主内容
def generate_main_content(data):
    content = "\n"
    # 添加分类内容
    for category in data:
        content += "        <section class='category'>\n"
        content += "            <h2><i class='fas " + category['icon'] + "'></i> " + category['category'] + "</h2>\n"
        content += "            <p class='category-description'>" + category['description'] + "</p>\n"
        content += "            <div class='items'>\n"
        
        for item in category['items']:
            content += "                <div class='item'>\n"
            content += "                    <a href='" + item['link'] + "' target='_blank'>\n"
            content += "                        <h3>" + item['name'] + "</h3>\n"
            content += "                        <p>" + item['description'] + "</p>\n"
            content += "                        <span class='link'>" + item['link'] + "</span>\n"
            content += "                    </a>\n"
            content += "                </div>\n"
        
        content += "            </div>\n"
        content += "        </section>\n"
    return content

# 主函数
def main():
    # 读取YAML文件
    with open('guide.yml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 确保public文件夹存在
    ensure_directory_exists('public')
    
    # 创建public/assets/css和public/assets/js目录
    ensure_directory_exists('public/assets/css')
    ensure_directory_exists('public/assets/js')
    
    # 复制assets文件夹中的CSS和JS文件到对应的目录
    copy_file('assets/css/style.css', 'public/assets/css/style.css')
    copy_file('assets/js/script.js', 'public/assets/js/script.js')
    
    # 读取模板文件
    header_template = read_template('templates/header.html')
    footer_template = read_template('templates/footer.html')
    
    # 生成主内容
    main_content = generate_main_content(data)
    
    # 组合完整的HTML内容，确保格式正确
    html_content = header_template + main_content + footer_template
    
    # 写入HTML文件
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML文件已生成：public/index.html")

if __name__ == "__main__":
    main()