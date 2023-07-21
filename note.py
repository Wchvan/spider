import requests
from config import service_url, config


class Note:
    id = None  # id    不需要传
    title_raw = None  # 原标题
    content_raw = None  # 原内容
    title_edited = None  # 修改的标题
    content_edited = None  # 修改的内容
    tag = None  # tag分类 "3,51,5"
    rate = None  # 评分
    files = None  # 图片链接/视频链接 "5464,"
    origin_files = None  # 初始图片链接/初始视频链接
    file_type = None  # 资源类型 image/video string
    source = None  # 来源
    product_name = None  # 产品名
    pandn = None  # 正负相关
    extend = None  # 扩展字段
    gpt_problem = None  # Gpt 问题  -1:默认   0: 没有问题       1: 有问题，需要人工处理

    note_group_id = None  # note组id

    # 不需要传
    uploader = None
    handler = None
    upload_date = None

    note_group = None  # note组

    def new(self, id, note_group, uploader, handler, title_raw, content_raw, title_edited, content_edited, tag, rate,
            files, origin_files, file_type, source, product_name, pandn, extend, upload_date, gpt_problem,*args,**kwargs):
        self.id = id
        self.note_group = note_group
        self.uploader = uploader
        self.handler = handler
        self.title_raw = title_raw
        self.content_raw = content_raw
        self.title_edited = title_edited
        self.content_edited = content_edited
        self.tag = tag
        self.rate = rate
        self.files = files
        self.origin_files = origin_files
        self.file_type = file_type
        self.source = source
        self.product_name = product_name
        self.pandn = pandn
        self.extend = extend
        self.upload_date = upload_date
        self.gpt_problem = gpt_problem

    def upload_new_note(self, note_group_id):
        self.note_group_id = note_group_id
        data = self.__dict__
        print(data)
        url = service_url.NOTE_URL
        res = requests.post(url, json=data, headers=config.HEADERS)
        print(res.text)


class UpdateNote(Note):

    def update_partial(self):
        data = self.__dict__
        url = service_url.NOTE_URL + str(self.id) + '/'
        res = requests.patch(url, json=data, headers=config.HEADERS)
        print(res.text)
