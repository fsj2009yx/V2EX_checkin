from DrissionPage import ChromiumPage
import json
import ddddocr

#获取url
with open('config.json', 'r') as file:
    json_str=json.load(file)#读取json文件并转成string列表

page = ChromiumPage()
page.get(json_str['url'])
ele_parents = page.eles(".cell")[-1]#输入栏父节点

#输入user
def input_user():
    ele1=ele_parents.ele("text:用户名")
    ele2=ele1.next()
    ele_input=ele2.child()
    if(ele_input):
        ele_input.input(json_str['name'])

#输入密码
def input_password():
    ele1=ele_parents.eles("text:密码")[0]
    ele2=ele1.next()
    ele_input=ele2.child()
    if(ele_input):
        ele_input.input(json_str['password'])

#验证码处理
def input_Code():
    ele1=ele_parents.eles("text:机器人")[0]
    ele2=ele1.next()
    ele_input=ele2.children()[2]
    captcha_image=ele2.ele("#captcha-image")
    if(captcha_image):
        #元素#captcha-image截图
        captcha_image.get_screenshot()
        bytes_str = captcha_image.get_screenshot(as_bytes='png')
        #识别验证码
        ocr=ddddocr.DdddOcr()
        Code=ocr.classification(bytes_str)
        ele_input.input(Code)

def login():
    ele1 = ele_parents.eles("text:机器人")[0]
    ele2=ele1.parent()
    ele3=ele2.next()
    ele4=ele3.children()[-1]
    ele_login=ele4.children()[-1]
    ele_login.click()

#签到
def check_in():
    ele_check=page.ele("text:领取今日的登录奖励")
    ele_check.click()
    page.wait.load_start()
    ele1=page.ele("text:每日登录奖励")
    ele_coin=ele1.next()
    ele_coin.click()
    page.wait.load_start()


def main():
    global ele_parents
    input_password()
    input_Code()
    login()
    page.wait.load_start()
    ele_problem=page.eles(".problem")
    if ele_problem:
        print(ele_problem)
        ele_parents=page.eles(".cell")[-1]  # 输入栏父节点
        main()
    else:
        page.wait.load_start()
        ele_failed=page.ele("text:登录受限")
        if not ele_failed:
            check_in()
        else:
            print(ele_failed)
            print("访问受限：请更换网络代理或稍后再次尝试运行该脚本")



if __name__ == '__main__':
    try:
        input_user()
        main()
    finally:
        page.close()
