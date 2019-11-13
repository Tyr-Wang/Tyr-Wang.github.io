import os
import re

def main():
    os.chdir(r"D:\Programs\Hexo-Blog\source\_posts")
    fls = os.listdir(r".")
    aim_ls = []
    for i in fls:
        if i[-3:] == ".md":
            aim_ls.append(i)

    for i in aim_ls:
        content = ""
        with open(i, "r", encoding='UTF-8') as f:
            content = f.read()

        if content == '':
            continue

        try:
            content = re.sub(r"(!\[.*?\]\()\\?/?(images)\\?/?(pasted-\d\d?\d?\d?\.....?\))", "\g<1>/\g<2>/\g<3>", content)
            f = open(i, "w", encoding='UTF-8')
            f.write(content)
            f.close()
        except AttributeError as e:
            print(e)

        finally:
            f.close()


if __name__ == '__main__':
    main()
