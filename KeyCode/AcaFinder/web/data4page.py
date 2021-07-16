# *_*coding:utf-8 *_*


def trans_data4entity(entity_relation):
    coauthor = []
    year_dict = {}
    year = []
    year_cnt = []
    interest_ls = []
    categories = [{'name': 'Core'}, {'name': 'Coauthor'}, {'name': 'Concept'},
                  {'name': 'Affiliation'}, {'name': 'Paper'}]
    data = []
    links = []

    author_profile = '"<h2>' + entity_relation[0]['n1']['authorName'] + '</h2>' + "<span class='digit'><strong>H-Index</strong>: " + \
                     str(entity_relation[0]['n1']['hi']) + "</span>  <span class='digit'><strong>Papers</strong>: " + str(entity_relation[0]['n1']['pc']) + \
                     "</span><br><span class='digit'><strong>Total Citations</strong>: " + str(entity_relation[0]['n1']['cn']) + '</span><br>'

    affiliation_num = 0

    for i in range(len(entity_relation)):
        if entity_relation[i]['rel']['type'] == 'Collaborate':
            coauthor.append(entity_relation[i])

    node = {}
    _id = 0
    node['name'] = entity_relation[0]['n1']['authorName']
    node['draggable'] = 'true'
    node['category'] = 0
    node['id'] = _id
    node['symbolSize'] = 70
    data.append(node)
    for i in range(len(entity_relation)):
        node = {'draggable': 'true'}
        relation = {'value': entity_relation[i]['rel']['type'], 'symbolSize': 20}
        if entity_relation[i]['rel']['type'] == 'Collaborate':
            relation['category'] = node['category'] = 1
            node['name'] = entity_relation[i]['n2']['authorName']
            node['value'] = int(entity_relation[i]['rel']['n_cooperation'])
            node['symbolSize'] = min(35 + 2 * node['value'], 65)
        elif entity_relation[i]['rel']['type'] == 'interest':
            interest_ls.append({'name': entity_relation[i]['n2']['conceptName'], 'value': 1})
            relation['category'] = node['category'] = 2
            node['name'] = entity_relation[i]['n2']['conceptName']
            node['value'] = 0
            node['symbolSize'] = 45
        elif entity_relation[i]['rel']['type'] == 'belong2':
            relation['category'] = node['category'] = 3
            node['name'] = entity_relation[i]['n2']['affiliationName']
            node['value'] = 0
            node['symbolSize'] = 55
            if affiliation_num < 3:
                author_profile += "<img src='../static/images/affiliation.png' alt='Affiliation' width='15' height='15'/> "
                author_profile += node['name'] + '<br>'
                affiliation_num += 1
        elif entity_relation[i]['rel']['type'] == 'own':
            if entity_relation[i]['n2']['paperYear'] in year_dict:
                year_dict[entity_relation[i]['n2']['paperYear']] += 1
            else:
                year_dict[entity_relation[i]['n2']['paperYear']] = 0
                year_dict[entity_relation[i]['n2']['paperYear']] += 1
            relation['category'] = node['category'] = 4
            node['name'] = entity_relation[i]['n2']['paperTitle']
            node['value'] = int(entity_relation[i]['rel']['author_pos'])
            if node['value'] == 1:
                node['symbolSize'] = 45
            elif node['value'] == 2:
                node['symbolSize'] = 30
            else:
                node['symbolSize'] = 20

        _id = i + 1
        node['id'] = _id
        data.append(node)
        relation['source'] = 0
        relation['target'] = node['id']
        links.append(relation)

    for item in year_dict:
        year.append(item)
        year_cnt.append(year_dict[item])

    y_max = max(year_cnt) + 1
    data_shadow = []
    for i in range(len(year_cnt)):
        data_shadow.append(y_max)

    author_profile += '"'

    return {'authorProfile': author_profile, 'categories': categories, 'data': data, 'links': links, 'year': year,
            'data_shadow': data_shadow, 'year_cnt': year_cnt, 'interest_ls': interest_ls, 'co_author': coauthor}


def trans_search_ls2json(entity_relation):
    authors_ls = {}
    for item in entity_relation:
        if item['n1']['authorID'] not in authors_ls:
            authors_ls[item['n1']['authorID']] = item['n1']
            authors_ls[item['n1']['authorID']]['affiliationName'] = []
            authors_ls[item['n1']['authorID']]['conceptName'] = []
        try:
            if item['n2']['affiliationName'] not in authors_ls[item['n1']['authorID']]['affiliationName']:
                authors_ls[item['n1']['authorID']]['affiliationName'].append(item['n2']['affiliationName'])
        except KeyError:
            pass
        try:
            if item['n3']['conceptName'] not in authors_ls[item['n1']['authorID']]['conceptName']:
                authors_ls[item['n1']['authorID']]['conceptName'].append(item['n3']['conceptName'].title())
        except KeyError:
            pass
        # print(item)
    return {'result_ls': authors_ls}
