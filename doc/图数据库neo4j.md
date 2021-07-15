### 2.6.1 图数据库概念

数据存储一直是人类长期研究的重要领域，关系型数据库[25]具备扎实的理论基础，它具备较高的安全性，而且经过多年的研究发展，关系型数据库的技术已经非常成熟了，它可以依赖简单的二维表结构来表达丰富的语义信息。但是随着数据量的加大，关系型数据库也表现出了其一直未能解决的瓶颈，那就是速度开始变慢，尤其是使用关联查询时，将耗费大量的资源，性能随之也会变差。另一方面，关系型数据库的事务机制也占用了大量的资源，因此越来越多的学者开始了对非关系型数据库（NoSQL[26]）的研究。

图数据库是非关系型数据库的一种，它可以很方便的将点、线、面等元素按照一定数据结构存储下来，如果需要表示不同事物之间的联系，关系型数据库需要进行关联查询才能实现，而图形数据库的优点在于它能直观的表示事物之间的关系。图数据库包括两种基本元素：结点（Node）和关系（Relationship）。使用结点表示现实世界的事物，即实体，实体可以有自己的属性（Property）；使用关系表示结点之间的联系，即实体与实体之间的联系，关系也可以具备自己的属性。

### 2.6.1 Neo4j图形数据库

neo4j的数据存储形式 主要是 **节点（node）和 边（edge）** 来组织数据。node可以代表知识图谱中的实体，edge可以用来代表实体间的关系，关系可以有方向，两端对应开始节点和结束节点。
另外，可以在node上加一个或多个**标签（Node Label）表示实体的分类**，以及一个键值对集合来表示该实体除了关系属性之外的一些额外属性。关系也可以附带额外的属性。Neo4j数据库是一个高性能的NoSQL图形数据库，它将结构化数据存储在网络而不是二维表中，是一个嵌入式的、基于磁盘的、具备完全的事务特性的Java持久化引擎[29]。Neo4j具备以下四个特征：

（1）高可用性：它可以很方便的集成到任何应用中，不会受到具体业务的约束。

（2）易扩展性：如果单个结点无法满足数据需求时，Neo4j的分布式集群部署支持可以解决这一问题。

（3）完整的数据库事务支持：数据库事务正确执行的四个基本要素是原子性、一致性、隔离性、持久性。Neo4j可以完整的支持这四个特性，保证数据的准确性。

（4）快速检索：可以通过Neo4j的遍历工具进行数据的快速检索。

Neo4j数据库是在java虚拟机的基础上进行开发的，因此要使用neo4j数据库的前提条件是安装了jdk，本文所使用的jdk版本是1.8。它的安装方法很简单，只需要根据提示同时neo4j也提供了一个desktop版操作页面供用户使用，默认访问地址为“127.0.0.1:7474”。

Cypher是Neo4j的官方查询语言，是一个类SQL语言，可以方便的对图形数据库进行查询和更新[30]。与SQL相比，Cypher语法简单，而且功能强大，很多SQL种无法解决的任务都可以用它来实现，它常用的子句有：

MATCH子句：通常用于匹配数据库中的数据。

WHERE子句：WHERE子句一般作为MATCH子句一部分，用于指定查询的条件。

RETURN子句：指定查询需要返回的内容。

CREATE子句：用于创建结点、关系、属性。

除了Cypher查询语言外，为了方便数据的导入Neo4j还支持数据的批量导入，同时也为java、python、javascript等语言提供了对应的API，方便编程人员直接调用和开发，本文所使用的是Neo4j为python提供的查询接口。





### 使用Python连接neo4j桌面版前，neo4j的界面简介和配置

详细步骤和说明：
1、打开neo4j桌面版。

2、点击“MyProject”。在Applications下是neo4j自带的浏览器neo4j Browser，在neo4j浏览器中，可以输入Cypher语句，来增删改查。点右边加号新建一个Graph。新建时，要求输入图名和密码，不输的话，默认名字和密码都是neo4j。

3、点击“Manage”，在Manage窗口中，选择“Settings”，按下修改配置

```python
# 去掉下面注释
dbms.connectors.default_listen_address=0.0.0.0  
dbms.connectors.bolt.enabled=true
dbms.connectors.bolt.tls_level=OPTIONAL
dbms.connectors.bolt.listen_address=:7687
dbms.connectors.http.enabled=true
dbms.connectors.http.listen_address=:7474
dbms.connectors.https.enabled=true
dbms.connectors.https.listen_address=:7473
dbms.directories.import=import
dbms.security.auth_enabled=true
dbms.memory.heap.initial_size=4Gg
dbms.memory.heap.max_size=15G
```

其余地方不需修改

4、点击“Manage”按钮右边的“Start”按钮，开启服务。

完成后，在自己的浏览器中输入“http://localhost:7474”，如果可以看到和neo4j自带浏览器中一样的界面，就可以使用python连接了。python需要借助py2neo进行连接，然后可以利用Cypher语句通过py2neo对neo4j图数据库进行增删改查等功能。

