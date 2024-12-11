from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import json
import ddddocr

# 获取url
with open('config.json', 'r') as file:
    json_config = json.load(file)  # 读取json文件并转成string列表

# 浏览器配置
co = ChromiumOptions()
co.headless()
page = ChromiumPage(co)

def login():
    ele_cell = page.eles(".cell")[-1]#输入栏父节点
    ele_user=ele_cell.ele("text:用户名").next().child()
    ele_password=ele_cell.ele("text:密码").next().child()
    ele_user.input(json_config['name'])
    ele_password.input(json_config['password'])
    input_Code(ele_cell)

# 验证码处理
def input_Code(ele_cell):
    ele2 = ele_cell.ele("text:机器人").next()
    ele_input = ele2.children()[2]
    captcha_image = ele2.ele("#captcha-image")
    if (captcha_image):
        # 元素#captcha-image截图
        captcha_image.get_screenshot()
        bytes_str = captcha_image.get_screenshot(as_bytes='png')
        # 识别验证码
        ocr = ddddocr.DdddOcr()
        Code = ocr.classification(bytes_str)
        ele_input.input(Code)

    ele_cell.ele(".super normal button").click()

# 签到
def check_in():
    ele_check = page.ele("text:领取今日的登录奖励")
    ele_check.click()
    page.wait.load_start()
    ele1 = page.ele("text:每日登录奖励")
    ele_coin = ele1.next()
    ele_coin.click()
    page.wait.load_start()

def main():
    page.get(json_config['base_url'])
    try:
        check_in()
        print("签到成功，正在关闭浏览器")
        page.close()
    except Exception as e:
        print("未登录状态")
        page.get(json_config['url_login'])
        try:
            while page.url != json_config['base_url']:
                login()
            if page.url == json_config['base_url']:
                print("登录成功，cookie已保存")
                check_in()
        except Exception as e:
            print("登录失败")
            return


if __name__ == "__main__":
    main()
