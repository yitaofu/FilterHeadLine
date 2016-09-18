#!/usr/bin/env python
#coding: utf-8

import sys
import json
import types

def is_ok(c):
    n = ord(c)
    if ( ( n >= 32 and n < 127 ) or (n >= 13312 and n <= 40959) ):
        return 1
    else:
        return 0
def tidy(s): return ''.join([ c if 1 == is_ok(c) else ' ' for c in s.decode('utf-8') ]).encode('utf8')

def get_max_img(attach_types):
    i = 0
    s = 0
    while i < len(attach_types):
        t = attach_types[i]
        while t != 2 and i < len(attach_types) :
            t = attach_types[i]
            i += 1
        if t >= len(attach_types): break
        k = 0
        while t == 2 and i < len(attach_types):
            t = attach_types[i]
            k += 1
            i += 1
        if k > s : s = k
        i += 1
    return s

def get_mix_num(attach_types):
    new_types = []
    for t in attach_types:
        if t == 1 or t == 2 :
            new_types.append(t)
    if len(new_types) == 0 : return 0
    clean_types = []
    for t in new_types:
        if len(clean_types) == 0:
            clean_types.append(t)
        if t != clean_types[-1]:
            clean_types.append(t)
    s = len(clean_types)
    s = s if s > 2 else 0
    s = int(s/2)
    return s

if 0: # just for test
    print 0,get_mix_num([1,2])
    print 1,get_mix_num([1,2,1])
    print 1,get_mix_num([2,1,2])
    print 2,get_mix_num([1,2,1,2])
    print 2,get_mix_num([1,1,2,2,1,2,1])
    print 3,get_mix_num([1,1,2,2,1,2,1,2])
    sys.exit()

def is_ascii(c):n=ord(c);return 1 if n>32 and n<=126 else 0
def get_char_cnt(text):
    flags = [ is_ascii(c) for c in text.replace('\n',' ').replace('\r',' ').decode('utf8') ]
    if len(flags) <= 1: return len(flags)
    last_c = 0
    total_cnt = len(flags)
    ascii_cnt = sum(flags)
    for i in range(len(flags)):
        c = flags[i]
        if last_c == 1 and c == 1:
            flags[i] = 0
        last_c = c 
    space_cnt = len([ 1 for c in text.replace('\n',' ').replace('\r',' ') if c == ' ' ])
    return total_cnt - ascii_cnt + sum(flags) - space_cnt
if 0:
    print 10,get_char_cnt('ab;;[]1231`4\n83543\r877.,./~#$% ^&*((*你是谁 我是谁')
    print 3,get_char_cnt('ab;;[]1231`483543877.,./~#$%^&*((*是谁')
    print 4,get_char_cnt('我ab;;[]1231`483543877.,./~#$%^&*((*是谁')
    sys.exit()

def get_w_h(img):
    uri = img.split('?')
    w, h = 0, 0
    if len(uri) == 2:
        wh = dict( g.split('=') for g in uri[1].split('&') )
        w = int(wh['w']) if 'w' in wh else 0
        h = int(wh['h']) if 'h' in wh else 0
    return [w,h]


def get_max_proportion(char_cnts):
    total_n = 0.1
    max_n = 0.01
    for n in char_cnts:
        if n > max_n :
            max_n = n
        if n > 0:
            total_n = total_n + n
    return max_n / total_n 

fileRead = open("abc")
fileWrite = open("result", 'w')
count = 0
for line in fileRead.readlines():
    fields =line.strip().split('\1')
    if len(fields) != 12 : continue
    sellerId,diaryId,title,content,attachments,status,add_time,update_time,atten_num,version,edit_time,shareId = fields
    if int(status) != 0 : continue
    #if add_time < '2016-01-18' : continue
    content = content.rstrip().strip().replace('\n',' ').replace('\r',' ').replace('\f',' ').replace('\t',' ')
    title = tidy(title.rstrip().strip().replace('\n',' ').replace('\r',' ')
            .replace('\t',' ').replace('"',' ').replace("'",' ').replace('\\','').replace('`',''))
    videos_cnt = 0
    items = []
    attach_types = []
    imgs= []
    char_cnts = []
    w = 0
    h = 0
    #if 1:
    count = count + 1
    try:
        fileWrite.write("--------------------" + str(count) + "------------------------\n")
        fileWrite.write("ID: " + diaryId + "\n")
        attachments = json.loads(attachments)
        if type(attachments) == type([]) and len(attachments) >= 1:
            for a in attachments:
                if type(a) == type({}):
                    if a.has_key('type') and int(a['type']) == 1 and a.has_key('text'):
                        #if(len(a['text'] > 30)):
                        #attach_types.append(1)
                        #char_cnts.append(len(a['text']))
                        content += a['text'].encode('utf8').replace('\n',' ').replace('\r',' ').replace('\f',' ').replace('\t',' ')
			fileWrite.write("content:" + content + "\n")
                    if ( a.has_key('type') and int(a['type']) == 2 ) or ( 
                            a.has_key('url') and a['url'].count('wd.geilicdn.com') > 0 
                            and a['url'].count('http') > 0 ):
                        attach_types.append(2)
                        img = a['url'].encode('utf8')
                        imgs.append(img)
                        char_cnts.append(-1)
			fileWrite.write("img:" + img + "\n")
                    if a.has_key('type') and int(a['type']) == 3 and a.has_key('goods'): 
                        attach_types.append(1)
                        items.append( a['goods']['itemID'].encode('utf8'))
                        char_cnts.append(-1)
			fileWrite.write("goods:\n")
			fileWrite.write("itemID:" + a['goods']['itemID'].encode('utf8') + "\n")
			fileWrite.write("h5url:" + a['goods']['h5url'].encode('utf8') + "\n")
			fileWrite.write("itemName:" + a['goods']['itemName'].encode('utf8') + "\n")
			fileWrite.write("price:" + a['goods']['price'].encode('utf8') + "\n")
			print "goods:"
			print "itemID:" + a['goods']['itemID'].encode('utf8')
			print "h5url:" + a['goods']['h5url'].encode('utf8')
			print "itemName:" + a['goods']['itemName'].encode('utf8')
			print "price:" + a['goods']['price'].encode('utf8')
                    if a.has_key('type') and int(a['type']) == 4 :
                        videos_cnt += 1
                        attach_types.append(1)
                        char_cnts.append(-1)
	fileWrite.write("----------------------------------------------\n")
                        
    except Exception,e:
        b = 'neng za di, jiu zhe me di le'
    char_cnt = get_char_cnt(content)
    pics_cnt = len(imgs)
    goods_cnt = len(items)
    first_img = imgs[0] if len(imgs) > 0 else ''
    w = 0
    h = 0
    if len(imgs) > 0:
        wh = get_w_h(imgs[0])
        w = wh[0]
        h = wh[1]
    if w == 0 : w = 640
    #print 'w',w
    #print 'h',h
    cont_img = get_max_img(attach_types)
    mix_num = get_mix_num(attach_types)
    max_ppt = get_max_proportion(char_cnts)
    '''
    print '\t'.join( [ sellerId, diaryId, add_time, atten_num, 
        str(pics_cnt), str(goods_cnt), str(videos_cnt), str(char_cnt),
        str(cont_img), str(mix_num), 
        tidy(title), str(w), str(h), first_img, str(max_ppt), content ] )
    '''

fileRead.close()
fileWrite.close()
