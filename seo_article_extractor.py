#!/usr/bin/env python3
"""
SEO Article Extractor - 简化版本
从 urls.txt 文件中读取 URL，自动提取文章内容
"""

import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import statistics

class SEOArticleExtractor:
    def __init__(self, keyword):
        self.keyword = keyword
        self.output_dir = f"research_{keyword.replace(' ', '_')}"
        Path(self.output_dir).mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.word_counts = []
        self.log_file = f"{self.output_dir}/log.txt"
        self._log(f"\\n{'='*80}")
        self._log(f"SEO Article Extractor Started")
        self._log(f"{'='*80}")
        self._log(f"时间：{self.timestamp}")
        self._log(f"关键词：{self.keyword}")
    
    def _log(self, message):
        """记录操作"""
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{message}\\n")
    
    def extract_from_urls(self):
        """从 urls.txt 中读取 URL 并提取文章"""
        self._log(f"\\n{'='*80}")
        self._log("【步骤 1】从 URLs.txt 提取文章内容")
        self._log(f"{'='*80}\\n")
        
        urls_file = "urls.txt"
        
        # 检查 urls.txt 是否存在
        if not Path(urls_file).exists():
            self._log(f"❌ 找不到 {urls_file} 文件")
            self._log(f"请在当前目录创建 urls.txt 文件，每行一个 URL")
            return False
        
        # 读取 URLs
        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            self._log(f"❌ 无法读取 urls.txt：{e}")
            return False
        
        self._log(f"📄 找到 {len(urls)} 个 URLs\\n")
        
        # 逐个提取文章
        for i, url in enumerate(urls[:5], 1):  # 最多处理前 5 个
            self._log(f"📥 正在提取文章 {i}: {url}")
            
            try:
                # 下载网页
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    # 使用 BeautifulSoup 解析 HTML
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # 移除不需要的元素
                    for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'form']):
                        element.decompose()
                    
                    # 提取文本
                    text = soup.get_text(separator='\\n')
                    
                    # 清理文本
                    lines = [line.strip() for line in text.split('\\n') if line.strip()]
                    clean_text = '\\n'.join(lines)
                    
                    # 保存文章
                    if len(clean_text) > 500:
                        file_path = f"{self.output_dir}/article_{i}.txt"
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(clean_text)
                        
                        word_count = len(clean_text.split())
                        self._log(f"✅ 成功提取：{word_count:,} 字\\n")
                    else:
                        self._log(f"⚠️ 内容过短，跳过\\n")
                else:
                    self._log(f"⚠️ HTTP {response.status_code}，无法访问\\n")
                    
            except Exception as e:
                self._log(f"⚠️ 错误：{str(e)}\\n")
        
        return True
    
    def analyze_word_count(self):
        """分析字数"""
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
    
    def generate_outline(self):
        """生成大纲"""
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
    
    def generate_writing_prompt(self, word_count, outline):
        """生成写作提示"""
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
        self._log("【下一步：复制提示内容到 Claude】\\n")
        self._log("="*80)
        self._log(prompt[:500] + "... [内容继续] ...")
        self._log("="*80 + "\\n")
        
        return prompt
    
    def run_all(self):
        """运行完整流程"""
        success = self.extract_from_urls()
        
        if not success:
            return
        
        word_count = self.analyze_word_count()
        outline = self.generate_outline()
        self.generate_writing_prompt(word_count, outline)
        
        self._log(f"\\n{'='*80}")
        self._log("✅ 所有步骤完成！")
        self._log(f"{'='*80}")
        self._log(f"\\n📁 文件保存在：{self.output_dir}/\\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        keyword = input("请输入关键词：")
    else:
        keyword = " ".join(sys.argv[1:])
    
    extractor = SEOArticleExtractor(keyword)
    extractor.run_all()