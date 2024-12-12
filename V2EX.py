from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import json
import ddddocr

# 获取url
with open('config.json', 'w+') as file:
    json_config = json.load(file)  # 读取json文件并转成string列表

# 浏览器配置
co = ChromiumOptions()
page = ChromiumPage(co)

#OCR初始化
ocr = ddddocr.DdddOcr()
ocr.set_ranges(3) #字符集为小写和大写字母

def login():
    ele_cell = page.eles(".cell")[-1]#输入栏父节点
    ele_user=ele_cell.ele("text:用户名").next().child()
    ele_password=ele_cell.ele("text:密码").next().child()
    ele_user.clear()
    ele_password.clear()
    ele_user.input(json_config['name'])
    ele_password.input(json_config['password'])
    input_Code(ele_cell)
    ele_cell.ele(".super normal button").click()
    page.wait.load_start()

# 验证码处理
def input_Code(ele_cell):
    ele2 = ele_cell.ele("text:机器人").next()
    ele_input = ele2.children()[2]
    captcha_image = ele2.ele("#captcha-image")
    if captcha_image:
        # 元素#captcha-image截图
        img_bytes=captcha_image.get_screenshot(as_bytes='png')
        # 识别验证码
        Code = ocr.classification(img_bytes)
        ele_input.input(Code)

# 签到
def check_in():
    try:
        ele_check = page.ele("text:领取今日的登录奖励")
        ele_check.click()
        page.wait.load_start()
        ele1 = page.ele("text:每日登录奖励")
        ele_coin = ele1.next()
        ele_coin.click()
        page.wait.load_start()
    except Exception as e:
        print(e)
        return False  # 签到失败
    else:
        return True  # 签到成功

def main():
    page.get(json_config['base_url'])
    page.set.cookies(json_config['cookie'])
    page.refresh()
    is_check = check_in()
    if is_check:
        print("签到成功，正在关闭浏览器")
        page.close()
    else:
        is_login=page.ele(".super normal button").text
        if is_login !="现在注册":
            print("今日已经签到，正在关闭浏览器")
            page.close()
            return
        print("未登录状态")
        page.get(json_config['url_login'])
        try:
            while page.url != json_config['base_url']:
                login()
            print(page.url)
            print(page.cookies().as_str())

            json_config['cookie'] = page.cookies().as_str()
            json.dump(json_config, file, indent=4)

            print("登录成功，cookie已保存")
            check_in()
        except Exception as e:
            print("登录失败")
            print(e)
            return


if __name__ == "__main__":
    main()
