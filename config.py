import os
# from pathlib import Path
import re
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
path = './docs'
md_all_list = []
for root, dirs, files in os.walk(path,topdown=True): 
    if os.path.basename(root)[:1] != '.' and os.path.basename(root)[:1] != '_' and os.path.basename(root) != 'images':
#         print(os.path.relpath(root))
        
        dir_list = []
        md_list = []
        
        sidebar = os.path.join(root,'_sidebar.md')
        readme = os.path.join(root,'README.md')
        
        for filename in files:
            if re.match(r'^(md)?[^._(readme)].*[.]md$',filename.lower()):  # 去掉.开头，_开头和readme文件
                file = os.path.relpath(os.path.join(root,filename))
                with open(file,'r',encoding='utf8') as f:
                    text = f.read()
                if re.match(r'(?:.|\n)*.*\[@title\]:.*',text):         
                    title = re.findall(r'\[@title\]: (.*)',text)[0]
                else:
                    title = filename.replace('.md','')
                md_dict = {
                    "id": filename,
                    "title": title,
                    "location": file.replace('\\','/'),
                    "root": os.path.relpath(root).replace('\\','/')
                }
                md_list.append(md_dict)

        md_all_dict = {
            'root':os.path.relpath(root).replace('\\','/'),
            'md_list':md_list
        }
    
        md_all_list.append(md_all_dict)

        if os.path.basename(root) != 'docs':            
            # readme
            readme_text = "\n[@id]: {id}\n[@title]: {title}\n[@location]: {location}\n[@author]: leity\n[@date]: {date}\n\n### 文章列表\n\n".format(
                    id = 'README.md ',title = os.path.basename(root),location = os.path.relpath(readme).replace('\\','/'),date=today)
            # sidebar
            sidebar_text = "\n[@id]: {id}\n[@title]: {title}\n[@location]: {location}\n[@author]: leity\n[@date]: {date}\n\n* [../](README.md)\n* [目录索引]({root}/README.md)\n".format(
                    id = '_sidebar.md ',title = os.path.basename(root),location = os.path.relpath(sidebar).replace('\\','/'),date=today,root=os.path.relpath(root).replace('\\','/').replace('docs/',''))
            for md in md_list:
                readme_text = readme_text + "##### {id}  [《{title}》]({location})\n".format(id=md['root'].replace('docs/','')+"/"+md['id'],title=md['title'],location=md['location'].replace('docs/',''))
                sidebar_text = sidebar_text + "* [{title}]({location})\n".format(title=md['title'],location=md['location'].replace('docs/',''))
            
#             print(readme_text)
#             print(sidebar_text)

            with open(readme,'w',encoding='utf8') as f:
                text = f.write(readme_text)
            with open(sidebar,'w',encoding='utf8') as f:
                text = f.write(sidebar_text)

        
# 首页
home = os.path.join(path,'README.md')
home_text = "\n[@id]: {id}\n[@title]: {title}\n[@location]: {location}\n[@author]: leity\n[@date]: {date}\n\n### 文章列表\n\n".format(
        id = 'README.md ',title = '首页',location = 'docs/README.md',date=today)
for mds in md_all_list:
    if mds['root'] != 'docs':
        home_text = home_text + "\n### "+ mds['root'].replace('docs/','') + "\n\n----\n\n"
        for md in mds['md_list']:
            home_text = home_text + "##### {id}  [《{title}》]({location})\n".format(id=md['root'].replace('docs/','')+"/"+md['id'],title=md['title'],location=md['location'].replace('docs/',''))
# print(home_text)
with open(home,'w',encoding='utf8') as f:
    text = f.write(home_text)
