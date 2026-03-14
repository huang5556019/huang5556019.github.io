#!/usr/bin/env python3
"""
Boss 博客文章迁移脚本
将旧博客的 HTML 文章转换为 Jekyll Markdown 格式
"""

import os
import re
import html
from pathlib import Path

# 配置
OLD_BLOG_DIR = os.path.expanduser("~/blog-backup")  # 旧博客目录
NEW_BLOG_DIR = os.path.expanduser("~/blog-new")  # 新博客目录 (cosy-jekyll-theme)
POSTS_DIR = os.path.join(NEW_BLOG_DIR, "_posts")

# 文章映射表 (旧文件名 -> 新文件名，不含扩展名)
POST_MAPPING = {
    # 2026 年文章
    "2026-03-13/中证 -500-指数分析报告 -2026-03-12.html": "2026-03-13-csi-500-index-analysis",
    "2026-03-13/github-trending-weekly.html": "2026-03-13-github-trending-weekly",
    "2026-03-09/OpenClaw-控制-UI-连接问题排查指南.html": "2026-03-09-openclaw-ui-troubleshooting",
    
    # 2022 年文章
    "2022-11-14/代码随想录读书笔记.html": "2022-11-14-code-thoughts-reading-notes",
    "2022-11-12/PlayCover-添加 ipa 源教程.html": "2022-11-12-playcover-ipa-source-tutorial",
    "2022-11-09/awesome-myself-tools.html": "2022-11-09-awesome-myself-tools",
    "2022-11-09/awesome-myself-remoteworks.html": "2022-11-09-awesome-myself-remoteworks",
    "2022-11-08/awesome-myself-books-doc.html": "2022-11-08-awesome-myself-books-doc",
    "2022-11-08/awesome-myself-cocoa.html": "2022-11-08-awesome-myself-cocoa",
    "2022-11-08/bookmarks-technical.html": "2022-11-08-bookmarks-technical",
}

# 分类映射 (根据文件名自动分类)
CATEGORY_MAP = {
    "github": ["GitHub", "开源"],
    "openclaw": ["OpenClaw", "工具"],
    "指数": ["投资", "分析"],
    "代码": ["编程", "学习"],
    "PlayCover": ["教程", "macOS"],
    "awesome": ["清单", "资源"],
    "bookmarks": ["收藏", "技术"],
}

def extract_title_from_html(html_content: str) -> str:
    """从 HTML 中提取标题"""
    # 尝试 h1 标签
    match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    
    # 尝试 title 标签
    match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        # 移除 " | Boss's Blog" 后缀
        title = re.sub(r'\s*\|\s*.*$', '', title)
        return title
    
    return "无标题"

def extract_body_from_html(html_content: str) -> str:
    """从 HTML 中提取正文内容"""
    # 尝试 article 标签
    match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        content = match.group(1)
    else:
        # 尝试 main 标签
        match = re.search(r'<main[^>]*>(.*?)</main>', html_content, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1)
        else:
            content = html_content
    
    # 移除脚本和样式
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.IGNORECASE | re.DOTALL)
    
    # 移除 HTML 标签，保留基本结构
    # 将 <br> 转换为换行
    content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
    # 将 <p> 转换为双换行
    content = re.sub(r'</p>\s*<p>', '\n\n', content, flags=re.IGNORECASE)
    content = re.sub(r'<p[^>]*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'</p>', '', content, flags=re.IGNORECASE)
    # 移除剩余的 HTML 标签
    content = re.sub(r'<[^>]+>', '', content)
    
    # 解码 HTML 实体
    content = html.unescape(content)
    
    # 清理空白
    content = re.sub(r'\n\s*\n', '\n\n', content)
    content = content.strip()
    
    return content

def guess_categories(filename: str) -> list:
    """根据文件名猜测分类"""
    categories = []
    filename_lower = filename.lower()
    
    for keyword, cats in CATEGORY_MAP.items():
        if keyword.lower() in filename_lower:
            categories.extend(cats)
            break
    
    if not categories:
        categories = ["随笔"]
    
    return categories

def create_front_matter(title: str, date_str: str, categories: list) -> str:
    """创建 Jekyll Front Matter"""
    return f"""---
layout: post
title: "{title}"
date: {date_str} 12:00:00 +0800
categories: [{', '.join(categories)}]
tags: []
---

"""

def migrate_post(old_path: str, new_name: str) -> bool:
    """迁移单篇文章"""
    src = os.path.join(OLD_BLOG_DIR, old_path)
    dst = os.path.join(POSTS_DIR, f"{new_name}.md")
    
    if not os.path.exists(src):
        print(f"⚠️  文件不存在：{src}")
        return False
    
    # 读取旧文件
    with open(src, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取信息
    title = extract_title_from_html(html_content)
    body = extract_body_from_html(html_content)
    categories = guess_categories(old_path)
    
    # 从路径提取日期
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', old_path)
    date_str = date_match.group(1) if date_match else "2026-03-14"
    
    # 创建新文件
    front_matter = create_front_matter(title, date_str, categories)
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(body)
    
    print(f"✅ 迁移成功：{old_path} -> {new_name}.md")
    print(f"   标题：{title}")
    print(f"   分类：{categories}")
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("Boss 博客文章迁移工具")
    print("=" * 60)
    print()
    
    # 检查目录
    if not os.path.exists(OLD_BLOG_DIR):
        print(f"❌ 旧博客目录不存在：{OLD_BLOG_DIR}")
        print("请修改脚本中的 OLD_BLOG_DIR 配置")
        return
    
    if not os.path.exists(NEW_BLOG_DIR):
        print(f"❌ 新博客目录不存在：{NEW_BLOG_DIR}")
        print("请先克隆 cosy-jekyll-theme 模板")
        return
    
    # 迁移所有文章
    success_count = 0
    total_count = len(POST_MAPPING)
    
    for old_path, new_name in POST_MAPPING.items():
        if migrate_post(old_path, new_name):
            success_count += 1
        print()
    
    # 输出统计
    print("=" * 60)
    print(f"迁移完成：{success_count}/{total_count} 篇文章")
    if success_count == total_count:
        print("🎉 所有文章迁移成功!")
    else:
        print(f"⚠️  有 {total_count - success_count} 篇文章迁移失败")
    print("=" * 60)

if __name__ == "__main__":
    main()
