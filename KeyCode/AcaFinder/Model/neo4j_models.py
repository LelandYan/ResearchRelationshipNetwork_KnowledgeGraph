# *_*coding:utf-8 *_*


from py2neo import Graph
from pypinyin import lazy_pinyin
import neo4j


class Neo4jTool:
    graph = None

    def __init__(self):
        print("Initialize Neo4j tools...")

    def zh2en(self, val):
        val_pinyin = lazy_pinyin(val)
        if val_pinyin[0] == val:
            return val.title()
        return (''.join(val_pinyin[1:]) + ' ' + val_pinyin[0]).title()

    def connect2neo4j(self):
        self.graph = Graph("http://localhost:7474", username="Graph", password="2139637")

    def get_author_rel_by_name(self, val):
        sql = "MATCH (n1:AUTHOR {authorName:\"" + self.zh2en(str(val)) + "\"})- [rel] -> (n2) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_author_rel_by_ID(self, val):
        sql = "MATCH (n1:AUTHOR {authorID:" + str(val) + "})- [rel] -> (n2) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_paper_detail_by_authorName(self, val):
        sql = "MATCH (n0:AUTHOR)-[rel]->(np:PAPER) WHERE n0.authorName='" + self.zh2en(str(val)) + \
              "' WITH np MATCH(np:PAPER)<-[rel2]-(na:AUTHOR) WITH np, rel2, na " \
              "MATCH (np:PAPER)-[rel3]->(nv:VENUE) RETURN np, rel2, na, nv;"
        answer = self.graph.run(sql).data()
        return answer

    def get_paper_detail_by_authorID(self, val):
        sql = "MATCH (n0:AUTHOR)-[rel]->(np:PAPER) WHERE n0.authorID=" + str(
            val) + " WITH np MATCH(np:PAPER)<-[rel2]-(na:AUTHOR) WITH np, rel2, na " \
                   "MATCH (np:PAPER)-[rel3]->(nv:VENUE) RETURN np, rel2, na, nv;"
        answer = self.graph.run(sql).data()
        return answer

    def match_author_affiliation_by_name(self, val):
        sql = "MATCH (n1:AUTHOR {authorName:'" + self.zh2en(str(val)) + \
              "'}) WITH n1 MATCH (n1)-[rel]-(n2:AFFILIATION) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        print('@@', answer)
        return answer

    def match_author_concept_by_name(self, val):
        sql = "MATCH (n1:AUTHOR {authorName:'" + self.zh2en(str(val)) + \
              "'}) WITH n1 MATCH (n1)-[rel]-(n2:CONCEPT) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        return answer

    def match_candidate_coauthor_by_ID_depth(self, val, depth1, depth2):
        sql = "MATCH (n1:AUTHOR{authorID:" + str(val) + "})-[*" + str(depth1) + ".." + str(
            depth2) + "]->(n2:AUTHOR) RETURN n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_search_ls_by_name(self, val):
        sql = "MATCH (n1:AUTHOR {authorName:'" + self.zh2en(str(val)) + \
              "'}) WITH n1 MATCH (n1)-[rel]-(n2:AFFILIATION) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()

        sql = "MATCH (n1:AUTHOR {authorName:'" + self.zh2en(str(val)) + \
              "'}) WITH n1 MATCH (n1)-[rel]-(n3:CONCEPT) RETURN n1, rel, n3;"
        answer.extend(self.graph.run(sql).data())
        return answer

    def get_search_ls_by_concept(self, val):
        # sql = "MATCH (n3:CONCEPT) -- (n1:AUTHOR) where n3.conceptName ='" + str(val) + \
        #       "' WITH n1 MATCH (n1)-[rel]-(n2:AFFILIATION) RETURN n1, rel, n2;"
        # sql = "MATCH (n3:CONCEPT) -[rel]- (n1:AUTHOR) where n2.conceptName ='" + str(val) + \
        #       "' RETURN n1, rel, n3;"
        sql = "MATCH (n3:CONCEPT {conceptName:'" + str(val) + \
              "'}) -- (n1:AUTHOR) WITH n1 MATCH (n1)-[rel]-(n2:AFFILIATION) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        sql = "MATCH (n2:CONCEPT {conceptName:'" + str(val) + \
              "'})-[rel]- (n1:AUTHOR) RETURN n1, rel, n2;"
        answer.extend(self.graph.run(sql).data())
        return answer

    def get_search_ls_by_keys(self, val):
        sql = "MATCH (n3:PAPER) -- (n1:AUTHOR) where n3.paperAbstract =~'.*(?i)" + str(val) + \
              ".*' WITH n1 MATCH (n1)-[rel]-(n2:AFFILIATION) RETURN n1, rel, n2 LIMIT 3;"
        answer = self.graph.run(sql).data()

        sql = "MATCH (n2:PAPER) -- (n1:AUTHOR) where n2.paperAbstract =~'.*(?i)" + str(val) + \
              ".*' WITH n1 MATCH (n1)-[rel]-(n3:CONCEPT) RETURN n1, rel, n3 LIMIT 3;"
        answer.extend(self.graph.run(sql).data())
        return answer

    # Not used yet
    def match_author_by_name(self, val):
        sql = "MATCH (n1:AUTHOR {authorName:'" + str(val) + "'})return n1;"
        answer = self.graph.run(sql).data()
        return answer

    def get_other_rel_by_author(self, val):  # exclude self
        sql = "MATCH (n1) - [rel] -> (n2)  WHERE n1.authorName = \"" + str(val) + "\" RETURN rel, n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_author_aff(self, val):
        sql = "MATCH (n1 {authorName:\"" + self.zh2en(
            str(val)) + "\"})- [rel {type:\"belong2\"}] -> (n2) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_author_interest(self, val):
        sql = "MATCH (n1 {authorName:\"" + self.zh2en(str(val)) + "\"})- [rel {type:\"interest\"}] -> (n2) RETURN n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_author_paper(self, val):
        '''
            MATCH (n1 {authorName:"Xingyi Zhang"})- [rel] -> (n2:PAPER) WITH n2 MATCH (n2)-[rel2:PAPER2VENUE]->(n3:VENUE) RETURN n2.paperID, n3.venueName;
        '''
        sql = "MATCH (n1 {authorName:\"" + str(val) + "\"})- [rel {type:\"own\"}] -> (n2) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        return answer

    def get_collaborator(self, val):
        sql = "MATCH (n1 {authorName:\"" + str(val) + "\"})- [rel {type:\"Collaborate\"}] -> (n2) RETURN n1, rel, n2;"
        answer = self.graph.run(sql).data()
        return answer
