# -*- coding: utf-8 -*-

import LangChain
import sys,io
import markdown

# LangChain.content_loader()
# LangChain.setup_data("./storage","./node.js")
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# print(sys.argv[1].encode('utf-8'))
re=LangChain.question_gpt("./storage/node.js",sys.argv[1])
re= str(re)
print(re)
md = markdown.Markdown(extensions=['tables'])
result=md.convert(re)
sys.stdout.flush()