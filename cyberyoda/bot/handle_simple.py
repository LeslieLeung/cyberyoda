def handle_echo(prompt: str):
    return prompt.replace("/echo", "").strip()


def handle_help():
    return """
    Usage:
    直接开始聊天即可
    /echo [text] 输出text
    /help 显示帮助信息
    /system [text] 保存系统指令（见https://platform.openai.com/docs/guides/chat/instructing-chat-models）
    prompt参考 https://www.explainthis.io/zh-hans/chatgpt
    /reset 重置对话历史
    """
