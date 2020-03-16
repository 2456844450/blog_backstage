
from flask import request,jsonify

from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User
from app.models.base import db


from sqlalchemy import desc


from app import create_app
from . import web
from datetime import datetime
app = create_app()

@web.route('/api/article/getallarticle', methods=['GET'])
def getallarticle():
    page_index = request.args.get('page_index')
    if page_index is not None:
        page_index = int(page_index)
        pagesize = 20
        paginate = Article.query.filter_by(state=1).paginate(page_index, pagesize, error_out=False)
        total = paginate.total
        query = paginate.items
        data = []
        for article in query:
            data.append({
                'index': pagesize * (page_index - 1) + query.index(article) + 1,
                'id': article.id,
                'title': article.title,
                'desc': article.desc,
                'tags': article.tags,
                'keyword': article.keyword
            })
        return jsonify({
            'code': 200,
            'message': '得到所有文章信息成功',
            'data': data,
            'total': total,
            'pagesize': pagesize
        })
    return jsonify({
        'code': 200,
        'message': '小可爱别瞎玩哦~',
        'data': 0
    })

@web.route('/api/article/deletearticle', methods=['POST'])
def deletearticle():
    form = request.form
    id = form['id']
    if id is not None:
        id = int(id)
        if request.method == 'POST':
            with db.auto_commit():
                article = Article.query.filter_by(id=id).first()
                db.session.delete(article)
            return jsonify({
                'code': 200,
                'message': '删除文章成功'
            })
    return jsonify({
        'code': 200,
        'message': '小可爱别瞎搞哦~'
    })

@web.route('/api/article/addArticle', methods=['POST'])
def addArticle():
    form = request.form
    # 计算字数  就是计算字符串的长度
    numbers = len(form['content'])
    if request.method == 'POST':
        with db.auto_commit():
            article = Article()
            article.set_attrs(form)
            article.numbers = numbers
            db.session.add(article)
        return jsonify({
            'code': 200,
            'message': '写入文章成功'
        })

@web.route('/api/getArticleDetail', methods=['POST'])
def getArticleDetail():
    id = request.json['id']
    if id is not None:
        id = int(id)
        article = Article.query.filter_by(id=id).first()
        if article:
            views = article.views
            likes = article.likes
            comments = article.comments

            desc = article.desc

            numbers = article.numbers

            img_url = article.img_url

            state = article.state

            tags = article.tags

            tagArray = tags.split(',')

            tagList = []

            title = article.title

            content = article.content

            for tag in tagArray:
                tagList.append({
                    '_id': tagArray.index(tag),
                    'name': tag
                })

            # 評論  先把主評論都拿出來  再把每個主評論下的二級評論推進去
            maincomments = Comment.query.filter_by(state=1,article_id=id,to_uid=-1).all()

            commentsList = []

            for maincomment in maincomments:

                id = maincomment.id
                article_id = maincomment.article_id
                article_type = maincomment.article_type
                content = maincomment.content
                from_uid= maincomment.from_uid

                commentpeople = User.query.filter_by(id=from_uid).first()

                name = commentpeople.name
                type = commentpeople.type
                avatar = commentpeople.avatar
                user_id = commentpeople.id

                userMessage = {
                    'name': name,
                    'type': type,
                    'avatar': avatar,
                    'user_id': user_id
                }


                other_comments_array = []
                other_comments = Comment.query.filter_by(state=1, article_id=id, origin_uid= from_uid ).filter(Comment.to_uid != -1).all()

                for other_comment in other_comments:
                    other_comment_from_uid = other_comment.from_uid
                    other_comment_to_uid = other_comment.to_uid

                    from_uid_query = User.query.filter_by(id=other_comment_from_uid).first()
                    to_uid_query = User.query.filter_by(id=other_comment_to_uid).first()

                    user = {
                        'name': from_uid_query.name,
                        'type': from_uid_query.type,
                        'avatar': from_uid_query.avatar,
                        'user_id': from_uid_query.id
                    }

                    to_user = {
                        'name': to_uid_query.name,
                        'type': to_uid_query.type,
                        'avatar': to_uid_query.avatar,
                        'user_id': to_uid_query.id
                    }
                    other_comments_array.append({
                        'user': user,
                        'to_user': to_user,
                        'create_time': other_comment.create_datetime,
                        'contnet': other_comment.content
                    })

                commentsList.append({
                    'user': userMessage,
                    'content': maincomment.content,
                    'other_comments': other_comments_array,
                    'create_time': maincomment.create_datetime
                })

            return jsonify({
                'code': 0,
                'message': '请求文章列表成功',
                'data': {
                    'meta': {
                        'views':views,
                        'likes': likes,
                        'comments': comments
                    },
                    'desc': desc,
                    'numbers': numbers,
                    'img_url': img_url,
                    'state': state,
                    'tags': tagList,
                    'comments': commentsList,
                    '_id': id,
                    'title': title,
                    'author': 'azhou就是安州啊',
                    'content': content,
                    'create_time': article.create_datetime
                }

            })
    return jsonify({
        'code': 0,
        'message': '別瞎玩好不啦~',
        'data': {}
    })

