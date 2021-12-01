# AutoAQZS

自动安全知识问答脚本

## QA

### 答案来源

答案来自官方题库，根据题目匹配作答。如果是第一次使用会自动下载官方题库。如果希望更新题库则删除目录下的**answer.json**文件再重新打开脚本即可。

答案不保证全对

可能会有匹配空的情况，因为不排除题库不完整的可能。

### 作答时间

作答时间是随机的

```python
random.randint(5, 9) * 60 + random.randint(1, 58)
```
