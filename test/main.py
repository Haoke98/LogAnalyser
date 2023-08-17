# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from ip_helper import getGeoLocation
import csv


def cutByMonth():
    # TODO：要完善后期部分， 可以按照 Oct，Nov，Feb这样分开成多个文件，方便操作。实现一键切割。
    with open("2022/www.xjip.info.log_aGyYz6.tar/www.xjip.info.log", 'r', encoding="utf-8") as rf:
        with open("2022/10/www.xjip.info.log", 'w', encoding="utf-8") as wf:
            while True:
                l: str = rf.readline()
                if "/Oct/2022" in l:
                    wf.write(l)
                    print(l)
                if "/Nov/2022" in l:
                    print("获取10月份的成功")
                    break


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import re

    pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    ips = {}
    with open("2022/10/www.xjip.info.log", 'r', encoding="utf-8") as f:
        ln = 0
        for i in f:
            l: str = f.readline()
            ln += 1
            m = pattern.search(l)
            if m is None:
                print(ln, l)
            else:
                ip = l[m.regs[0][0]:m.regs[0][1]]
                if ips.keys().__contains__(ip):
                    ips[ip] += 1
                else:
                    ips.setdefault(ip, 1)
    l = sorted(ips.keys(), key=lambda item: ips.get(item), reverse=True)
    i = 1
    with open("2022/10/www.xjip.info.ip.csv", 'w', encoding='utf-8') as f:
        cw = csv.writer(f)
        for ip in l:
            count = ips.get(ip)
            location = getGeoLocation(ip)
            print(str(i).rjust(4, " "), ip.ljust(15, " "), str(count).rjust(5, " "), location)
            cw.writerow([i, ip, count, location])
            i += 1

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
