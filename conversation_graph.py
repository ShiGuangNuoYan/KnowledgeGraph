# -*- coding: gbk -*-
import ahocorasick
import os
class QuestionClassifier():
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #������·��
        self.poem_path=os.path.join(cur_dir,'dictionary/poem.txt')
        self.dynasty_path=os.path.join(cur_dir,'dictionary/dynasty.txt')
        self.category_path=os.path.join(cur_dir,'dictionary/category.txt')
        self.author_path=os.path.join(cur_dir,'dictionary/author.txt')

        #����������
        self.poem_wds=[i.strip() for i in open(self.poem_path,encoding="gbk") if i.strip()]
        self.dynasty_wds=[i.strip() for i in open(self.dynasty_path,encoding="gbk") if i.strip()]
        self.category_wds=[i.strip() for i in open(self.category_path,encoding="gbk") if i.strip()]
        self.author_wds=[i.strip() for i in open(self.author_path,encoding="gbk") if i.strip()]
        self.field_words=set(self.poem_wds+self.dynasty_wds+self.category_wds+self.author_wds)
        #��������actree,���Խ��ı��������Զ������Զ��������ı���Ѱ������Ԥ�ȶ���Ĺؼ��ʣ������ܹ�������ÿ���ؼ��ʵĳ���λ�á����ַ�������һ����ÿ���ؼ���Ҫ��Ч�ö࣬�ر����ڹؼ��ʼ��Ϻܴ���ı��ܳ�������¡�
        self.field_tree=self.build_actree(list(self.field_words))
        #�����ʵ�
        self.wdtype_dict=self.build_wdtype_dict()
        #�ʾ����ʾ�
        self.author_qwd=['����','˭д��','ʫ��','����','����˭��']
        self.dynasty_qwd=['����','���','�ĸ�ʱ��']
        self.content_qwd=['������ʲô','��ôд��','զд��','��ô��','���㱳д','Ĭд','��ȫ']
        self.category_qwd=['���','��ʽ']
        self.appreciation_qwd=['����','����','Ʒ��','����','����','����','Ŀ����']
        self.background_qwd=['��ʷ����','��������','������','��ʷ����','��ʱ','��ʱ','д��Ե��','д��ԭ��']
        self.trans_qwd=['����','����ʫ�Ľ���','ͨ��','����','�˻�','����']
        self.annotation_qwd=['ע��','�ؼ�֪ʶ��','��������','֪ʶ��']
        #print('model init finished ......')
        return

    #����������
    def classify(self,question):
        data={}
        poem_dict=self.check_poems(question)#����һ������
        if not poem_dict:#���Ϊ��
            return {}
        data['args']=poem_dict
        #�ռ����⵱�е�ʵ������
        types=[]
        for type_ in poem_dict.values():
            types+=type_
        question_type='others'#������
        question_types=[]

        if self.check_words(self.author_qwd,question) and ('poem' in types):#����ʫ��������˭
            question_type='poem_author'
            question_types.append(question_type)

        if self.check_words(self.dynasty_qwd,question) and 'poem' in types:#����ʫ�ĳ�����ʲô
            question_type='poem_dynasty'
            question_types.append(question_type)

        if self.check_words(self.dynasty_qwd,question) and 'author' in types:#���߳�����ʲô
            question_type='author_dynasty'
            question_types.append(question_type)

        if self.check_words(self.content_qwd,question) and 'poem' in types:#����ʫ��������ʲô?
            question_type='poem_content'
            question_types.append(question_type)

        if self.check_words(self.category_qwd,question) and 'poem' in types:#����ʫ�������ʲô
            question_type='poem_category'
            question_types.append(question_type)

        if self.check_words(self.trans_qwd,question) and 'poem' in types:#����ʫ�ķ�����ʲô
            question_type='poem_trans'
            question_types.append(question_type)

        if self.check_words(self.annotation_qwd,question) and 'poem' in types:#����ʫ�ĳ���ע����ʲô
            question_type='poem_annotation'
            question_types.append(question_type)

        if self.check_words(self.appreciation_qwd,question): #������ʲô
            question_type='appreciation'
            question_types.append(question_type)

        if self.check_words(self.background_qwd,question): #������ʲô
            question_type='background'
            question_types.append(question_type)

        data['question_types']=question_types

        return data

    #����actree���ٹ���
    def build_actree(self,wordlist):
        actree=ahocorasick.Automaton()
        for index,word in enumerate(wordlist):
            actree.add_word(word,(index,word))
        actree.make_automaton()
        return actree

    def build_wdtype_dict(self):#���������
        wd_dict=dict()
        for wd in self.field_words:#�ҵ��û�����Ĵ���ʲô��Χ��
            wd_dict[wd]=[]
            if wd in self.poem_wds:
                wd_dict[wd].append('poem')
            if wd in self.author_wds:
                wd_dict[wd].append('author')
            if wd in self.dynasty_wds:
                wd_dict[wd].append('dynasty')
            if wd in self.category_wds:
                wd_dict[wd].append('category')
        return wd_dict

    #�ʾ����
    def check_poems(self,question):
        field_wds=[]
        for i in self.field_tree.iter(question):# ahocorasick�� ƥ������  iter����һ��Ԫ�飬i����ʽ��(3, (23192, '�Ÿ�'))
            wd=i[1][1]#ƥ�䵽�Ĵ�
            field_wds.append(wd)
        stop_wds=[]
        for wd1 in field_wds:
            for wd2 in field_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1) #stopwordȡ�ظ��ҽ϶̵Ĵ���
        final_wds = [i for i in field_wds if i not in stop_wds]  # final_wdsȡ����,Ҳ������󷵻ص��ǳ���
        final_dict= {i:self.wdtype_dict.get(i) for i in final_wds}#�����ڹ���ʵ䣬# ��ȡ�ʺʹ�����Ӧ��ʵ������
        return final_dict

    #���������ʽ��з���
    def check_words(self,wds,sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler=QuestionClassifier()
    while True:
        question=input('��������������:')
        data = handler.classify(question)
        print(data)
