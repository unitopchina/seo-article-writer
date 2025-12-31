#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import statistics

class SEOArticleAutomation:
    def __init__(self, keyword):
        self.keyword = keyword
        self.output_dir = f"research_{keyword.replace(' ', '_')}"
        Path(self.output_dir).mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.word_counts = []
        self.log_file = f"{self.output_dir}/log.txt"
        self._log(f"\\n{'='*80}")
        self._log(f"SEO Article Automation Started: {self.timestamp}")
        self._log(f"关键词：{self.keyword}")
        self._log(f"{'='*80}")
    
    def _log(self, message):
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\\n")
    
    def step1_google_search_and_extract(self):
        self._log(f"\\n{'='*80}")
        self._log("【步骤 1】Google 搜索 + 文章提取")
        self._log(f"{'='*80}\\n")
        
        search_url = f"https://www.google.com/search?q={quote(self.keyword)}"
        self._log(f"🔎 搜索 URL: {search_url}\\n")
        
        puppeteer_script = self._create_puppeteer_script(search_url)
        script_path = f"{self.output_dir}/google_search.js"
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(puppeteer_script)
        
        self._log(f"📝 脚本已生成: {script_path}")
        self._log(f"⏳ 正在执行... 请稍候（30-60 秒）\\n")
        
        try:
            result = subprocess.run(
                ['node', script_path],
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                self._log("✅ 搜索和提取完成！\\n")
                return True
            else:
                self._log(f"⚠️ 错误: {result.stderr}\\n")
                return False
        except Exception as e:
            self._log(f"❌ 错误: {e}\\n")
            return False
    
    def _create_puppeteer_script(self, search_url):
        return f"""
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {{
    let browser;
    try {{
        console.log('🚀 启动浏览器...');
        browser = await puppeteer.launch({{headless: true, args: ['--no-sandbox']}});
        
        const page = await browser.newPage();
        await page.setDefaultNavigationTimeout(30000);
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
        
        console.log('🔍 打开 Google...');
        await page.goto('{search_url}', {{waitUntil: 'networkidle2', timeout: 30000}});
        await page.waitForSelector('div.g', {{ timeout: 10000 }});
        
        console.log('📄 提取搜索结果...');
        
        const results = await page.evaluate(() => {{
            const items = document.querySelectorAll('div.g');
            const topResults = [];
            
            for (let i = 0; i < items.length; i++) {{
                if (topResults.length >= 5) break;
                
                const linkElem = items[i].querySelector('a[href]');
                const titleElem = items[i].querySelector('h3');
                
                if (linkElem && titleElem) {{
                    const url = linkElem.href;
                    const title = titleElem.innerText;
                    
                    if (!url.includes('google.com') && 
                        !url.includes('youtube.com') &&
                        url.startsWith('http')) {{
                        topResults.push({{position: topResults.length + 1, title, url}});
                    }}
                }}
            }}
            return topResults;
        }});
        
        console.log('\\\\n✅ 找到 ' + results.length + ' 篇文章');
        
        for (let i = 0; i < results.length; i++) {{
            console.log('\\\\n📥 提取文章 ' + (i + 1));
            
            try {{
                const articlePage = await browser.newPage();
                await articlePage.setDefaultNavigationTimeout(20000);
                await articlePage.goto(results[i].url, {{waitUntil: 'networkidle2', timeout: 20000}});
                
                const articleText = await articlePage.evaluate(() => {{
                    document.querySelectorAll('script, style, nav, footer, aside').forEach(el => el.remove());
                    const article = document.querySelector('article') || document.querySelector('main') || document.body;
                    return article ? article.innerText : '';
                }});
                
                const cleanText = articleText.split('\\\\n').filter(line => line.trim()).join('\\\\n');
                
                if (cleanText.length > 500) {{
                    fs.writeFileSync('article_' + (i + 1) + '.txt', cleanText, 'utf-8');
                    console.log('✅ 保存成功');
                }}
                
                await articlePage.close();
                await new Promise(resolve => setTimeout(resolve, 2000));
                
            }} catch (error) {{
                console.log('⚠️ 无法提取');
            }}
        }}
        
        console.log('\\\\n✅ 完成！');
        await browser.close();
        process.exit(0);
        
    }} catch (error) {{
        console.error('❌ 错误:', error.message);
        if (browser) await browser.close();
        process.exit(1);
    }}
}})();
"""
    
    def step2_word_count_analysis(self):
        self._log(f"\\n{'='*80}")
        self._log("【步骤 2】字数分析")
        self._log(f"{'='*80}\\n")
        
        articles = sorted(Path(self.output_dir).glob('article_*.txt'))
        
        if not articles:
            self._log("❌ 没有找到文章文件\\n")
            return 3000
        
        for i, path in enumerate(articles, 1):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            word_count = len(content.split())
            self.word_counts.append(word_count)
            self._log(f"  📄 文章 {i}: {word_count:,} 字")
        
        if self.word_counts:
            avg = statistics.mean(self.word_counts)
            median = statistics.median(self.word_counts)
            recommended = int((avg + median) / 2)
            
            self._log(f"\\n✅ 推荐字数: {recommended:,}\\n")
            return recommended
        
        return 3000
    
    def step3_outline_analysis(self):
        self._log(f"\\n{'='*80}")
        self._log("【步骤 3】生成最优大纲")
        self._log(f"{'='*80}\\n")
        
        outline = f"""# {self.keyword.title()}

## 简介
- 定义概念
- 为什么重要

## 好处
- 好处 1
- 好处 2

## 工作原理
- 概念 1
- 概念 2

## 最佳实践
- 实践 1
- 实践 2

## 常见错误
- 错误 1
- 错误 2

## 工具
- 工具 1
- 工具 2

## 常见问题
- Q1: ...?
- Q2: ...?

## 结论
- 总结
- 下一步
"""
        
        outline_path = f"{self.output_dir}/outline.md"
        with open(outline_path, 'w', encoding='utf-8') as f:
            f.write(outline)
        
        self._log("✅ 大纲已生成\\n")
        self._log(outline)
        return outline
    
    def step4_ai_writing_prompt(self, word_count, outline):
        self._log(f"\\n{'='*80}")
        self._log("【步骤 4】生成 AI 写作提示")
        self._log(f"{'='*80}\\n")
        
        prompt = f"""你是专业的 SEO 内容创作者。根据以下要求写一篇文章。

【要求】
- 关键词：{self.keyword}
- 字数：{word_count:,} 字
- 格式：Markdown

【大纲】
{outline}

【关键指令】
1. 避免 AI 风格
   - 说"我发现..."而不是"研究表明..."
   - 表达真实观点
   - 避免："在当今...","综合来看...","值得一提的是..."

2. 添加个人经验
   - 至少 2-3 个真实案例
   - 分享失败经历
   - 使用具体数字

3. 变化句式结构
   - 混合短句和长句
   - 每段 3-4 句
   - 段落开头用主题句

4. 创造对话感
   - 使用修辞性问题
   - 表达困惑和思考
   - 邀请读者思考

【SEO 优化】
- 关键词密度：1-2%
- 在前 100 字出现主关键词
- 在 H2/H3 中融入长尾词
- 包含列表和表格
- 包含 FAQ 部分

现在请写出这篇文章。字数 {int(word_count * 0.9)} - {int(word_count * 1.1)} 之间。"""
        
        prompt_path = f"{self.output_dir}/writing_prompt.txt"
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        self._log("✅ 写作提示已生成\\n")
        self._log("【复制下面内容到 ChatGPT 或 Claude】\\n")
        self._log("="*80)
        self._log(prompt)
        self._log("="*80 + "\\n")
        
        return prompt
    
    def step5_seo_titles(self):
        self._log(f"\\n{'='*80}")
        self._log("【步骤 5】生成 SEO 优化的标题和描述")
        self._log(f"{'='*80}\\n")
        
        keyword_title = self.keyword.title()
        
        titles = [
            f"The Ultimate {keyword_title} Guide: Complete Step-by-Step [2024]",
            f"How to {keyword_title}: Expert Strategies & Best Practices",
            f"What is {keyword_title}? Complete Beginner's Guide",
            f"{keyword_title} 101: Everything You Need to Know",
            f"Best {keyword_title} Tips: Proven Strategies from Experts",
        ]
        
        descriptions = [
            f"Learn {keyword_title} with our comprehensive guide. Discover strategies, best practices, examples, and expert tips.",
            f"Complete guide to {keyword_title}. Get step-by-step instructions, proven tactics, and professional insights.",
            f"Master {keyword_title} with our resource. Includes tips, tools, case studies, and everything you need.",
            f"Everything about {keyword_title} here. Guide, strategies, examples, and actionable advice.",
        ]
        
        self._log("📋 推荐 Page Title\\n")
        for i, title in enumerate(titles, 1):
            self._log(f"{i}. ({len(title)} 字) {title}\\n")
        
        self._log("📝 推荐 Meta Description\\n")
        for i, desc in enumerate(descriptions, 1):
            self._log(f"{i}. ({len(desc)} 字) {desc}\\n")
        
        with open(f"{self.output_dir}/seo_titles.txt", 'w', encoding='utf-8') as f:
            f.write("Page Titles\\n\\n")
            for i, title in enumerate(titles, 1):
                f.write(f"{i}. {title}\\n\\n")
            f.write("\\nMeta Descriptions\\n\\n")
            for i, desc in enumerate(descriptions, 1):
                f.write(f"{i}. {desc}\\n\\n")
    
    def run_all(self):
        self.step1_google_search_and_extract()
        word_count = self.step2_word_count_analysis()
        outline = self.step3_outline_analysis()
        self.step4_ai_writing_prompt(word_count, outline)
        self.step5_seo_titles()
        
        self._log(f"\\n{'='*80}")
        self._log("✅ 所有步骤完成！")
        self._log(f"{'='*80}")
        self._log(f"\\n📁 文件保存在：{self.output_dir}/\\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        keyword = input("请输入关键词：")
    else:
        keyword = " ".join(sys.argv[1:])
    
    automation = SEOArticleAutomation(keyword)
    automation.run_all()
