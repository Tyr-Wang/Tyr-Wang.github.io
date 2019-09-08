# coding: utf-8
import os
import re
import subprocess
from time import sleep

'''
requirements:
original format is template of vnote blog tmp, with the header values and read more sign.
Deploy：change the format to the blog (no need) and modify the "\\" to "/"
specific func:
log: read log.txt and return a list of the files newly changed or established
copy: from Vnote to Blog folder && only copy newer and record in txt
modify:, modify newly copied file 
copy: pack up md file for recover more easily
Hidden deploy: same way and modify the index page
finally: dat, hexo g -d

ATTENTION:
please use abs addr
put script under the folder of your daily work space
OR
you can use linker to Desktop if you put script in Blog folder and pack up in git
'''
v_post_dir = r'D:\Data\Documents\Note\vnotebook\Blog'
v_hidden_dir = r'D:\Data\Documents\Note\vnotebook\Hidden'
blog_dir = r"D:\Programs\Hexo-Blog"
source_dir = r"D:\Programs\Hexo-Blog\source"
post_dir = r"D:\Programs\Hexo-Blog\source\_posts"
Hidden_dir = r"D:\Programs\Hexo-Blog\source\Hidden"
log_dir = r"D:\Programs\Hexo-Blog\source\uploads\log.txt"
exclude_dir = r"D:\Programs\Hexo-Blog\source\uploads\exclude.txt"
img_dir = r"D:\Programs\Hexo-Blog\source\images"


def copy(src=v_hidden_dir, dst=Hidden_dir, exclude=exclude_dir, log_file=log_dir, imgs_dir=img_dir):
    # os.popen("xcopy {} {} /s /h /d /y".format(src, dst))
    cmd = "xcopy {} {} /S /D /Y /EXCLUDE:{} 2>&1 >{}".format(src, dst, exclude, log_file)
    cmd2 = "xcopy {} {} /S /D /Y  2>&1".format(src+"\\_v_images", imgs_dir)
    #print(cmd, "\n", cmd2)
    subprocess.Popen(cmd, shell=True)
    subprocess.Popen(cmd2, shell=True)


def log(log_path=log_dir):
    sleep(0.1)
    try:
        f = open(log_path, "r", encoding="gbk")
        logs = f.read()
        f.close()
        log = re.sub(r"复制了 .*? 个文件", "", logs)
        log_list = log.split("\n")
        log_list.remove("")
        log_list.remove("")
        return log_list

    except FileNotFoundError as e:
        print(e)
        input("wait")

    except ValueError as e:
        return log_list


def show_log(ls, str="log:"):
    if ls:
        print(str)
        for i in ls:
            print(i)


def del_last(file=r"D:\source\uploads\log.txt"):
    log_list = []
    with open(file, "rb+") as f:
        index = f.seek(-18, 2)
        if f.read(1) == "\n":
            f.seek(-1, 1)
            f.truncate()
            f.seek(0, 0)
            strings = f.read()
            log_list = strings.split("\n")
        elif  index == 0:
            f.seek(-1, 1)
            f.truncate()
            f.seek(0, 0)
            strings = f.read()
            log_list = strings.split("\n")

        else:
            pass
    return log_list


def mv_img(dir, imgs_dir=img_dir):
    v_img = dir+"\\_v_images"
    ls = os.listdir(v_img)
    for i in ls:
        try:
            os.rename(v_img+"\\"+i, imgs_dir+"\\"+i)
        except FileExistsError as e:
            os.remove(v_img+"\\"+i)
            continue


def modify(dir, file_list=[]):
    if not file_list:
        return 0
    #os.chdir(post_dir)
    os.chdir(dir)
    #fls = os.listdir(r".")
    fls = file_list
    aim_ls = []
    for i in fls:
        i = i.split("\\")[-1]
        if i[-3:] == ".md":
            aim_ls.append(i)

    for i in aim_ls:
        content = ""
        with open(i, "rb") as f:
            cls = f.readlines()
            cl = []
            for j in cls:
                cl.append(j.decode("utf8", "ignore").strip("\n"))
            content = "".join(cl)

        if content == '':
            continue

        try:
            content = re.sub(r"(!\[.*?\]\()\\?/?(images)\\?/?(pasted-\d\d?\d?\d?\.png\))", "\g<1>/\g<2>/\g<3>", content)
            content = re.sub(r"(!\[.*?\]\()\\?/?_v_(images)/?(.*?\.png.*?\))", "\g<1>/\g<2>/\g<3>", content)
            #mv_img(dir)
            f = open(i, "w", encoding='UTF-8')
            f.write(content)
        except AttributeError as e:
            print(e)

        finally:
            f.close()


def ch_index(ls=[], dir=Hidden_dir):
    if not ls:
        return 0
    os.chdir(dir)
    try:
        tmp = '<center><a href="/Hidden/{}" style="color:white;text-decoration:none;" >{}</a></center>\r'
        #ls = os.listdir(".")
        f = open("index.md", "r+b")
        contents = f.read()
        for i in ls:
            i = i.split("\\")[-1]
            if os.path.isdir(i) or "index" in i or i[-3:] != ".md":
                continue
            tmp = tmp.format(i[:-3], i[:-3])
            if tmp.encode("utf8") in contents:
                continue
            f.write(tmp.encode("utf8"))
    except Exception as e:
        print(e)

    finally:
        f.close()


def pack_up():
    pass


def deploy(clean=False):
    os.chdir(blog_dir)
    if clean:
        os.system("hexo clean")
    os.system("hexo g -d")


def main(c=False):
    copy(v_post_dir, post_dir)
    l_post = log()
    modify(post_dir, l_post)
    copy(v_hidden_dir, Hidden_dir)
    l_hidden = log()
    modify(Hidden_dir, l_hidden)
    ch_index(l_hidden)
    show_log(l_hidden, "hidden")
    show_log(l_post, "post")
    deploy(clean=c)


if __name__ == '__main__':
    #main(False)
    main(True)
    input("All Done !!")
