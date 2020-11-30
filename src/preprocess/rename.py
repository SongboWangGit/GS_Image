import os
path = "./data/pictures"
filelist = os.listdir(path) 
count=0
for file in filelist:
    Olddir = os.path.join(path, file) 
    if os.path.isdir(Olddir):  
        continue
    filename = os.path.splitext(file)[0]  
    filetype = os.path.splitext(file)[1]  
    print(filename)
    Newdir = os.path.join(path, str(count).zfill(5) + filetype)  
    os.rename(Olddir, Newdir)  
    count += 1

print ('END')
count=str(count)
print("共有"+count+"张图片尺寸被修改")
