---
layout: post
title: "无标题"
date: 2026-03-09 12:00:00 +0800
categories: [OpenClaw, 工具]
tags: []
---

问题现象

打开 OpenClaw 控制面板 (http://127.0.0.1:18789/) 后无法连接，可能的表现：

    页面一直加载中

    显示连接错误

    看不到配对页面

根本原因

OpenClaw Gateway 使用设备配对机制来确保安全性。首次访问控制面板时，设备需要与 Gateway 完成配对握手。如果配对未完成或被阻塞，连接会被拒绝，日志中会出现：

reason: "not-paired"
code: 1008 reason: pairing required
`

⚠️ macOS 升级后的常见问题

重要： macOS 系统升级后，此问题很可能再次出现。原因包括：

    系统重置了网络权限 - macOS 升级后可能重置应用的网络访问权限

    设备标识符变化 - 系统升级可能导致设备指纹/标识符改变

    配对信息丢失 - Gateway 的配对状态可能因系统更新被清除

    服务重启 - 升级过程中 Gateway 服务被中断，需要重新配对

建议： 每次 macOS 升级后，如果控制面板无法连接，优先检查配对状态：

openclaw devices list
`

排查步骤

1. 检查 Gateway 运行状态

openclaw gateway status
`

正常输出示例：

`Runtime: running (pid 95807, state active)
RPC probe: ok
Listening: 127.0.0.1:18789
`

如果 Gateway 未运行，先启动它：

openclaw gateway start
`

2. 查看日志确认错误

tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i "pairing"
`

如果看到 pairing-required 或 not-paired 错误，说明是配对问题。

3. 检查待配对设备列表

openclaw devices list
`

输出示例：

`Pending (1)
┌──────────────────────────────────────┬──────────────┬──────────┬────────────┐
│ Request                              │ Device       │ Role     │ Age        │
├──────────────────────────────────────┼──────────────┼──────────┼────────────┤
│ 8e238d19-c27a-4d90-bdce-d180ba6bf878 │ Mac mini     │ operator │ just now   │
└──────────────────────────────────────┴──────────────┴──────────┴────────────┘
`

4. 批准配对请求

方法一：批准最近的请求（推荐）

openclaw devices approve --latest
`

方法二：批准指定请求 ID

openclaw devices approve &lt;requestId&gt;
`

成功输出：

`Approved 51991519449ac3ad9cc62bf5b7c5cfd35e5a1905c2540bd46376db6ac9873f52 (8e238d19-c27a-4d90-bdce-d180ba6bf878)
`

5. 刷新控制面板

配对批准后，刷新浏览器页面 (http://127.0.0.1:18789/)，应该可以正常连接了。

常用命令速查

命令
说明

openclaw devices list
查看待配对和已配对设备

openclaw devices approve --latest
批准最近的配对请求

openclaw devices approve &lt;id&gt;
批准指定请求

openclaw devices remove &lt;deviceId&gt;
移除已配对设备

openclaw devices clear
清空所有配对设备

openclaw gateway status
检查 Gateway 状态

openclaw logs
实时查看 Gateway 日志

其他可能的问题

如果 devices list 显示为空

可能是浏览器没有发起配对请求，尝试：

    清除浏览器缓存和 Cookie

    使用无痕/隐私模式访问控制面板

    重启 Gateway：openclaw gateway restart

如果配对后仍然连不上

    检查是否有防火墙阻止本地连接

    确认 Gateway 绑定地址：openclaw gateway status 应显示 bind=loopback

    查看完整日志：openclaw logs

多设备场景

如果你有多个设备需要配对，每个设备都会生成独立的配对请求。使用 openclaw devices list 查看所有待处理请求，然后逐个批准或使用 --latest 批准最新的。

安全提示

    只批准你认识的设备

    定期使用 openclaw devices list 审查已配对设备

    可疑设备可用 openclaw devices remove &lt;deviceId&gt; 移除

    如需全部重置：openclaw devices clear

最后更新： 2026-03-09

适用版本： OpenClaw 2026.3.8+

参考资料

    OpenClaw 官方文档

    OpenClaw GitHub 仓库

    OpenClaw 社区 Discord