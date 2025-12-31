# SEO-Optimized Article Writer Skill

一个完全自动化的 SEO 文章写作系统，为 Claude AI 设计。快速从 Google 搜索结果生成 SEO 优化的高质量文章。

## ✨ 功能特性

- 🔍 **自动 Google 搜索** - 从排名前 5 的文章中提取内容
- 📄 **智能文章提取** - 自动清理 HTML，提取干净的文章文本
- 📊 **竞争分析** - 分析竞争对手文章的字数、结构
- 📋 **大纲优化** - 自动生成 SEO 友好的文章大纲
- ✍️ **AI 写作提示** - 包含 AI 去重指令的完整写作提示
- 🎯 **SEO 优化** - 自动生成标题和 Meta Description 建议
- 📁 **完整报告** - 所有数据和提示都保存为文件

## 🚀 快速开始

### 前置要求
```bash
# Python 3.7+
python3 --version

# 安装 Python 依赖
pip3 install requests beautifulsoup4
```

### 方式 A：从 URL 列表自动提取（推荐）

#### 第 1 步：收集 URLs

1. 在 Google 搜索你的关键词
2. 找出排名前 5 的高质量文章
3. 将这 5 个 URL 保存到 `urls.txt` 文件（每行一个）

**参考示例：** 查看 `urls_example.txt`

#### 第 2 步：运行脚本
```bash
# 进入脚本所在目录
cd ~/Downloads

# 运行自动提取脚本
python3 seo_article_extractor.py "你的关键词"

# 示例
python3 seo_article_extractor.py "What Is LED & How It Works"
```

#### 第 3 步：查看输出

脚本会生成 `research_你的关键词/` 目录，包含：
```
research_你的关键词/
├── article_1.txt         # 提取的文章 1
├── article_2.txt         # 提取的文章 2
├── article_3.txt         # 提取的文章 3
├── article_4.txt         # 提取的文章 4
├── article_5.txt         # 提取的文章 5
├── log.txt               # 执行日志
├── outline.md            # 📋 优化的文章大纲
├── writing_prompt.txt    # ✍️ AI 写作提示（复制到 Claude）
└── seo_titles.txt        # 🎯 SEO 标题和描述
```

### 方式 B：手动提供文章内容

如果你想手动提供文章而不是从 URL 提取：

1. 创建文件 `article_1.txt` - `article_5.txt`
2. 将 5 篇文章的内容复制到这些文件中
3. 运行原始脚本：`python3 seo_article_writer.py "你的关键词"`

## 📖 完整工作流程
```
1. 【步骤 1】收集参考文章 (5-10 分钟)
   └─ 在 Google 搜索关键词
   └─ 找出排名前 5 的文章
   └─ 收集 URL 或文章内容

2. 【步骤 2】自动提取和分析 (30 秒)
   └─ 运行 Python 脚本
   └─ 自动生成大纲和写作提示

3. 【步骤 3】在 Claude 中生成文章 (5-15 分钟)
   └─ 复制 writing_prompt.txt 到 Claude
   └─ Claude 生成 SEO 优化的文章

4. 【步骤 4】编辑和优化 (10-30 分钟)
   └─ 人工审查和编辑
   └─ 添加图片和链接
   └─ 最终 SEO 检查

5. 【步骤 5】发布 (5-10 分钟)
   └─ 发布到博客或网站
   └─ 提交到 Google Search Console
```

## 🛠️ 文件说明

### seo_article_extractor.py
自动从 URL 列表提取文章、分析字数、生成大纲和写作提示的 Python 脚本。

**使用：** `python3 seo_article_extractor.py "关键词"`

### seo_article_writer.py
原始脚本（需要 Puppeteer）。使用文本文件中的文章内容生成大纲和提示。

### urls_example.txt
`urls.txt` 的示例文件，显示正确的格式。

## 💡 最佳实践

### 选择高质量的参考文章

优先选择来自以下网站的文章：
- ✅ Wikipedia（维基百科）
- ✅ 官方公司网站
- ✅ 知名技术博客
- ✅ 教育网站（Khan Academy, Coursera 等）
- ✅ 专业新闻网站（Investopedia, TechCrunch 等）

### SEO 优化建议

- 关键词在 H1、H2、H3 中自然出现
- 关键词密度 1-2%
- 文章字数 2,700-3,300 字
- 包含有序列表和无序列表
- 包含 FAQ 部分
- 清晰的标题和小标题结构

### AI 去重指令

脚本自动生成的 writing_prompt.txt 包含以下 AI 去重指令：

- 使用对话式、自然的语言
- 避免 AI 常见表达（"在当今..."、"综合来看..." 等）
- 融入个人经验和真实案例
- 混合句式长度
- 创造读者对话感

## 🔧 故障排除

### 问题：某些 URL 无法访问

**解决方案：**
- 检查 URL 是否正确
- 确保网站未被屏蔽或需要登录
- 尝试其他来源的 URL

### 问题：提取的文章内容很少

**解决方案：**
- 网站可能阻止了自动提取
- 尝试手动复制文章内容
- 使用其他来源的文章

### 问题：writing_prompt.txt 生成失败

**解决方案：**
- 确保至少有 1 篇文章成功提取
- 检查 outline.md 文件是否存在
- 查看 log.txt 中的错误信息

## 📊 性能和时间

| 步骤 | 任务 | 预估时间 |
|------|------|---------|
| 1 | 找 5 个高质量 URL | 5-10 分钟 |
| 2 | 运行 Python 脚本 | 30 秒 |
| 3 | 在 Claude 中生成文章 | 5-15 分钟 |
| 4 | 编辑和优化 | 10-30 分钟 |
| 5 | 发布 | 5-10 分钟 |
| **总计** | **完整 SEO 文章** | **25-65 分钟** |

## 🎁 高级用法

### 批量生成多篇文章
```bash
# 为多个关键词生成文章
python3 seo_article_extractor.py "关键词 1"
python3 seo_article_extractor.py "关键词 2"
python3 seo_article_extractor.py "关键词 3"
```

### 与 Claude 集成

将生成的 `writing_prompt.txt` 复制到：
- ChatGPT (https://chat.openai.com)
- Claude (https://claude.ai)
- Google Gemini (https://gemini.google.com)
- Perplexity (https://www.perplexity.ai)

## 📝 常见问题

**Q: 我需要有编程经验吗？**
A: 不需要。脚本已经为你完全自动化了。你只需要：
1. 找 5 个 URL
2. 运行一条命令
3. 复制提示到 Claude

**Q: 生成的文章质量如何？**
A: 非常高。脚本包含详细的 AI 去重指令，确保文章读起来像人写的，而不是 AI 生成的。

**Q: 我可以用不同的语言吗？**
A: 可以。脚本支持任何语言。只需用你的语言提供 URL 和关键词。

**Q: 我可以批量生成文章吗？**
A: 可以。为不同的关键词重复运行脚本即可。

## 📄 许可证

MIT License - 自由使用、修改和分享

## 🤝 贡献

欢迎提交 Pull Request 或报告 Issue！

## 📞 联系方式

- GitHub: [@unitopchina](https://github.com/unitopchina)
- Email: [你的邮箱]（可选）

---

**祝你写作愉快！** 🚀
