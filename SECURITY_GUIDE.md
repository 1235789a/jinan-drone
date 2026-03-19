🛡️ ClawGuard OSS 安全使用指南
📋 目录
安全功能概览
API 密钥保护
异常流量告警
HTTPS 最佳实践
密钥轮换建议
OSS vs PRO 安全对比
常见安全问题
安全功能概览
ClawGuard OSS v2 提供 3 个核心安全功能：

1. 🔐 API 密钥自动打码
功能说明：

自动检测并打码日志中的 API 密钥
防止密钥在终端输出中泄漏
零配置，自动生效
示例：

原始: Bearer sk-1234567890abcdef1234567890abcdef
打码: Bearer sk-1234****cdef
2. 🚨 异常流量实时告警
功能说明：

检测短时间内大量失败请求
触发条件：5 分钟内同一 IP 失败 10 次
告警冷却期：10 分钟（避免重复告警）
告警示例：

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
🚨 安全告警：检测到异常流量模式
   来源 IP: 192.168.1.100
   失败次数: 12 次（5分钟内）
   最后状态: 401
   可能原因: API 密钥失效、被盗用或恶意扫描
   💎 PRO 版支持：邮件告警、自动封禁、智能检测
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
3. ⚠️ HTTPS 安全提醒
功能说明：

启动时检测目标主机协议
如果使用 HTTP，显示醒目警告
提供 HTTPS 配置建议
API 密钥保护
为什么需要密钥保护？
API 密钥是访问 AI 服务的凭证，一旦泄漏可能导致：

💸 账户余额被盗用
🚨 服务被滥用
📊 数据被窃取
OSS 版保护措施
终端日志打码

自动检测 Authorization: Bearer sk-... 格式
只显示前后 4 位字符
中间部分用 **** 替代
错误信息脱敏

网络错误不包含完整密钥
异常信息自动清洗
PRO 版增强功能
✅ 完整的 PII 脱敏（邮箱、手机、身份证等）
✅ 自定义脱敏规则
✅ 脱敏日志持久化
✅ 密钥使用统计和审计
异常流量告警
告警触发条件
指标	OSS 版	PRO 版
检测窗口	5 分钟	可配置（1-60 分钟）
失败阈值	10 次	可配置（1-1000 次）
告警方式	终端输出	终端 + 邮件 + Webhook
冷却期	10 分钟	可配置
自动封禁	❌	✅
常见告警场景
场景 1：API 密钥失效
症状：大量 401 错误
原因：密钥过期或被撤销
解决：更换新的 API 密钥
场景 2：密钥被盗用
症状：来自陌生 IP 的大量请求
原因：密钥泄漏到公开仓库或日志
解决：立即撤销密钥并更换
场景 3：恶意扫描
症状：大量 404 或 403 错误
原因：攻击者尝试探测 API 端点
解决：考虑添加 IP 白名单（PRO 版）
如何响应告警
立即检查

查看告警中的 IP 地址
确认是否为合法请求
分析原因

检查 API 密钥是否有效
查看请求路径是否正确
确认是否有代码错误
采取行动

如果是密钥问题：更换密钥
如果是攻击：考虑升级到 PRO 版使用 IP 封禁
如果是误报：调整告警阈值（PRO 版）
HTTPS 最佳实践
为什么需要 HTTPS？
使用 HTTP 协议存在以下风险：

🔓 数据明文传输，可被窃听
🎭 易受中间人攻击
🚫 无法验证服务器身份
OSS 版 HTTPS 配置
ClawGuard OSS 本身不提供 HTTPS，但可以通过以下方式实现：

方案 1：使用 Nginx 反向代理
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
方案 2：使用 Caddy（自动 HTTPS）
your-domain.com {
    reverse_proxy localhost:8000
}
PRO 版 HTTPS 功能
✅ 内置 HTTPS 支持
✅ 自动证书管理（Let's Encrypt）
✅ HSTS 头自动添加
✅ TLS 1.3 支持
✅ 证书自动续期
密钥轮换建议
为什么需要轮换密钥？
定期轮换 API 密钥可以：

