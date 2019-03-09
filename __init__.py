import os
from cudatext import *
import sys
from io import StringIO


sys.path.append(os.path.dirname(__file__))

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_css_inspector.ini')
fn_icon = os.path.join(os.path.dirname(__file__), 'icon.png')

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

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
       
    def config(self):
        ini_write(fn_config, 'op', 'option_int', str(option_int))
        ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        file_open(fn_config)

    def on_caret(self, ed_self):
        from lxml import etree
        from lxml import cssselect 
        car = ed_self.get_carets()[0]
        f=StringIO(ed_self.get_text_substr(0,0,car[0],car[1]))
        tree=etree.parse(f,etree.HTMLParser())
        try:
            root=tree.getroot()[-1]
            while(len(root.getchildren())>0):
                root=root.getchildren()[-1]
            
            # получены все свойства последнего тега до курсора
            
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
                
            pos = car[:2]
            
            while(';' in res):
                res = res.replace(';','\n')
            
            dlg_proc(self.panel, DLG_CTL_PROP_SET, index=self.label, prop={
              'cap':res+'\n',
            })
        except:
            pass