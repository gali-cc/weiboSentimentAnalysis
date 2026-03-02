from flask import Blueprint, jsonify, render_template, request
import pandas as pd
from snownlp import SnowNLP



from weiboanalysis.dao import articleDao, commentDao
from weiboanalysis.util import wordcloudUtil

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')

@pb.route('/home')
def home():
    """
    首页, 获取相应数据
    """
    articleData = articleDao.get7DayArticleCount() or []
    if articleData:
        xAxis7ArticleData, yAxis7ArticleData = zip(*articleData)
        xAxis7ArticleData = list(xAxis7ArticleData)
        yAxis7ArticleData = list(yAxis7ArticleData)
    else:
        xAxis7ArticleData, yAxis7ArticleData = [], []

    # 获取文章类型数量
    articleTypeAmount = articleDao.getArticleTypeAmount() or []
    arcTypeData = []
    for row in articleTypeAmount:
        arcTypeData.append({
            'name': row[0],
            'value': row[1]
        })
    
    # 获取Top50评论用户, 生成词云图
    topCommentUsers = commentDao.getTopCommentUsers()
    commentUser_str = ' '.join(topCommentUsers) # 转换为字符串 空格分隔
    wordcloudUtil.genWordCloudPic(commentUser_str, maskImg='weiboanalysis/static/image/comment_mask.jpg',
                                  outImg='comment_user_cloud.jpg')
    
    # 获取最近7天的评论数量
    commentAmount = commentDao.getCommentAmount() or []
    commentData = []
    for row in commentAmount:
        commentData.append({
            'name': row[0],
            'value': row[1]
        })
    


    return render_template('index.html', xAxis7ArticleData=xAxis7ArticleData, yAxis7ArticleData=yAxis7ArticleData,
                           arcTypeData=arcTypeData, commentData=commentData)

@pb.route('/homePageData', methods=['GET'])
def getHomePageData():
    """
    获取首页数据 ajax异步交互 前端每隔5分钟请求一次 实时数据
    """
    totalArticle = articleDao.getTotalArticleCount()
    topAuthor = articleDao.getTopAuthor()
    topRegion = articleDao.getTopRegion()
    topArticles = articleDao.getArticleTopZan()
    return jsonify({
        'totalArticle': totalArticle,
        'topAuthor': topAuthor,
        'topRegion': topRegion,
        'topArticles': topArticles
    })

@pb.route('/hotWord')
def hotWord():
    """
    热词分析统计
    """
    # 读取评论分词文件, 前100条数据
    hotWordList = []
    # 读取评论分词文件, 前100条数据
    df = pd.read_csv('weiboanalysis/fenci/comment_fre.csv', nrows=100)

    for row in df.values:
        hotWordList.append(row[0])

    # select触发请求 获取请求参数 word
    defaultHotWord = request.args.get('word', default=hotWordList[0])
    
    hotWordNum = 0
    for row in df.values:
        if defaultHotWord == row[0]:
            hotWordNum = row[1]
            break

    # 情感分析
    stc = SnowNLP(defaultHotWord).sentiments
    if stc > 0.6:
        sentiments = '正面'
    elif stc < 0.2:
        sentiments = '负面'
    else:
        sentiments = '中性'

    # 获取日期用户评论中热词数量
    commentHotWordAmount = commentDao.getCommentHotWordAmount(defaultHotWord) or []
    if commentHotWordAmount:
        xAxisCommentData, yAxisCommentData = zip(*commentHotWordAmount)
        xAxisCommentData = list(xAxisCommentData)
        yAxisCommentData = list(yAxisCommentData)
    else:
        xAxisCommentData, yAxisCommentData = [], []

    # 获取评论中包含热词的评论
    commentList = commentDao.getCommentByHotWord(defaultHotWord) or []
    
    return render_template('hotWord.html',
                           hotwordList=hotWordList,
                           defaultHotWord=defaultHotWord,
                           hotWordNum=hotWordNum,
                           sentiments=sentiments,
                           xAxisCommentData=xAxisCommentData,
                           yAxisCommentData=yAxisCommentData,
                           commentList=commentList)

@pb.route('/articleData', methods=['GET'])
def articleData():
    """
    获取所有文章数据
    """
    articleList = articleDao.getAllArticle() or []

    for article in articleList:
        text = article[1] if len(article) > 1 else None
        if not text:
            sentiments = '中性'
        else:
            stc = SnowNLP(text).sentiments
            if stc > 0.6:
                sentiments = '正面'
            elif stc < 0.2:
                sentiments = '负面'
            else:
                sentiments = '中性'
        article.append(sentiments)
    return render_template('articleData.html', articleList=articleList)

