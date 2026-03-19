🛡️ ClawGuard OSS - AI Security Gateway
ClawGuard Logo
License: MIT
Python 3.8+
FastAPI

极简 | 炫酷 | 零配置 | 高性能 | 安全

English | 中文

⚠️ Upgrade to PRO
✨ ClawGuard PRO - Enterprise-Grade Security
Feature	OSS (Free)	PRO ($14)
🔐 API Key Masking	✅	✅
🚨 Anomaly Detection	✅ Terminal	✅ Multi-channel
📊 Audit Logging	❌	✅ SQLite
🛡️ PII Scrubbing	❌	✅ Full
🌐 IP Whitelist/Blacklist	❌	✅
🔄 Auto Key Rotation	❌	✅
📧 Email/Webhook Alerts	❌	✅
🔒 Hardware-level Isolation	❌	✅
🚀 Get PRO Now - Only ¥99 ($14)

中文
🎯 什么是 ClawGuard OSS？
ClawGuard OSS 是一个开源的 AI API 安全网关，专为保护你的 OpenAI API 密钥而设计。它提供：

🔐 API 密钥自动打码 - 防止密钥在日志中泄漏
🚨 异常流量实时告警 - 检测可疑的 API 使用模式
⚡ 零配置透明转发 - 无需修改现有代码
🎨 炫酷终端界面 - 彩色 ASCII Logo + 实时流量可视化
🚀 高性能异步架构 - 基于 FastAPI + httpx
📸 效果展示
   ██████╗██╗      █████╗ ██╗    ██╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ 
  ██╔════╝██║     ██╔══██╗██║    ██║██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
  ██║     ██║     ███████║██║ █╗ ██║██║  ███╗██║   ██║███████║██████╔╝██║  ██║
  ██║     ██║     ██╔══██║██║███╗██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
  ╚██████╗███████╗██║  ██║╚███╔███╔╝╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
                              OSS v2 - Security Enhanced Edition

[22:30:45] ⚡ 流量劫持 | 127.0.0.1 → POST /v1/chat/completions | 状态: 🟢 200 | 1250ms | 🔐 Bearer sk-1234****cdef
🚀 快速开始
1. 安装依赖
pip install -r requirements-oss.txt
2. 设置环境变量
Linux/macOS:

export TARGET_HOST=https://api.openai.com
export PORT=8000
Windows (PowerShell):

$env:TARGET_HOST="https://api.openai.com"
$env:PORT="8000"
3. 启动服务
python clawguard_oss.py
4. 使用代理
将你的 API 请求指向 http://localhost:8000：

import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "sk-your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
🛡️ 安全功能
1. API 密钥自动打码
原始: Bearer sk-1234567890abcdef1234567890abcdef
打码: Bearer sk-1234****cdef
2. 异常流量告警
当检测到 5 分钟内同一 IP 失败 10 次时，自动触发告警：

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
🚨 安全告警：检测到异常流量模式
   来源 IP: 192.168.1.100
   失败次数: 12 次（5分钟内）
   最后状态: 401
   可能原因: API 密钥失效、被盗用或恶意扫描
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
3. HTTPS 安全提醒
如果目标主机使用 HTTP 协议，启动时会显示醒目警告。

📚 文档
安全使用指南 - 完整的安全最佳实践
配置示例 - 环境变量配置模板
🤝 贡献
欢迎提交 Issue 和 Pull Request！

📄 开源协议
MIT License - 详见 LICENSE

💎 升级到 PRO 版
想要获得企业级安全保护？

🔐 私钥物理隔离
📊 SQLite 审计日志
🛡️ PII 自动脱敏
🚨 智能异常检测
📧 邮件/Webhook 告警
🌐 IP 白名单/黑名单
🔄 自动密钥轮换
立即购买 PRO 版 - 仅需 ¥99 ($14)

English
🎯 What is ClawGuard OSS?
ClawGuard OSS is an open-source AI API security gateway designed to protect your OpenAI API keys. It provides:

🔐 Automatic API Key Masking - Prevent key leakage in logs
🚨 Real-time Anomaly Alerts - Detect suspicious API usage patterns
⚡ Zero-config Transparent Proxy - No code changes required
🎨 Stunning Terminal UI - Colorful ASCII logo + real-time traffic visualization
🚀 High-performance Async Architecture - Built on FastAPI + httpx
🚀 Quick Start
1. Install Dependencies
pip install -r requirements-oss.txt
2. Set Environment Variables
Linux/macOS:

export TARGET_HOST=https://api.openai.com
export PORT=8000
Windows (PowerShell):

$env:TARGET_HOST="https://api.openai.com"
$env:PORT="8000"
3. Start the Service
python clawguard_oss.py
4. Use the Proxy
Point your API requests to http://localhost:8000:

import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = "sk-your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
🛡️ Security Features
1. Automatic API Key Masking
Original: Bearer sk-1234567890abcdef1234567890abcdef
Masked:   Bearer sk-1234****cdef
2. Anomaly Detection Alerts
Automatically triggers when detecting 10 failures from the same IP within 5 minutes:

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
🚨 Security Alert: Anomalous Traffic Pattern Detected
   Source IP: 192.168.1.100
   Failed Requests: 12 (within 5 minutes)
   Last Status: 401
   Possible Cause: Invalid key, stolen key, or malicious scanning
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
3. HTTPS Security Reminder
Displays a prominent warning if the target host uses HTTP protocol.

📚 Documentation
Security Guide - Complete security best practices
Configuration Example - Environment variable template
🤝 Contributing
Issues and Pull Requests are welcome!

📄 License
MIT License - see LICENSE

💎 Upgrade to PRO
Want enterprise-grade security?

🔐 Hardware-level Key Isolation
📊 SQLite Audit Logging
🛡️ Automatic PII Scrubbing
🚨 Intelligent Anomaly Detection
📧 Email/Webhook Alerts
🌐 IP Whitelist/Blacklist
🔄 Automatic Key Rotation
Get PRO Now - Only ¥99 ($14)

Made with ❤️ by Independent Developers

⭐ Star us on GitHub if you find this useful!