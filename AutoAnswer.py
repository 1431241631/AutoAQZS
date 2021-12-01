import json
import random
from os import path

import requests

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 "
                  "Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63040029) "
}


class AutoAnswer:
    def __init__(self):
        self._http_request = requests.session()  # 统一会话可以省略cookie合并
        if path.exists("./answer.json") is False:
            self.question_bank()
        with open("./answer.json", "r") as f:
            self._answer_data = json.loads(f.read())
        if self._answer_data is None:
            print("题库提取失败！")

    def login(self, user_name: str, password: str, unit_code: int = 13):
        """
        登录
        :param user_name:
        :param password:
        :param unit_code: 学校代码，默认河科大为13
        """
        form_data = {
            "unit_code": unit_code,
            "student_id": user_name,
            "password": password
        }
        response_data = self._http_request.post(url="http://gjaqzsjs.haedu.cn/Login/auth", data=form_data,
                                                headers=Headers).json()
        print(response_data)

    def __get_que_list(self):
        que_list_data = self._http_request.post(url="http://gjaqzsjs.haedu.cn/Answer/getQuestionLists",
                                                headers=Headers).json()
        print(que_list_data)
        que_list = que_list_data["data"]["question"]
        # print(que_list)
        return que_list

    def match_answer(self):
        que_list = self.__get_que_list()
        panduan_ = {"对": "A", "错": "B"}
        answer_list = [{"number": i["number"],
                        "answer": self._answer_data[i["type_code"]][i["question"]]["answer"] if panduan_.get(
                            self._answer_data[i["type_code"]][i["question"]][
                                "answer"].strip()) is None else panduan_.get(
                            self._answer_data[i["type_code"]][i["question"]]["answer"].strip())} for i in que_list]
        print(answer_list)

        return answer_list

    def submit_answer(self, answer_list: list):
        form_data = {
            "answer": json.dumps(answer_list),
            "use_time": random.randint(5, 9) * 60 + random.randint(1, 58)
        }
        print("提交内容：", form_data)
        response_data = self._http_request.post(url="http://gjaqzsjs.haedu.cn/Answer/submitAnswer", headers=Headers,
                                                data=form_data).json()
        print(response_data)

    def auto(self, user_name: str, password: str):
        self.login(user_name=user_name, password=password)
        que_list = self.match_answer()
        self.submit_answer(que_list)

    @staticmethod
    def question_bank():
        """
        采集/更新 题库
        """
        que_types = {"danxuan": 16, "duoxuan": 9, "panduan": 11}  # 题型及题库大小
        type_codes = {"danxuan": 1, "duoxuan": 2, "panduan": 3}
        que_bank_data = {}  # 定义本地题库
        for que_type in que_types.keys():
            # 下载题库
            page_size = que_types[que_type]
            for page_index in range(1, page_size + 1):
                que_bank_url = f"http://gjaqjs.haedu.cn/data/gjaqzsjsxxzl_{que_type}/gjaqzsjsxxzl_" \
                               f"{que_type}_{page_index}.json"
                print("题库：", que_bank_url)
                ans_data = requests.get(que_bank_url).json()
                print("内容：", ans_data)
                ans_data = {i["question"]: i for i in ans_data}  # 原题库中的题为列表存储，提取题目id方便后续查找
                que_bank_data[type_codes[que_type]] = ans_data if que_bank_data.get(type_codes[que_type]) is None else \
                    dict(que_bank_data[type_codes[que_type]], **ans_data)  # 合并子题库
                # print(que_bank_data)
        # 写入本地文件
        with open("answer.json", "w") as f:
            f.write(json.dumps(que_bank_data))


if __name__ == '__main__':
    user_name = input("请输入学号：")
    password = input("请输入密码：")

    try:
        auto_answer = AutoAnswer()
        auto_answer.auto(user_name=user_name, password=password)
    except Exception as e:
        print(e)
    finally:
        input("输入任意键结束...")
