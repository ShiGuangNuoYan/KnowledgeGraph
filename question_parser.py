# -*- coding: gbk -*-
class QuestionParser:

    # ����ʵ��ڵ�,�������Թ�ϵΪ�����ڵ�Ϊֵ���ֵ�
    def build_entity(self,args):
        entity_dict={}
        for arg,types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type]=[arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    #����������,res_classify����conversation_graph.py�е�data
    def parser_main(self,res_classify):
        args=res_classify['args']
        entity_dict=self.build_entity(args)
        question_types=res_classify['question_types']
        sqls=[]
        for question_type in question_types:
            sq={}
            sq['question_type']=question_type
            sql=[]
            if question_type=='poem_author':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type=='poem_dynasty':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type=='author_dynasty':
                sql=self.sql_transfer(question_type,entity_dict.get('author'))
            elif question_type=='poem_category':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type=='poem_content':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type=='poem_trans':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type=='appreciation':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type=='annotation':
                sql=self.sql_transfer(question_type,entity_dict.get('poem'))
            elif question_type == 'background':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))
            if sql:
                sq['sql']=sql
                sqls.append(sq)
        return sqls #����sql��ѯ��乩ͼ�ײ�ѯ(�����Ƕ���)
    def sql_transfer(self,question_type,entities):#��Բ�ͬ���������ת��
        if not entities:
            return []
        #��ѯ���
        sql=[]
        #��ѯ
        if question_type=='poem_author':
            sql=["MATCH (m:Poem)-[r:created_by]->(n:Author) where m.name = '{0}' return m.name,r.name,n.name".format(i) for i in entities]
        elif question_type=='poem_dynasty':
            sql=["MATCH (m:Poem)-[r:created_during]->(n:Dynasty) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type=='author_dynasty':
            sql=["MATCH (m:Author)-[r:born in]->(n:Dynasty) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type=='poem_category':
            sql=["MATCH (m:Poem)-[r:belongs_to]->(n:Category) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type=='poem_content':
            sql = ["MATCH (m:Poem) where m.name = '{0}' return m.name, m.content".format(i) for i in entities]
        elif question_type=='poem_trans':
            sql=["MATCH (m:Poem) where m.name = '{0}' return m.name, m.trans".format(i) for i in entities]
        elif question_type=='appreciation':
            sql=["MATCH (m:Poem) where m.name = '{0}' return m.name, m.appreciation".format(i) for i in entities]
        elif question_type=='annotation':
            sql=["MATCH (m:Poem) where m.name = '{0}' return m.name, m.annotation".format(i) for i in entities]
        elif question_type=='background':
            sql=["MATCH (m:Poem) where m.name = '{0}' return m.name, m.background".format(i) for i in entities]
        return sql

if __name__ == '__main__':
    handler=QuestionParser()