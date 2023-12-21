from sparkdesk_web.core import SparkWeb



sparkWeb = SparkWeb(
    cookie=cookie,
    fd=fd,
    GtToken=GtToken
)

# single chat
# print(sparkWeb.chat("repeat: hello world"))
# continue chat
# sparkWeb.chat_stream()
# print(sparkWeb.chat_stream(false))

# print(sparkWeb.chat("你好啊"))
# print(sparkWeb.chat_stream("你是谁"))

response, addr = sparkWeb.rewrite_chat(question="你好啊",
                                       history_file_path="./history/history_2023-12-21-16-32-49.json")
print(response)
sparkWeb = SparkWeb(
    cookie=cookie,
    fd=fd,
    GtToken=GtToken
)
