import LangChain

# LangChain.content_loader()
# LangChain.setup_data("./storage","./node.js")
re=LangChain.question_gpt("./storage","Uint8Array.prototype.slice()の使用方法を教えてください")
print(re)