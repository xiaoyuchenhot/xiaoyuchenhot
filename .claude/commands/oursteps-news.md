# 新足迹论坛热帖追踪

抓取新足迹论坛 (oursteps.com.au) 过去48小时内的热门帖子，聚焦中国新闻与战争新闻，生成中文摘要文档。

## 执行步骤

**第一步：获取以下版块的最新帖子列表**

使用 WebFetch 分别获取以下三个版块的第一页：
- 国际新闻 (fid=160): https://www.oursteps.com.au/bbs/forum.php?mod=forumdisplay&fid=160
- 新闻汇总 (fid=43): https://www.oursteps.com.au/bbs/forum.php?mod=forumdisplay&fid=43
- 澳洲和世界时政 (fid=124): https://www.oursteps.com.au/bbs/forum.php?mod=forumdisplay&fid=124

获取时请求：列出所有可见帖子的标题、TID、阅读数、回复数、发帖时间。

**第二步：筛选热帖**

从第一步结果中，筛选出满足以下所有条件的帖子：
- 发帖时间在今天日期往前48小时以内
- 阅读数 > 500，或回复数 > 20
- 内容涉及：中国新闻、中美关系、台海局势、战争局势（中东/乌克兰/伊朗/以色列等）

**第三步：获取帖子内容**

对每个筛选出的帖子，使用 WebFetch 访问：
`https://www.oursteps.com.au/bbs/forum.php?mod=viewthread&tid=<TID>`

提示词：请提取帖子标题（中文）、发帖时间、阅读数、回复数，以及原帖核心内容和主要讨论观点。

**第四步：生成中文摘要文档**

将所有摘要内容写入文件：`highlights/oursteps_news_<YYYY-MM-DD>.md`

文档格式如下：

```
# 新足迹论坛热帖摘要 — <日期>

> 数据来源：https://www.oursteps.com.au/bbs/forum.php
> 抓取范围：过去48小时 | 关注领域：中国新闻、战争动态

---

## 一、中国相关新闻

### [帖子标题]
- 链接：https://www.oursteps.com.au/bbs/forum.php?mod=viewthread&tid=<TID>
- 版块：<版块名> | 发帖时间：<时间> | 阅读：<数> | 回复：<数>
- **摘要**：<2-4句中文摘要>
- **论坛主要观点**：<简述讨论焦点>

---

## 二、战争与国际局势

### [帖子标题]
...

---

## 三、其他热门话题

### [帖子标题]
...

---

*文档由 /oursteps-news 指令自动生成*
```

**注意事项：**
- 所有文字输出使用中文（普通话/简体字）
- 摘要内容客观呈现，不加入个人评论
- 帖子按阅读量从高到低排列
- 若当天论坛无法访问，在文档中注明并记录错误原因
