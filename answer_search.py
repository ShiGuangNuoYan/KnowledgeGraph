# -*- coding: gbk -*-
from py2neo import Graph
class AnswerSearcher:
    def __init__(self):#调用数据库进行查询
        self.g = Graph("http://localhost:7474", auth=("neo4j", "jiayuang123"),name="neo4j")
        self.num_limit=5 #答案种类的限制数目

    #执行cypher查询并返回相应结果
    def search_main(self,sqls):
        final_answers=[]
        for sq in sqls:
            question_type=sq['question_type']
            queries=sq['sql']
            answers=[]

            for query in queries:
                res=self.g.run(query).data()
                answers+=res
            final_answer=self.answer_prettify(question_type,answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_prettify(self,question_type,answers):
        final_answer=[]
        if not answers:
            return ''
        if question_type=='poem_author':
            desc=[i ['n.name'] for i in answers]
            subject=answers[0]['m.name']
            final_answer='{0}的作者是{1}'.format(subject,';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_dynasty':
            desc=[i ['n.name'] for i in answers]
            subject=answers[0]['m.name']
            final_answer='{0}这首经典作于{1}'.format(subject,';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='author_dynasty':
            desc=[i ['n.name'] for i in answers]
            subject=answers[0]['m.name']
            final_answer='{0}生活的朝代是{1}'.format(subject,';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_category':
            desc=[i ['m.category'] for i in answers]
            subject=answers[0]['m.name']
            final_answer = '{0}的体裁是{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_content':
            desc = [i['m.content'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的具体内容是{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_trans':
            desc = [i['m.trans'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的具体翻译是{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='appreciation':
            desc = [i['m.appreciation'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的详细赏析如下{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='annotation':
            desc = [i['m.annotation'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的常见知识点和注释如下{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='background':
            desc = [i['m.background'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的创作背景是{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))

        return final_answer

if __name__ == '__main__':
    seacher=AnswerSearcher()


