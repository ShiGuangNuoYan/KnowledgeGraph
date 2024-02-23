# -*- coding: gbk -*-
from py2neo import Graph
class AnswerSearcher:
    def __init__(self):#�������ݿ���в�ѯ
        self.g = Graph("http://localhost:7474", auth=("neo4j", "jiayuang123"),name="neo4j")
        self.num_limit=5 #�������������Ŀ

    #ִ��cypher��ѯ��������Ӧ���
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
            final_answer='{0}��������{1}'.format(subject,';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_dynasty':
            desc=[i ['n.name'] for i in answers]
            subject=answers[0]['m.name']
            final_answer='{0}���׾�������{1}'.format(subject,';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='author_dynasty':
            desc=[i ['n.name'] for i in answers]
            subject=answers[0]['m.name']
            final_answer='{0}����ĳ�����{1}'.format(subject,';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_category':
            desc=[i ['m.category'] for i in answers]
            subject=answers[0]['m.name']
            final_answer = '{0}�������{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_content':
            desc = [i['m.content'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}�ľ���������{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='poem_trans':
            desc = [i['m.trans'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}�ľ��巭����{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='appreciation':
            desc = [i['m.appreciation'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}����ϸ��������{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='annotation':
            desc = [i['m.annotation'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}�ĳ���֪ʶ���ע������{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
        elif question_type=='background':
            desc = [i['m.background'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}�Ĵ���������{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))

        return final_answer

if __name__ == '__main__':
    seacher=AnswerSearcher()


