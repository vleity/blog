import os

# os.path.basename(root)  获取目录名称


for root, dirs, files in os.walk('.',topdown=True):
    if os.path.basename(root)[:1] != '.' and os.path.basename(root)[:1] != '_':
        print(os.path.relpath(root))
        #print(os.path.basename(root))
    for file in files:
        if file[:1] != '.' and file[:1] != '_':
            print('\t%s' % file)