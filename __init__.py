import os
from cudatext import *
import sys

sys.path.append(os.path.dirname(__file__))
import lxml
from lxml import etree
from lxml import cssselect 

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_css_inspector.ini')
fn_icon = os.path.join(os.path.dirname(__file__), 'snip.png')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

'''
def parsehtml(html):
    html = html.replace('\n','')
    res = []
    tmp=''
    is_tag=False
    for i in html:
        if i=='<':
            tmp=''
            is_tag=True
        elif i=='>':
            is_tag=False
            res.append(tmp)
            tmp=''
        else:
            tmp+=i
    n=0
    while (n<len(res)):
        current = res[n]
        if current[0]=='/':
            #print("DELETING")
            tag = current[1:]
            i=n-1
            res.pop(n)
            print('deleting '+tag)
            print('l'+str(res))
            while i>0 and not res[i] == tag :
                i -= 1
            for j in range(n-i+1):
                res.pop(i)
            print(res)
            n=0
        n+=1
    return res

def get_style_by_tag(tag):
    return '\tdisplay_'+tag+':block';
    
def get_style_by_class(tag):
    while ' =' in tag:
        tag = tag.replace(' =','=')
    while '= ' in tag:
        tag = tag.replace('= ','=')
    if not 'class=' in tag:
        return ''
    tag_class = tag.split('class=')[1]
    tag_class = tag_class.split(tag_class[0])[1]
    return ('\tdisplay_'+tag_class+':block')
     
def get_style(tag):
    if not 'style=' in tag:
        return ''
    style=tag.split('style=')[1]
    print('STYLE: '+str(style))
    quote=style[1]
    style=style.split(quote)[1]
    res=''
    for i in style.split(';'):
        res+='\n\t'+i
    return res


def get_stylesheet(text):
    res=''
    while('<style>' in text):
        res += text.split('<style>')[1].split('</style>')[0]
        after = text.split('</style>')
        text=''
        num=0
        for i in after:
            if num>0:
                text+=i+'</style>'
            num+=1
    return res

def parse_to_text(parse): 
    res=''
    for i in parse:
        res+=i+'\n'+get_style_by_tag(i.split(' ')[0])+'\n'+get_style_by_class(i)+get_style(i)+'\n'
    return res
'''
class Command:
    
    def __init__(self):
        self.panel = dlg_proc(0, DLG_CREATE)
        dlg_proc(self.panel, DLG_PROP_SET,prop={
        })	
        self.label = dlg_proc(self.panel,DLG_CTL_ADD,'label')
        dlg_proc(self.panel, DLG_CTL_PROP_SET, index=self.label, prop={
          'x':3,
          'y':3,
          #'color_font':55555555,  
          'cap':'test\nku',
        })
        app_proc(PROC_SIDEPANEL_ADD_DIALOG, ('CSS Inspector', self.panel, fn_icon) )
        app_proc(PROC_SIDEPANEL_ACTIVATE, 'CSS Inspector')
       
        print('STARTED')
        
    def config(self):
        ini_write(fn_config, 'op', 'option_int', str(option_int))
        ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        file_open(fn_config)

    def on_caret(self, ed_self):
        #####
        
        from io import StringIO
        
        f=StringIO('''
        <html>
            <head>
              <style>
                .c{
                  display:block;
                }
                .d #e{
                  font-family:helvetica;
                  color:red;
                }
                
              </style>
              <style>
              </style>
            </head>
            <body>
                <p class="c" style='background-color:lightred' id="e">
        ''')
        car = ed_self.get_carets()[0]
        f=StringIO(ed_self.get_text_substr(0,0,car[0],car[1]))
        tree=etree.parse(f,etree.HTMLParser())
        
        root=tree.getroot()[-1]
        while(len(root.getchildren())>0):
            root=root.getchildren()[-1]
        
        print(root.attrib)  # получены все свойства последнего тега до курсора
        
        csscode=''
        css=cssselect.CSSSelector('style')(tree)
        for i in css:
            csscode+=i.text   # получен текст всех тегов style
        
        csscodeold=csscode
        csscode=''
        for i in csscodeold:
            if i in ['\t']:
                pass
            else:
                csscode+=(i)  # из вcех тегов style убраны табы, пробелы и ентеры
        
        csscodeold=csscode
        csscode=''
        for i in csscodeold.split('\n'):
            while len(i)>0:
                if i[0]==' ':
                    i=i[1:]
                elif i[-1]==' ':
                    i=i[:-1]
                else: break
            csscode=csscode+i
        
        cssarr=csscode.split('}')[:-1]
        for i in range(len(cssarr)):
            cssarr[i]=[cssarr[i].split('{')[0].split(' '),cssarr[i].split('{')[1]]
        
        print(cssarr)
        
        res=''
        for i in cssarr:
            if 'class' in root.attrib and '.'+root.attrib['class'] in i[0]:
                res+=i[1]
            elif 'id' in root.attrib  and '#'+root.attrib['id'] in i[0]:
                res+=i[1]
            elif root.tag in i[0]:
                res+=i[1]
        if 'style' in root.attrib:
            res+=root.attrib['style']
            
        print(res)
        #####
        pos = ed_self.get_carets()[0][:2]
        #sub_str = ed_self.get_text_substr(0,0,pos[0],pos[1])
        while(';' in res):
            res = res.replace(';','\n')
        dlg_proc(self.panel, DLG_CTL_PROP_SET, index=self.label, prop={
          'cap':res+'\n',
        })
        pass
