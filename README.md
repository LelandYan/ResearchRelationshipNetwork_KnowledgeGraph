# 基于知识图谱的科研关系网络分析

> 本项目完成了构建科研关系网络知识图谱以及相关应用。构建知识图谱所用到数据均来自网络爬虫爬行的数据；并且可提取结构化、半结构化、非结构化数据的实体与实体之间的关系；数据的存储采用的开源图数据库 Neo4j 存储科研网络关系知识；本文同时使用 Django 、 Echart js 、 D3.js 和 Boostrap 实现一个具有信息检索、大数据分析、专家技术画像可视化和合作专家信息以及推荐功能网站，可以快速的了解相关领域和专家的相关信息 。

## 总体技术路线：

![](imgs\流程图.png)

## 项目功能模块以及相关效果图

* 主页面：

  ![](imgs\1.png)

  ![](imgs\2.png)

  主页面主要分为两个部分：

  第一部分为提供的搜索接口（可以支持作者名字搜索（拼音、汉字、英文）、研究领域搜（英文）、关键技术搜索（英文））

  第二部分为数据可视化分析，主要是分析数据库现存的数据，从左到右依次为，作者按照文章发表的数据和文章被引用的数据降序可视化，文章所属机构和投递的期刊会议所占比例问题，右侧是针对科研领域所发的文章数量降序排列展示，最后是一个词语，用于展示那些科研领域是比较热门（根据的是文章发表的数量）

* 副页面

  ![](imgs\3.png)

  ![](imgs\4.png)

  副页面主要分为两个部分：

  第一部分为可视化学科领域本体关系，就是展示不同领域的归属问题

  第二部分为通过上传的pdf文章来进行关系提取，并展示各个三元组之间的关系

* 搜索后跳转页面：

  ![](imgs\5.png)

  这里会列出搜索字段相关的作者列表，然后显示各个作者相关的基本信息

* 点击选择某作者后生成的专家技术画像

  ![](imgs\6.png)

  ![](imgs\7.png)

  ![](imgs\8.png)

  ![](imgs\9.png)

  本页面共分为8个部分：

  第一个部分是关于作者的相关信息和数据库收录的文章数量

  第二个部分是关于该作者发表过论文的领域

  第三个部分是该作者合作过的作者名称和合作的多少

  第四个部分是关于该作者用图数据库查询后得到与之相关的感兴趣领域、合作者、作者所属结构和发表的文章

  第五个部分是关于该作者推荐合作功能，推荐以后可能合作的作者对象以及可信度和作者相关信息

  第六个部分是关于作者信息补充，通过网络爬虫获得作者信息，并使用文本分类模型进行分类并展示

  第七个部分是作者的在不同年份的发布的文章，显示文章的名字

  第八个部分是作者发表文章的详细展示，展示数据库中文章的详细信息。

## 项目介绍

本项目希望提出一种分析科研关系网络的新方法，能够充分利用现在的 数据挖掘、文本主题提取 、文本聚类分析等计算机技术 。这种方法应该 建立 起“领域 —专家 ”模型 ，通过技术关键词能够直接找到擅长该项技术的 专家 ，并能够完整地了解每个 专家 的擅长技术、工作单位、国籍等详细信息 。并采用系统分析方法 可以建立起不同专家之间的合作网络， 尤其是一些跨学科，跨领域的合作关系，从而更好地了解目前的交叉学科现状 。最后能够 建立一个具有检索和数据分析功能的 科研关系网站，实现相关的数据展示 。

要有一个任务表和一个功能表。

## 目录结构

## 可复用资源

## 项目配置

## 项目不足

## 参考

[Agriculture_KnowledgeGraph](https://github.com/qq547276542/Agriculture_KnowledgeGraph)、[KGQA-Based-On-medicine](https://github.com/YeYzheng/KGQA-Based-On-medicine)、[KGQA_HLM](https://github.com/chizhu/KGQA_HLM)、[neo4j-prediction](https://github.com/mr-csj/neo4j-prediction)、[economic_audit_knowledge_graph](https://github.com/Guanngxu/economic_audit_knowledge_graph)、[ stock-knowledge-graph](https://github.com/lemonhu/stock-knowledge-graph)、[ DouBanRecommend](https://github.com/mattzheng/DouBanRecommend)、[Film-Recommendation-System](https://github.com/zut-cs-wangluo152/Film-Recommendation-System)、[ Taiwan-Stock-Knowledge-Graph](https://github.com/jojowither/Taiwan-Stock-Knowledge-Graph)、[AcaFinder](https://github.com/xyjigsaw/AcaFinder)

