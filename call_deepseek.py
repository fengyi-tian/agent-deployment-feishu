#!/usr/bin/env python3
"""
调用 DeepSeek API 的示例脚本
面试必备技能：用 Python 调用大模型 API
"""
import requests
import json

# ===== 配置区域 =====
API_KEY = "你的 DeepSeek API Key"  # 替换成你自己的 key
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"  # 或 deepseek-reasoner, deepseek-v4-flash 等
# ===================

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "你是一个有用的助手"},
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ],
    "temperature": 0.7,
    "max_tokens": 1024
}

print(f"📤 发送请求到 {API_URL}")
print(f"📝 模型: {MODEL}")
print("-" * 50)

response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    print(f"🤖 回复:\n{reply}")
    
    # 显示 token 用量
    usage = result.get("usage", {})
    print(f"\n📊 Token 用量:")
    print(f"   输入: {usage.get('prompt_tokens', 'N/A')}")
    print(f"   输出: {usage.get('completion_tokens', 'N/A')}")
    print(f"   总计: {usage.get('total_tokens', 'N/A')}")
else:
    print(f"❌ 错误: {response.status_code}")
    print(response.text)
