import yaml
import os

# 读取YAML文件
with open('guide.yml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# 生成HTML内容
html_content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网站导航</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="https://openlist.cflmy.cn/sd/iv5f06Iw/Web/logo/logo.ico">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="logo-container">
                <img src="https://openlist.cflmy.cn/sd/iv5f06Iw/Web/logo/logo-rb-b.webp" alt="Logo" class="logo">
                <h1>网站导航</h1>
            </div>
        </header>
        
        <main>
'''

# 添加分类内容
for category in data:
    html_content += f"        <section class='category'>\n"
    html_content += f"            <h2><i class='fas {category['icon']}'></i> {category['category']}</h2>\n"
    html_content += f"            <p class='category-description'>{category['description']}</p>\n"
    html_content += f"            <div class='items'>\n"
    
    for item in category['items']:
        html_content += f"                <div class='item'>\n"
        html_content += f"                    <a href='{item['link']}' target='_blank'>\n"
        html_content += f"                        <h3>{item['name']}</h3>\n"
        html_content += f"                        <p>{item['description']}</p>\n"
        html_content += f"                        <span class='link'>{item['link']}</span>\n"
        html_content += f"                    </a>\n"
        html_content += f"                </div>\n"
    
    html_content += f"            </div>\n"
    html_content += f"        </section>\n"

# 完成HTML内容
html_content += '''        </main>
        
        <footer>
            <p>&copy; 2023 网站导航</p>
        </footer>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''

# 写入HTML文件
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML文件已生成：public/index.html")