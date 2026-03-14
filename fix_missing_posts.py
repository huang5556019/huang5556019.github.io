#!/usr/bin/env python3
import os

backup_dir = "/Users/aisling308/blog-backup"
new_dir = "/Users/aisling308/blog-new"

# 中证 500 文章
src1 = os.path.join(backup_dir, "2026-03-13", "中证 -500-指数分析报告 -2026-03-12.html")
dst1 = os.path.join(new_dir, "_posts", "2026-03-13-csi-500-index-analysis.md")

with open(src1, 'r', encoding='utf-8') as f:
    content = f.read()

with open(dst1, 'w', encoding='utf-8') as f:
    f.write("""---
layout: post
title: "中证 500 指数分析报告 -2026-03-12"
date: 2026-03-13 12:00:00 +0800
categories: [投资，分析]
tags: [中证 500, 指数]
---

""")
    f.write(content)

print(f"✅ 中证 500 文章创建成功：{dst1}")

# PlayCover 文章
src2 = os.path.join(backup_dir, "2022-11-12", "PlayCover-添加 ipa 源教程.html")
dst2 = os.path.join(new_dir, "_posts", "2022-11-12-playcover-ipa-source-tutorial.md")

with open(src2, 'r', encoding='utf-8') as f:
    content = f.read()

with open(dst2, 'w', encoding='utf-8') as f:
    f.write("""---
layout: post
title: "PlayCover 添加 ipa 源教程"
date: 2022-11-12 12:00:00 +0800
categories: [教程，macOS]
tags: [PlayCover, iOS, 教程]
---

""")
    f.write(content)

print(f"✅ PlayCover 文章创建成功：{dst2}")