@web.route('/api/getArticleList', methods=['GET'])
def getArticleList():
    article = request.args.get('article')
    if article is not None:
        article = int(article)
    keyword = request.args.get('keyword')
    likes = request.args.get('likes')
    state = int(request.args.get('state'))
    tag_id = request.args.get('tag_id')
    category_id = request.args.get('category_id')
    pageNum = int(request.args.get('pageNum'))
    pageSize = int(request.args.get('pageSize'))
    biglist = []
    # 如果article 為 1 按歸檔來查 先查年份  然後再查遞減查詢
    if pageNum is not None and pageSize is not None:
        if article == 1:
            currentyear = int(datetime.now().year)
            while currentyear >=2020:
                smalllist = []
                query = Article.query.filter_by(state=1, year=currentyear).order_by(Article.create_time.desc()).all()
                for article in query:
                    id = article.id
                    title = article.title
                    create_time = article.create_datetime
                    smalllist.append({
                        '_id': id,
                        'title': title,
                        'create_time': create_time
                    })
                if len(query) > 0:
                    biglist.append({
                        'year': currentyear,
                        'list': smalllist
                    })
                currentyear-=1
        else:
            paginate = Article.query.filter_by(state=1).order_by(Article.create_time.desc()).paginate(pageNum, pageSize, error_out=False)
            total = paginate.total
            query = paginate.items

            for article in query:
                id = article.id
                img_url = article.img_url
                title = article.title
                desc = article.desc
                views = article.views
                comments = article.comments
                likes = article.likes
                create_time = article.create_datetime
                biglist.append({
                    '_id': id,
                    'img_url': img_url,
                    'title': title,
                    'desc': desc,
                    'meta': {
                        'views': views,
                        'comments': comments,
                        'likes': likes
                    },
                    'create_time': create_time

                })
    return jsonify({
        'code': 0,
        'message': '请求文章列表成功',
        'data': {
            'list': biglist,
            'count': 100
        }

    })

@web.route('/api/getProjectList', methods=['GET'])
def getProjectList():
    keyword = request.args.get('keyword')
    pageNum = request.args.get('pageNum')
    pageSize = request.args.get('pageSize')
    if pageNum is not None:
        pageNum = int(pageNum)
    if pageSize is not None:
        pageSize = int(pageSize)
    projectList  = Article.query.filter_by(state=1, field=1).order_by(Article.create_time.desc()).all()

    list  = []
    for project in projectList:
        id = project.id
        title = project.project_name
        content = project.title
        img = project.img_url
        url = project.project_url
        start_time = project.start_time
        end_time = project.end_time

        list.append({
            'id': id,
            'title': title,
            'content': content,
            'img': img,
            'url': url,
            'start_time': start_time,
            'end_time': end_time
        })
    return jsonify({
        'code': 0,
        'message': '请求項目列表成功',
        'data': {
            'list': list,
            'count': 100
        }

    })
