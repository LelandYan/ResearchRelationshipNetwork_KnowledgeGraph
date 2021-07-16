# *_*coding:utf-8 *_*

from django.shortcuts import render
from django.http import JsonResponse
from toolkit.initialization import neo_con
from toolkit.initialization import author_emb
from web.data4page import trans_data4entity
from toolkit.profileSpider.profile_class import Profile

import json
import random

entity_flag = None
co_author = None


def search_entity(request):
    global entity_flag
    global co_author
    nothing = {}
    if request.GET:
        entity = entity_flag = request.GET['user_text'].strip()
        db = neo_con
        tmp = db.get_author_rel_by_ID(entity)
        entity_relation = json.loads(json.dumps(tmp, ensure_ascii=False))
        if len(entity_relation) == 0:
            nothing = {'title': '<h1>Not Found</h1>'}
            return render(request, 'entity.html', {'nothing': json.dumps(nothing, ensure_ascii=False)})
        else:
            trans_data = trans_data4entity(entity_relation)
            co_author = trans_data['co_author']
            return render(request, 'entity.html', trans_data)
    return render(request, "entity.html", {'nothing': nothing})


def ajax_return_paper(request):
    global entity_flag
    db = neo_con
    tmp = db.get_paper_detail_by_authorID(entity_flag)
    papers_detail = {}
    year_paper = {}
    for i in range(len(tmp)):
        if tmp[i]['np']['paperID'] not in papers_detail:
            papers_detail[tmp[i]['np']['paperID']] = \
                {'paperTitle': tmp[i]['np']['paperTitle'].title(), 'paperYear': tmp[i]['np']['paperYear'],
                 'paperAbstract': tmp[i]['np']['paperAbstract'],
                 'venue': {'venueName': tmp[i]['nv']['venueName'], 'venueID': tmp[i]['nv']['venueID']}}
        if 'authors' not in papers_detail[tmp[i]['np']['paperID']]:
            papers_detail[tmp[i]['np']['paperID']]['authors'] = {}
        papers_detail[tmp[i]['np']['paperID']]['authors'][tmp[i]['rel2']['author_pos']] = {
            'authorID': tmp[i]['na']['authorID'],
            'authorName': tmp[i]['na']['authorName']}
        # for year_paper
        if tmp[i]['np']['paperYear'] not in year_paper:
            year_paper[tmp[i]['np']['paperYear']] = []
        if tmp[i]['np']['paperTitle'].title() not in year_paper[tmp[i]['np']['paperYear']]:
            year_paper[tmp[i]['np']['paperYear']].append(tmp[i]['np']['paperTitle'].title())
    return JsonResponse({'papers_detail': papers_detail, 'year_paper': year_paper})


def ajax_rec_coauthor(request):
    global entity_flag
    global co_author
    db = neo_con
    tmp = db.match_candidate_coauthor_by_ID_depth(entity_flag, 2, 3)  # 1011021
    candidate_ID = []
    co_author_ID = set()
    tmp = json.loads(json.dumps(tmp, ensure_ascii=False))
    try:
        for k in co_author:
            co_author_ID.add(k['n2']['authorID'])
        for i in range(len(tmp)):
            # print(tmp[i]['n2']['authorID'])
            if tmp[i]['n2']['authorID'] not in co_author_ID:
                candidate_ID.append('authorID' + str(tmp[i]['n2']['authorID']))
        # print(2222)
        rec_ID_prob = author_emb.get_sim_top_on_candidate(entity_flag, 10, candidate_ID)
        print('Call Coauthor Recommendation', rec_ID_prob)
        rec_author = []
        for i in range(len(tmp)):
            if 'authorID' + str(tmp[i]['n2']['authorID']) in rec_ID_prob:
                au = json.loads(json.dumps(tmp[i]['n2']))
                au['prob'] = rec_ID_prob['authorID' + str(tmp[i]['n2']['authorID'])]
                if au not in rec_author:
                    rec_author.append(au)
        random.shuffle(rec_author)
        return JsonResponse({'status': 'ok', 'rec_author': rec_author})
    except:
        return JsonResponse({'status': 'error'})


# TODO link to html
#  李克秋 张建忠
info_dict = {"946043": "http://cic.tju.edu.cn/faculty/xuexiao/index.html",
             "1011021": "https://cs.nju.edu.cn/zhouzh/zhouzh.files/resume_cn.htm",
             "565140": "http://cic.tju.edu.cn/faculty/likeqiu/",
             "1641449": "https://cc.nankai.edu.cn/2019/1010/c13619a209626/page.htm",
             "235550": "http://cs.henu.edu.cn/info/1048/1934.htm"}


def ajax_extInfo(request):
    authorID = entity_flag
    url = info_dict.get(authorID, None)
    if url is None:
        return JsonResponse({'status': 'error'})
    # url = "http://cic.tju.edu.cn/faculty/xuexiao/index.html"
    # url = "http://cs.henu.edu.cn/info/1048/1934.htm"
    # url = "https://cs.nju.edu.cn/zhouzh/zhouzh.files/resume_cn.htm"
    print(url)

    profile = Profile(url)
    profile.identify()
    email = profile.get_email()
    # print(profile.get_homepage())
    # print(profile.get_gender())
    edu_dict = profile.get_edu_dict()
    honor_dict = profile.get_honor_dict()
    pub_dict = profile.get_pub_dict()
    year_dict = profile.get_year_dict()

    for key in edu_dict:
        print('----')
        print('education', edu_dict[key]['prob'], edu_dict[key]['year'], key)

    for key in honor_dict:
        print('----')
        print('honor', honor_dict[key]['prob'], honor_dict[key]['year'], key)

    for key in pub_dict:
        print('----')
        print('publication', pub_dict[key]['prob'], pub_dict[key]['year'], key)

    # for key in year_dict:
    #     print('----')
    #     print('publication', year_dict[key]['prob'], year_dict[key]['year'], key)
    if len(honor_dict) > 0 or len(pub_dict) > 0 or len(edu_dict) > 0:
        print("success")
        return JsonResponse(
            {'status': 'ok', 'honor_dict': honor_dict, 'pub_dict': pub_dict, 'edu_dict': edu_dict, 'email': email})
    else:
        return JsonResponse({'status': 'error'})