@pb.route('/articleDataAnalysis', methods=['GET'])
def articleDataAnalysis():
    """
    微博文章数据分析
    """
    df = pd.read_csv('weiboanalysis/spider/arcType_data.csv')
    arcTypeList = []
    for row in df.values:
        arcTypeList.append(row[0])
    
    # 获取请求中的arcType 参数  or 默认为第一个文章类型
    defaultArcType = request.args.get('arcType', default=arcTypeList[0])
    # 根据文章类型获取文章
    articleList = articleDao.getArticleByArcType(defaultArcType) or []
    xDzData = [] # 点赞x轴
    xPlData = [] # 评论x轴
    xZfData = [] # 转发x轴
    rangeNum = 1000
    rangeNum2 = 100
    for item in range(0, 10):
        xDzData.append(str(item * rangeNum) + '-' + str((item + 1) * rangeNum))
        xPlData.append(str(item * rangeNum) + '-' + str((item + 1) * rangeNum))
    for item in range(0, 20):
        xZfData.append(str(item * rangeNum2) + '-' + str((item + 1) * rangeNum2))
    xDzData.append('1W+')
    xPlData.append('1W+')
    xZfData.append('2K+')
    yDzData = [0 for item in range(0, len(xDzData))] # 点赞y轴
    yPlData = [0 for item in range(0, len(xPlData))] # 评论y轴
    yZfData = [0 for item in range(0, len(xZfData))] # 转发y轴
    # 统计点赞数量, 评论数量, 转发数量
    for article in articleList:
        # 统计点赞数量
        for i in range(0, len(xDzData)):
            if article[4]  < rangeNum * (i + 1):
                yDzData[i] += 1
                break
            elif article[4] >= 10000:
                yDzData[-1] += 1
                break
        # 统计评论数量
        for i in range(0, len(xPlData)):
            if article[3]  < rangeNum * (i + 1):
                yPlData[i] += 1
                break
            elif article[3] >= 10000:
                yPlData[-1] += 1
                break
        # 统计转发数量
        for i in range(0, len(xZfData)):
            if article[2]  < rangeNum2 * (i + 1):
                yZfData[i] += 1
                break
            elif article[2] >= 2000:
                yZfData[-1] += 1
                break


    return render_template('articleDataAnalysis.html',
                            arcTypeList=arcTypeList,
                            defaultArcType=defaultArcType,
                            xDzData=xDzData,
                            yDzData=yDzData,
                            xPlData=xPlData,
                            yPlData=yPlData,
                            xZfData=xZfData,
                            yZfData=yZfData)

@pb.route('/commentDataAnalysis', methods=['GET'])
def commentDataAnalysis():
    """
    微博评论数据分析
    """

    commentList = commentDao.getAllComment() or []
    xDzData = [] # 点赞x轴
    rangeNum = 5
    for item in range(0, 20):
        xDzData.append(str(item * rangeNum) + '-' + str((item + 1) * rangeNum))
    xDzData.append('100+')
    yDzData = [0 for item in range(0, len(xDzData))] # 点赞y轴

    genderDict = {'男': 0, '女': 0}
    # 统计点赞数量
    for comment in commentList:
        # 统计点赞数量
        for i in range(0, len(xDzData)):
            if comment[4]  < rangeNum * (i + 1):
                yDzData[i] += 1
                break
            elif comment[4] >= 100:
                yDzData[-1] += 1
                break
        # 统计性别
        genderDict[comment[8]] += 1

    genderData = [{'name': x[0], 'value': x[1]} for x in genderDict.items()]

    # 用户评论词云图 前50个词
    df = pd.read_csv('weiboanalysis/fenci/comment_fre.csv', nrows=50)
    hotCommentWordList = [x[0] for x in df.values]
    comment_str = ' '.join(hotCommentWordList) # 空格连接成字符串
    # 生成词云图
    wordcloudUtil.genWordCloudPic(comment_str, 'weiboanalysis/static/image/comment_mask.jpg', 'comment_cloud.jpg')


    return render_template('commentDataAnalysis.html',
                            xDzData=xDzData,
                            yDzData=yDzData,
                            genderData=genderData)

@pb.route('/articleCloud', methods=['GET'])
def articleCloud():
    """
    微博文章词云图
    """
    # 获取文章词云图 前50个词
    df = pd.read_csv('weiboanalysis/fenci/article_fre.csv', nrows=50)
    hotArticleWordList = [x[0] for x in df.values]
    article_str = ' '.join(hotArticleWordList) # 空格连接成字符串
    # 生成词云图
    wordcloudUtil.genWordCloudPic(article_str, 'weiboanalysis/static/image/article_mask.jpg', 'article_cloud.jpg')

    return render_template('articleCloud.html')


