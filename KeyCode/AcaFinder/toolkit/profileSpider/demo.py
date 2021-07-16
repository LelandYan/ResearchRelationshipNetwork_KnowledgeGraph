from profile_class import Profile
import re

# url = 'http://cs.ahu.edu.cn/2018/0329/c11201a163134/page.htm'
# url = "http://cs.henu.edu.cn/info/1048/1934.htm"
# url = "http://cs.henu.edu.cn/info/1048/1794.htm"
url = "http://cic.tju.edu.cn/faculty/xuexiao/index.html"
# url = "https://cs.nju.edu.cn/zhouzh/"
# url = "http://cic.tju.edu.cn/info/1067/1103.htm"
# url = "http://cic.tju.edu.cn/faculty/likeqiu/"
# url = "https://cs.nju.edu.cn/zhouzh/zhouzh.files/resume_cn.htm"
'''
html, _ = he.extract(url, text_only=False, remove_img=False, save=True)
doc, p_val = he.extract(url, save=True)
'''

profile = Profile(url)
profile.identify()
print(profile.get_email())
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

# print('###########')
#
# for i in year_dict:
#     print(i, year_dict[i])
#
