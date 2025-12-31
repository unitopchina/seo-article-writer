---
name: seo-optimized-article-writer
description: 完全自动化的企业级 SEO 文章写作系统。一键从 Google 搜索、文章提取、竞争分析、大纲优化、AI 驱动写作到 SEO 优化。
allowed-tools: Browser Automation, Python, JavaScript, Google Search, File Writing
version: 2.0
author: SEO Content Automation
license: MIT
---

# 🚀 SEO-Optimized Article Writer Skill

## 简介

这是一个完全自动化的 SEO 文章写作系统。只需输入一个关键词，系统会自动：

1. 🔍 在 Google 搜索排名前 5 的文章
2. 📄 提取所有文章的干净内容
3. 📊 分析文章字数和给出建议
4. 📋 生成最优的文章大纲
5. ✍️ 生成 AI 写作提示（包含 AI 去重指令）
6. 🎯 生成 SEO 优化的标题和描述

## 如何使用

### 快速开始
```bash
# 1. 安装依赖
npm install puppeteer
pip3 install beautifulsoup4 trafilatura requests

# 2. 保存 Python 脚本为 seo_article_writer.py

# 3. 运行脚本
python3 seo_article_writer.py "你的关键词"
```

### 输出文件

脚本会生成：
- 5 篇参考文章内容
- 字数分析报告
- 最优文章大纲
- AI 写作提示（可直接用于 ChatGPT/Claude）
- SEO 优化的标题和描述

## 完整 Python 脚本

[见下面的 seo_article_writer.py 文件]

## 最佳实践

✅ 第一步完成后，检查提取的文章质量
✅ 获得 AI 写作提示后，复制到 ChatGPT/Claude
✅ 初稿生成后，进行人工编辑和优化
✅ 发布前使用 SEO 工具验证

## 常见问题

**Q: Puppeteer 安装失败？**
A: 可以手动打开 Google，复制排名前 5 的文章内容到文件。

**Q: 提取不到文章？**
A: 某些网站可能需要登录，可以手动复制粘贴。

## 许可证

MIT License
