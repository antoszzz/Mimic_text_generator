import random
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import *
##import ctypes #---> ctypes.windll.user32.MessageBoxW(0,'Message' ,'Title',0)
#import sys
import os.path
from tkinter import scrolledtext
#separate the symbols from the letters
def split_pro(t1='',t2=''):
    if t1=='' or t2=='': return t2
    for i in t1:
        t2=t2.replace(i,' '+i+' ')
    t2 = t2.replace('   ',' ') #replacing the triple space by single
    t2 = t2.replace('  ',' ') #replacing the duble space by single
    return t2.split()

def replace_pro(t1='',t2='',txt_to_kill=[],sent_sep=[]):
    if t1=='' or t2=='': return t2
    for i in t1:  #sticking some symbols together
        t2=t2.replace(' '+i,i)
    for i in t1: #removing from the text sum chosen duplicates
        t2=t2.replace(i+i+i,i)
        t2=t2.replace(i+i+i,i)
        t2=t2.replace(i+i,i)
        t2=t2.replace(i+i,i)
    for i in sent_sep:
        t2=t2.replace(i,i+' ')
    for i in txt_to_kill:#removing from the text sum chosen symbols
        t2=t2.replace(i,'')
    t2=t2.replace('-',' -')
    for i in range(2):
        t2=t2.replace('  ',' ')
    return t2
def s_file_refresh(): 
    res = filedialog.askopenfile('r',title='Choose the text source file',filetypes=[('Text sourses',['*.txt'])])
    if res is None:
        tk.messagebox.showinfo(title='File not found', message='Source file not found :(')
        return
    lbl_source.configure(text=res.name)
    return
#get the text content from the file chosen
def text_import(s_f:str):
    if not os.path.isfile(s_f):
        tk.messagebox.showinfo(title='File not found', message='Source file not found :(')
        return
    with open(s_f, 'r') as file:
        copy_book = file.read()
    return copy_book
#Returns mimic dict mapping each word to list of words which follow it.
def mimic_dict(text):
    b_txt=[]
    b_txt = split_pro('`,.-+#$@!;:>?<][}{\\/*',text.lower())
    d={}; d['']=[b_txt[0]]; j=0;id2=0
    unic_list=[]
    r_ge=[]
    l=len(b_txt)
    for i in b_txt:
        if i not in unic_list and id2<l:
            unic_list.append(i)
            id=0
            for ii in b_txt:
                if ii ==i and id<(l-1):
                    r_ge.append(b_txt[id+1])
                id+=1
            print(r_ge)
            if r_ge==[]: r_ge.append(' ')
            print(r_ge)
            d[unic_list[j]]=r_ge
            r_ge=[]
            j+=1
        id2+=1
    return d
#"""Given mimic dict and start word, prints 50 random words."""
def print_mimic(data_text,first_word = '',txt_scale=1.0):
    dic={}
    dic=data_text
    separ_s = ['.','!','?']
    #print(dic)
    #s=['']
    f_word=first_word.lower()
    r_ge=[]
    if f_word in dic:
        r_ge.append(first_word.capitalize())
    else:
        f_word=''
        r_ge.append(f_word)
        txt_w.delete(0,END)
        txt_w.insert(0,'Only the word from the text!')
    rg = range(int(100*txt_scale))
    for i in rg:
        if i>0:
            if f_word in dic:
                s= random.choices(dic[f_word])
            else:
                s=['']

            if (r_ge[i-1] in separ_s) or (i==1):
                a = s[0]
                r_ge.append(a.capitalize())
            else:
                r_ge.append(s[0])
            f_word=s[0]
    result =" ".join(r_ge)
    separ_s.append(',')
    result = replace_pro(',.-+#$@!;:>?<][} {\\/*', result,['`'," ' "],separ_s)
    return result
#inicjalization of new text generation and saving results and source to the labels on the frame
def generate(src=''):
    if src =='': 
        if lbl_source.cget('text')=='': s_file_refresh()
        src=text_import(lbl_source.cget('text'))
    f_word=txt_w.get()
    try:
        a = txt_w2.get()
        scale=int(float(a.replace(',','.')))
        scale = abs(scale)
    except:
        tk.messagebox.showinfo(title='Warning',message='Scale has to be a number')
        return
    Dict = mimic_dict(src)
    lbl_dict.configure(text=src, wraplength=500)
    txt = print_mimic(Dict, f_word, scale)
    scrol_result.delete(1.0,END)
    scrol_result.insert(INSERT, txt)
    return
#change the source of the text
def dict_refresh():
    s_file_refresh()
    src =text_import(lbl_source.cget('text'))
    #Dict = mimic_dict(src)
    lbl_dict.configure(text=src)
    scrol_result.delete(1.0, END)
    return
#button trigger
def b_clicked():
    generate(lbl_dict.cget('text'))

#if __name__=='__main__':
root = tk.Tk()
root.title('Text generator')
root.geometry('900x500')
lbl_com1 = tk.Label(root,text='Start the story with any word, for the exit input "stop":')
lbl_com1.grid(column=1, row=1,sticky="SW")
lbl_com2 = tk.Label(root,text='Source file: ')
lbl_com2.grid(column=0,row=0,sticky='NE')
lbl_source = tk.Label(root,text='')
lbl_source.grid(column=1,row=0)
txt_w=tk.Entry(root,width=100)
txt_w.grid(column=1,row=2,pady=10)
lbl_com3 = tk.Label(root,text='Result:')
lbl_com3.grid(column=0,row=4,sticky='NE')
#lbl_result = tk.Label(root,text='',wraplength=500)
#lbl_result.grid(column=1,row=4)
scrol_result = scrolledtext.ScrolledText(root,width=70, height=10)
scrol_result.grid(column=1,row=4)
lbl_dist = tk.Label(root,text = ' ')
lbl_dist.grid(column=1,row=5)
lbl_com4=tk.Label(root, text='Fragment of \nthe source text:')
lbl_com4.grid(column=0,row=6,sticky='NE')
lbl_dict = tk.Label(root,text='',width = 100)
lbl_dict.grid(column=0,row=7,columnspan=2)
fr = tk.Frame(root)
fr.grid(column=2, row=2)
btn = tk.Button(fr,text='Generate',command=b_clicked)
btn.grid(column = 0, row=0)
btn_source = tk.Button(fr,text = "Get New Source",command = dict_refresh)
btn_source.grid(column=1,row=0)
f2 = tk.Frame(root)
f2.grid(column=2,row=4)
lbl_scale = tk.Label(f2,text='The scale of output text:')
lbl_scale.grid(row=0)
txt_w2 = tk.Entry(f2,width = 5)
txt_w2.grid(row=1)
txt_w2.insert(0,'1')
root.mainloop()