# 运行方式

- Flask：
  - uv run python -m weiboanalysis.app
  - uv run flask --app weiboanalysis.app --debug run
  - uv run python -m flask --app app --debug run --host 127.0.0.1 --port 5000
- 爬虫：
  - uv run python -m weiboanalysis.spider.arcType_spider
  - uv run python -m weiboanalysis.spider.article_spider
  - uv run python -m weiboanalysis.spider.comment_spider
  - uv run python -m weiboanalysis.spider.main
- 分词
  - uv run python -m weiboanalysis.fenci.commentFenci
  - uv run python -m weiboanalysis.fenci.articleFenci
- 情感分析
  - uv run python -m weiboanalysis.npl.snowNLPTest
- 词云
  - uv run python -m weiboanalysis.wordcloud.wordcloudTest

# 项目初次运行

- 数据库：
  - 首次运行项目时，需要先创建数据库。。
  - 数据库连接文件为：weiboanalysis.db
  - 数据库sql文件: db_weibo.sql
- 爬虫：
  - 首次运行项目时，需要先运行爬虫，将数据爬取到数据库中。
  - 运行顺序：
    - 先运行 spider/arcType_spider，将文章类型爬取到csv文件。

    ```
    uv run python -m weiboanalysis.spider.arcType_spider
    ```

    - 再运行 spider/main，将文章，评论爬取到数据库中。

    ```
    uv run python -m weiboanalysis.spider.main
    ```

- 分词：
  - 运行分词，将文章，评论进行分词。
  - 运行顺序：
    - 先运行 commentFenci，将评论分词到csv中。

    ```
    uv run python -m weiboanalysis.fenci.commentFenci
    ```

    - 再运行 articleFenci，将文章分词到csv文件中。

    ```
    uv run python -m weiboanalysis.fenci.articleFenci
    ```

- 启动项目
  - 启动Flask项目，访问 http://127.0.0.1:5000/user/login 即可。
  ```
  uv run python -m weiboanalysis.app
  ```
