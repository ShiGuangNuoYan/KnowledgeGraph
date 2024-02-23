# -*- coding: gbk -*-
class QuestionParser:

    # 创建实体节点,构造了以关系为键，节点为值的字典
    def build_entity(self,args):
        entity_dict={}
        for arg,types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type]=[arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    #解析主函数,res_classify就是conversation_graph.py中的data
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
        return sqls #返回sql查询语句供图谱查询(可以是多条)
    def sql_transfer(self,question_type,entities):#针对不同的问题进行转换
        if not entities:
            return []
        #查询语句
        sql=[]
        #查询
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