🔒 降低密钥泄漏风险
🛡️ 限制潜在损失范围
📊 符合安全合规要求
轮换频率建议
环境	建议频率	说明
开发环境	90 天	风险较低
测试环境	60 天	中等风险
生产环境	30 天	高风险
高敏感环境	7-14 天	极高风险
OSS 版轮换流程
生成新密钥

在 OpenAI 控制台创建新密钥
记录密钥创建时间
更新环境变量

export OPENAI_API_KEY=sk-new-key-here
重启服务

# 停止旧服务
Ctrl+C

# 启动新服务
python clawguard_oss_v2.py
撤销旧密钥

等待 24 小时确保无问题
在控制台撤销旧密钥
PRO 版自动轮换
✅ 自动生成新密钥
✅ 零停机时间切换
✅ 多密钥负载均衡
✅ 旧密钥自动撤销
✅ 轮换历史审计
OSS vs PRO 安全对比
功能	OSS 版	PRO 版
密钥保护		
终端日志打码	✅	✅
完整 PII 脱敏	❌	✅
自定义脱敏规则	❌	✅
脱敏日志持久化	❌	✅
流量监控		
异常流量告警	✅ 终端	✅ 多渠道
告警阈值配置	❌ 固定	✅ 可配置
邮件通知	❌	✅
Webhook 集成	❌	✅
智能异常检测	❌	✅ ML
访问控制		
IP 白名单	❌	✅
IP 黑名单	❌	✅
自动封禁	❌	✅
地理位置识别	❌	✅
密钥管理		
密钥轮换提醒	✅	✅
自动密钥轮换	❌	✅
多密钥管理	❌	✅
密钥使用统计	❌	✅
审计日志		
终端日志	✅	✅
SQLite 持久化	❌	✅
请求/响应记录	❌	✅
日志导出	❌	✅ CSV/JSON
HTTPS		
HTTPS 提醒	✅	✅
内置 HTTPS	❌	✅
自动证书管理	❌	✅ Let's Encrypt
HSTS 支持	❌	✅
常见安全问题
Q1: 如何防止 API 密钥泄漏？
A: 遵循以下最佳实践：

不要硬编码密钥

# ❌ 错误
api_key = "sk-1234567890abcdef"

# ✅ 正确
api_key = os.getenv("OPENAI_API_KEY")
使用 .gitignore

.env
*.key
*.pem
定期扫描代码库

# 使用 git-secrets
git secrets --scan
Q2: 收到异常流量告警怎么办？
A: 按以下步骤处理：

确认告警真实性

检查 IP 地址是否熟悉
查看失败原因（401/403/404）
分析根本原因

密钥问题：更换密钥
代码错误：修复 bug
恶意攻击：考虑升级 PRO 版
采取预防措施

加强密钥管理
添加访问控制
启用更多监控
Q3: OSS 版够用吗？什么时候需要升级 PRO？
A: 考虑升级 PRO 版的场景：

🏢 生产环境：需要完整审计日志
💰 高价值应用：API 调用成本高
🔒 合规要求：需要 PII 脱敏和审计
🌐 多用户场景：需要访问控制
📊 精细监控：需要详细统计和告警
Q4: 如何测试安全功能？
A: 使用以下方法测试：

测试密钥打码

# 发送带密钥的请求
curl http://localhost:8000/v1/models \
  -H "Authorization: Bearer sk-test1234567890abcdef"

# 检查终端日志，应显示打码后的密钥
测试异常流量告警

# 快速发送 10+ 个失败请求
for i in {1..12}; do
  curl http://localhost:8000/v1/models \
    -H "Authorization: Bearer sk-invalid"
done

# 应该看到红色告警
测试 HTTPS 提醒

# 设置 HTTP 目标
export TARGET_HOST=http://api.example.com
python clawguard_oss_v2.py

# 应该看到安全警告
🚀 升级到 PRO 版
想要获得企业级安全保护？

💎 仅需 ¥99 ($14)
🔐 私钥物理隔离
📊 SQLite 审计日志
🛡️ PII 自动脱敏
🚨 智能异常检测
📧 邮件/Webhook 告警
🌐 IP 白名单/黑名单
🔄 自动密钥轮换
立即购买: https://clawguard.dev/pro

📚 相关文档
README_OSS.md - 快速开始指南
.env.oss.example - 配置示例
官方文档 - 完整文档
保护你的 API 密钥，从现在开始！ 🛡️