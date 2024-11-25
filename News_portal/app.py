from flask import Flask, render_template, abort  
from datetime import datetime  

app = Flask(__name__)  

# Пример данных новостей  
news_articles = [  
    {  
        'id': 1,  
        'title': 'Ужасная редиска в новостях',  
        'content': 'Редиска - это плохое слово!',  
        'date': datetime(2024, 11, 20)  
    },  
    {  
        'id': 2,  
        'title': 'Служба доставки редиски',  
        'content': 'Сегодня мы будем говорить о редиске.',  
        'date': datetime(2024, 11, 22)  
    },  
]  

# Список ругательств  
censored_words = ['редиска', 'редиски', 'редиске']  

# Фильтр для цензурирования  
def censor(text):  
    if not isinstance(text, str):  
        raise ValueError("filter censor должен применяться только к строкам")  
    for word in censored_words:  
        # Создание замены  
        replacement = word[0] + '*' * (len(word) - 1)  
        text = text.replace(word, replacement)  
    return text  

@app.route('/news/')  
def news_list():  
    # Сортировка новостей по дате  
    sorted_news = sorted(news_articles, key=lambda x: x['date'], reverse=True)  
    return render_template('news_list.html', news=sorted_news)  

@app.route('/news/<int:news_id>/')  
def news_detail(news_id):  
    article = next((article for article in news_articles if article['id'] == news_id), None)  
    if article is None:  
        abort(404)  # вернуть 404, если статья не найдена  
    # Цензурирование заголовка и содержания  
    article['title'] = censor(article['title'])  
    article['content'] = censor(article['content'])  
    formatted_date = article['date'].strftime('%d.%m.%Y')  
    return render_template('news_detail.html', article=article, date=formatted_date)  

if __name__ == '__main__':  
    app.run(debug=True)