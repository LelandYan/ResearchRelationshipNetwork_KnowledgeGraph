# *_*coding:utf-8 *_*

import random
import time


def cos_sim(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0

    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2

    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA * normB) ** 0.5)


class EmbeddingModel:
    wv = None

    def read_vec(self, vec_src, obj):
        start = time.time()
        self.wv = {}

        f = open(vec_src, 'r', encoding="utf-8")
        line = f.readline()
        count = 0
        while line:
            count += 1
            if count % 1000000 == 999999:
                print('Loading embedding (' + str(count + 1) + ') ......')
            # if count == 100000: break
            line = line.split("\t")
            if obj not in line[0]:
                line = f.readline()
                continue
            curList = []
            for i in range(1, len(line)):
                curList.append(float(line[i]))
            self.wv[line[0]] = curList
            line = f.readline()

        f.close()
        print('Embedding cnt ' + str(len(obj)) + 'reading costs %.2fs.' % (time.time() - start))

    def get_sim_top(self, ID, top_num, sample):
        top_num += 1
        vec = self.wv[ID]
        cur_entity = []
        cur_sim = []
        for key, value in self.wv.items():
            if random.randint(0, 100) < sample:  # 留百分8数据
                continue
            if key == ID:
                continue
            sim = cos_sim(vec, value)
            cur_entity.append(key)
            cur_sim.append(sim)

            p = len(cur_entity) - 1
            if p <= 0:
                cur_entity.append(key)
                cur_sim.append(sim)
                continue

            while p >= 0:
                if sim < cur_sim[p]:
                    cur_entity.insert(p + 1, key)
                    cur_sim.insert(p + 1, sim)
                    break
                if p == 0:
                    cur_entity.insert(p, key)
                    cur_sim.insert(p, sim)
                    break
                p -= 1
            if len(cur_entity) > top_num:
                cur_entity = cur_entity[:top_num]
                cur_sim = cur_sim[:top_num]

        res = {}
        vis = set()
        top_num -= 1
        for t in range(top_num):
            max_sim = -100000
            max_item = ''
            for i in range(len(cur_entity)):
                if cur_entity[i] in vis:
                    continue
                if cur_sim[i] > max_sim:
                    max_sim = cur_sim[i]
                    max_item = cur_entity[i]

            res[max_item] = max_sim
            vis.add(max_item)

        return res

    def get_sim_top_on_candidate(self, ID, top_num, candidate):
        print('#', len(candidate))
        ID = 'authorID' + str(ID)
        top_num += 1
        vec = self.wv[ID]
        candidate_vec = {}
        cur_entity = []
        cur_sim = []
        for c in candidate:
            candidate_vec[c] = self.wv[c]
        for key, value in candidate_vec.items():
            if key == ID:
                continue
            if 10000 < len(candidate) < 20000:
                if random.randint(1, 100) > 60:
                    continue
            elif 20000 < len(candidate):
                if random.randint(1, 100) > 50:
                    continue

            sim = cos_sim(vec, value)
            cur_entity.append(key)
            cur_sim.append(sim)

            p = len(cur_entity) - 1
            if p <= 0:
                cur_entity.append(key)
                cur_sim.append(sim)
                continue

            while p >= 0:
                if sim < cur_sim[p]:
                    cur_entity.insert(p + 1, key)
                    cur_sim.insert(p + 1, sim)
                    break
                if p == 0:
                    cur_entity.insert(p, key)
                    cur_sim.insert(p, sim)
                    break
                p -= 1
            if len(cur_entity) > top_num:
                cur_entity = cur_entity[:top_num]
                cur_sim = cur_sim[:top_num]

        res = {}
        vis = set()
        top_num -= 1
        for t in range(top_num):
            max_sim = -100000
            max_item = ''
            for i in range(len(cur_entity)):
                if cur_entity[i] in vis:
                    continue
                if cur_sim[i] > max_sim:
                    max_sim = cur_sim[i]
                    max_item = cur_entity[i]

            res[max_item] = max_sim
            vis.add(max_item)

        return res


'''
emb_model = EmbeddingModel()
emb_model.read_vec('entity_embeddings.tsv')
print(emb_model.get_sim_top('authorID1347783', 2))
'''
