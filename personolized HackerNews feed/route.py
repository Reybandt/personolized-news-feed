from bottle import route, run, template, request, redirect
from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from cleaner import clean

@route("/news")
def news_list():
	s = session()
	rows = s.query(News).filter(News.label == None).all()
	return template('news_template', rows=rows)

@route("/add_label/")
def add_label():
	s = session()
	news_id = request.query.id
	news_label = request.query.label
	curr_news = s.query(News).filter(News.id == news_id)
	curr_news.update({'label': news_label})
	s.commit()
	redirect("/news")

@route("/update_news")
def update_news():
	news = get_news(url="https://news.ycombinator.com/", n_pages=1)
	s = session()
	for i in news:
		if s.query(News).filter(News.title == i['title'], News.author == i['author']).first():
			break
		else:
			s.add(News(**i))
	s.commit()
	redirect("/news")

@route("/recommendations")
def recommendations():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    classified_news = []
    prediction = []
    for i in rows:
        prediction.append(model.predict(clean(i.title)))
    for j in range(len(prediction)):
        if prediction[j] == ['good']:
            classified_news.append(rows[j])
        else:
            break
    return template('news_recommendations', rows=classified_news)


if __name__ == '__main__':
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    X_train = [clean(row.title) for row in rows]
    y_train = [row.label for row in rows]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    
    run(host="localhost", port=8080)