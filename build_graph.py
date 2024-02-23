import os
from py2neo import Graph,Node
import json

class KL_Graph():
    #初始化
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path=os.path.join(cur_dir,'data/kownledge.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "jiayuang123"),name="neo4j")
    #读取文件
    def read_nodes(self):
        #构建实体节点
        poem=[]#诗词
        author=[]#作者
        dynasty=[]#朝代
        category=[]#种类
        #theme=[]#主题

        poem_infos=[]#诗词信息

        #构建节点实体关系
        rel_create=[]#创作关系
        rel_dynasty=[]#朝代归属关系
        rel_belongC=[]#分类关系
        rel_birth=[]#作者与朝代关系


        count=0
        for data in open(self.data_path,encoding='utf-8'):
            poem_dict={}
            count+=1
            print(count)
            data_json=json.loads(data)
            poem_name=data_json['name']
            #print(poem_name)
            poem_dict['name']=poem_name
            poem.append(poem_name)
            poem_dict['content']=''
            poem_dict['trans']=''
            poem_dict['annotation']=''
            poem_dict['appreciation']=''
            poem_dict['background']=''

            if 'dynasty' in data_json:
                dynasty.append(data_json['dynasty'])
                rel_dynasty.append([poem_name,data_json['dynasty']])
            if 'author' in data_json:
                author.append(data_json['author'])
                print(author)
                rel_create.append([poem_name,data_json['author']])
            if 'category' in  data_json:
                category.append(data_json['category'])
                rel_belongC.append([poem_name,data_json['category']])
            if 'author' in data_json and 'dynasty' in data_json:
                rel_birth.append([data_json['author'],data_json['dynasty']])

            if 'content' in data_json:
                poem_dict['content']=data_json['content']
            if 'trans' in data_json:
                poem_dict['trans']=data_json['trans']
            if 'annotation' in data_json:
                poem_dict['annotation']=data_json['annotation']
            if 'appreciation' in data_json:
                poem_dict['appreciation']=data_json['appreciation']
            if 'background' in data_json:
                poem_dict['background']=data_json['background']
            poem_infos.append(poem_dict)

        return set(poem),set(author),set(dynasty),set(category),poem_infos,\
            rel_create,rel_dynasty,rel_belongC,rel_birth

    #创建普通节点
    def create_node(self,label,nodes):
        """
        :param label: 节点标签(即名称)
        :param nodes: 具体节点
        :return: None
        """
        count=0
        for node_name in nodes:
            node=Node(label,name=node_name)
            self.g.create(node)
            count+=1
            print(count,len(nodes))
        return

    #创建poem中心结点
    def create_poem_nodes(self,poem_infos):
        """
        :param poem_infos: 诗歌节点具体信息
        :return: None
        """
        count=0
        for poem_dict in poem_infos:
            node=Node("Poem",name=poem_dict['name'],content=poem_dict['content'],
                      trans=poem_dict['trans'],annotation=poem_dict['annotation'],
                      appreciation=poem_dict['appreciation'],background=poem_dict['background'])
            self.g.create(node)
            count+=1
            print(count)
        return

    #创建指示图谱的实体节点
    def create_graphnodes(self):
        poem, author, dynasty, category, poem_infos, rel_create, rel_dynasty, rel_belongC,rel_birth=self.read_nodes()
        self.create_poem_nodes(poem_infos)#创建古诗详细信息
        self.create_node('Dynasty',dynasty)#创建朝代节点
        self.create_node('Author',author)#创建作者节点
        self.create_node('Category',category)#创建种类节点
        return

    def create_relationship(self,start_node,end_node,edges,rel_type,rel_name):
        """
        :param start_node: 起始节点
        :param end_node: 终点节点
        :param edges: 边
        :param rel_type: 关系类型
        :param rel_name: 关系名字
        :return: None
        """
        count=0
        #去重处理
        set_edges=[]
        for edge in edges:
            set_edges.append('###'.join(edge))#使用###作为不同关系之间分隔的标志
        all=len(set(set_edges))
        for edge in set(set_edges):
            edge=edge.split('###')
            p=edge[0]
            q=edge[1]
            query="match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)"%(
                start_node,end_node,p,q,rel_type,rel_name)#match语法，p，q分别为标签，rel_type表示关系类别，rel_name 关系名字
            try:
                self.g.run(query)
                count+=1
                print(rel_type,count,all)
            except Exception as e:
                print(e)
        return

    #创建实体关系边
    def create_graphrels(self):
        poem, author, dynasty, category, poem_infos, rel_create, rel_dynasty, rel_belongC,rel_birth = self.read_nodes()
        self.create_relationship('Poem','Author',rel_create,'created_by','被创作')
        self.create_relationship('Poem','Dynasty',rel_dynasty,'created_during','创作于')
        self.create_relationship('Poem','Category',rel_belongC,'belongs_to','属于')
        self.create_relationship('Author','Dynasty',rel_birth,'born in','生于')

    def export_data(self):
        poem, author, dynasty, category, poem_infos, rel_create, rel_dynasty, rel_belongC,rel_birth = self.read_nodes()
        f_poem=open('dictionary/poem.txt', 'w+')
        f_author=open('dictionary/author.txt', 'w+')
        f_dynasty = open('dictionary/dynasty.txt', 'w+')
        f_category = open('dictionary/category.txt', 'w+')

        f_poem.write('\n'.join(list(poem)))
        f_author.write('\n'.join(list(author)))
        f_dynasty.write('\n'.join(list(dynasty)))
        f_category.write('\n'.join(list(category)))

        f_poem.close()
        f_author.close()
        f_dynasty.close()
        f_category.close()

        return
if __name__ == '__main__':
    handler=KL_Graph()#创建图数据库
    handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()
























