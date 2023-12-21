from sparkdesk_web.core import SparkWeb

cookie = ("di_c_mti=02d4252d-7c7f-631b-95b0-5ded3cb30249; d_d_app_ver=1.4.0; "
          "d_d_ci=b16f0a55-b69a-66c5-ac02-73bdd97afc80; account_id=16588257894; "
          "ssoSessionId=b6e5304e-a91e-45aa-8323-7b70272734a6; daas_st={"
          "%22sdk_ver%22:%221.3.9%22%2C%22status%22:%220%22}; appid=150b4dfebe; "
          "gt_local_id=EzipNS03IHCTtxkO+6pSeVHmIC79v9gd8Q7I+A77OzHd2a1UuNMIwA==")
fd = "865327"
GtToken = ("RzAwAGOQpkLQ//nbnz9Qe+qaEuPQHWvgaXjW41Cjf3+TfhoeuVbvZXqe3DcjE4uU5JQC1W7cczSupOU"
           "/3bzS2eBWlUQQqMLiss6WfbsyceOCUCrxOhd0t4UpTPtATjfG36VUXhKYllKaL2ZkVdMNhD7kFBFGHfPDe0wYSwmFuvPtXx"
           "/D5SsKzCKNEuaJEyNRFYQ4UGWOfqlgrk/Cv3TX/sNSUJNt+MrWPIWHknynwmmMEM86Bs7A5FYL9dF"
           "+3qjwdejrjTFcAQqEz49qnl0qGngNgZK0+kKdZPCkdDK8eTiidy61OIMr"
           "+UM3Hgd9yyjxWLPOQ9J2kFYsqaHcusEwARPibgetTh7oKdmeye"
           "/o8LyLT2VEJkj23OOgdK6IYIXudTfF6LmBbA6iPBjNTYzJjxPkCUHTklQzOWnpyKuReYgsFMUPeq0nMT8zaCHx1YiAC"
           "+2KaZdtRMZn2LlA3+F2G96UBkPJoMOziSmLIu4M6L2/CkucUMdjjbfOvZKcYNRmlBgnQs4l8nyzz1"
           "+xp2ya5OT22IPxiwXP0fFtUDreeRSBtqLGSzrUb7fXESoc2zb4W7olzIrIaKSOcZ4C9JIQgWLU"
           "+uko33LS1tEWdqvUvuuCrCIofHW71ERTaaRTmh2k19H1h+LbbrqdfF8fCaDeT5Pee9ih/ZrcJiQXJNGtdrJZoIqU2H+jrJnO91HcIpt"
           "+MUdxZWe73JGUGRVLqmrbJSDzbqC3i74A66n4n/g+lPQbuQlewCRkQczX"
           "+hZ41YCgHF22sTZyoEkUG013nu7S0MBsBMMzNX3sH33bzfrheX+V"
           "+5P6qOdFhZAsnG98zrRK3FddtD7miPXXZ2fAYzlOHSXjGWhItg4UCvm31AhmP2ujxlOe6JwpZ1bi"
           "+/nt0HuMFsc51L3y9eabyw9A5uc1WMBtjkipk3tF/oHkKJkM+fJKCd6vGpSw/ifGzn0fDNjK"
           "+uJvus2y1MxF8fOxChXbXPb9FtWPWj0jq2z9/153fD++OOJDJal3YoIrfOH0cVCs2GWLO2wjp62Qfk"
           "/a03Bww6PgWT6koEnORpsfZZGWKx65Yemj4wsLiL1ZQoI80ebzH6bpWsFd6NldMaWlhEWdl19S3MsRkRQCi6JM71WsjJHVxmHw7U"
           "/Ti9C7AhETDj8GOpM6yLGhIG+CcAMDgA4fikVRXOPUrqZSgrAyE3kGFfuk+HnU6xQyu743Vbfy7+U"
           "/jHDP6wiNa1b0CjYRnCBVAwGqJVVaSZwJIlGqxYFM1R6Pxqb+6aFyJ/Z2dYJ"
           "/sbMpkYoLiiE0CPAXYqWTIwrArpwkqsru5ZnywyCXWPr5MjFZF7pmTAT+DvO78eMRoTyYB8rnkSHL8SABNbwqaGaZl"
           "/pe0mdmAyKgDmGkGFVd0scUFYt0zlrJhA8Y3X7OdkyuKAxWkH/sUwSrklzfaq7Mf4RPM2DrqVPGBs4xMoOZAzQH1Rsin"
           "+6K37DptcVBRzNpH9csppdMUnMGxIJ9K2brumdgO3BDqEbj4PLuYUjACqu4B45mo78teFN9iUlQEvwZVwt2+w"
           "+Dj5eEYT6wvw2BHSAmqFT1C3dZjPosEESdAeInWKwodtP4F7og2T9NLHlcfnyUmsuG5d56H+sX6yDpi/HO2A74xQB2MuFv3S8eyn9E"
           "+ypfOA==")

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
