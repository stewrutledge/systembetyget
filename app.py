from flask import Flask, render_template, request
from lib.systemet import fetch_rating, add_rating, query

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def cat_list():
    if request.method == 'GET':
        cat = request.args.get('cat', None)
        name = request.args.get('name', None)
        limit = request.args.get('limit', 25)
        search_term = request.args.get('searchterm', None)
        target = request.args.get('target', None)
        country = request.args.get('country', None)
        from_range = request.args.get('from', None)
        to_range = request.args.get('to', None)
        boolean = request.args.get('boolean', "OR")
        mobile = request.args.get('mobile', None)
        search_list = []
        if country:
            search_list.append('Ursprunglandnamn:' + country)
        if cat:
            search_list.append('Varugrupp:' + cat)
        if name:
            search_list.append('Namn:' + name)
        if search_term:
            search_list.append('_all:' + search_term)
        if len(search_list) == 0:
            search_string = str('_all:*')
        else:
            search_string = str(" " + boolean + " ").join(search_list)
        app.jinja_env.globals.update(fetch_rating=fetch_rating)
        if target and from_range and to_range:
            print search_string
            output = query(
                search_string, limit, target, from_range, to_range)
        else:
            output = query(search_string, limit)
        if mobile == 'true':
            return render_template('mobile_result.html', output=output)
        elif mobile != 'true':
            return render_template('index.html', output=output, mobile=mobile)
    elif request.method == 'POST':
        articleid = request.args.get('arid', None)
        rating = request.args.get('rating', None)
        #try:
        add_rating(articleid, rating)
        return "Updated post with %s %s \n" % (articleid, rating)
        #except:
        #    return "Could not update post with %s %s \n" % (articleid, rating)


@app.route('/mobile', methods=['GET'])
def render_mobile():
    return render_template('mobile.html')


if __name__ == '__main__':
    app.run(debug=True)