@pb.route('/commentCloud', methods=['GET'])
def commentCloud():
    """
    微博评论词云图
    """
    # 获取评论词云图 前50个词
    df = pd.read_csv('weiboanalysis/fenci/comment_fre.csv', nrows=50)
    hotCommentWordList = [x[0] for x in df.values]
    comment_str = ' '.join(hotCommentWordList) # 空格连接成字符串
    # 生成词云图
    wordcloudUtil.genWordCloudPic(comment_str, 'weiboanalysis/static/image/comment_mask.jpg', 'comment_cloud.jpg')

    return render_template('commentCloud.html')

@pb.route('/commentUserCloud', methods=['GET'])
def commentUserCloud():
    """
    微博评论用户词云图
    """
    # 获取Top50评论用户, 生成词云图
    topCommentUsers = commentDao.getTopCommentUsers() or []
    commentUser_str = ' '.join(topCommentUsers) # 转换为字符串 空格分隔
    wordcloudUtil.genWordCloudPic(commentUser_str, maskImg='weiboanalysis/static/image/comment_mask.jpg',
                                  outImg='comment_user_cloud.jpg')
    
    return render_template('commentUserCloud.html')


@pb.route('/ipDataAnalysis', methods=['GET'])
def ipDataAnalysis():
    """
    微博评论用户IP地址分布
    """
    # 获取文章IP数据
    articleIPData = articleDao.getArticleIPData() or []
    # 转换为地图数据格式
    articleMapData = []
    for item in articleIPData:
        articleMapData.append({'name': item[0], 'value': item[1]})

    # 获取评论IP数据
    commentIPData = commentDao.getCommentIPData() or []
    # 转换为地图数据格式
    commentMapData = []
    for item in commentIPData:
        commentMapData.append({'name': item[0], 'value': item[1]})

    return render_template('ipDataAnalysis.html',
                           articleIPData=articleMapData,
                           articleMaxValue=articleMapData[0]['value'],
                           commentIPData=commentMapData,
                           commentMaxValue=commentMapData[0]['value'])

# 微博舆情分析 sentiments
@pb.route('/sentimentAnalysis', methods=['GET'])
def sentimentsAnalysis():
    """
    微博舆情分析
    """
    # 情感分析
    commentList = pd.read_csv('weiboanalysis/fenci/comment_fre.csv', nrows=200)
    xCommentSentimentData = ['正面', '中性', '负面'] # 情感x轴
    yCommentSentimentData = [0 for item in range(0, 3)] # 情感y轴
    for item in commentList.values:
        stc = SnowNLP(item[0])
        if stc.sentiments > 0.6:
            yCommentSentimentData[0] += 1
        elif stc.sentiments < 0.2: 
            yCommentSentimentData[2] += 1
        else:
            yCommentSentimentData[1] += 1   

    # 情感分析 文章
    articleList = pd.read_csv('weiboanalysis/fenci/article_fre.csv', nrows=200)
    xArticleSentiment = ['正面', '中性', '负面'] # 情感x轴
    yArticleSentiment = [0 for item in range(0, 3)] # 情感y轴
    for item in articleList.values:
        stc = SnowNLP(item[0])
        if stc.sentiments > 0.6:
            yArticleSentiment[0] += 1
        elif stc.sentiments < 0.2: 
            yArticleSentiment[2] += 1
        else:
            yArticleSentiment[1] += 1  
    
    artticleHotWordSentmentList = [{'name': x, 'value': y} for x, y in zip(xArticleSentiment, yArticleSentiment)]
    commentHotWordSentmentList = [{'name': x, 'value': y} for x, y in zip(xCommentSentimentData, yCommentSentimentData)]
    
    # 热词分析 Top15
    xHotWordTop15Data = []
    yHotWordTop15Data = []

    for i in range(14, -1, -1):
        xHotWordTop15Data.append(commentList.values[i][0])
        yHotWordTop15Data.append(commentList.values[i][1])
    

    return render_template('sentimentAnalysis.html',
                            xCommentSentimentData=xCommentSentimentData,
                            yCommentSentimentData=yCommentSentimentData,
                            artticleHotWordSentmentList=artticleHotWordSentmentList,
                            commentHotWordSentmentList=commentHotWordSentmentList,
                            xHotWordTop15Data=xHotWordTop15Data,
                            yHotWordTop15Data=yHotWordTop15Data)
