#!/usr/bin/python

'''
aangenomen dat het base64 betreft (op basis van tekenset)
aangenomen dat het een geshuffeld alfabet is
is het een kwestie van het juiste alfabet vinden.

de encoded string is als volgt:

IyVjGQSXF+XLt1OOH+XPeR4uVGR=

de string is 28 tekens lang, 1 padding, het alfabet behoeft slechts 20 tekens 
lang te zijn (uitgaande van gelijk gebleven padding teken)
De originele tekst bestond dan uit 20 tekens (6x3 + 1x2)

gokjes (untested):
 - gelukkig kerstfeest!

als we dit in groepjes van 4 verdelen (4 encoded chars = 3 decoded chars)

IyVj GQSX F+XL t1OO H+XP eR4u VGR=

kunnen we al beginnen met onze zoektocht naar constraints, de volgende zijn te vinden:

VGR=
  - levert 2 printbare karakters op
  - geen hoofdletters, waarschijnlijk geen spatie, mogelijk een uitroepteken of punt

F+XL & H+XP
  - enkel kleine letters en spaties
  - elke valide input set voor F+XL moet een set hebben in H+XP met 1e en 3e karakter anders

t1OO
  - enkel kleine letters en spaties
  - laatste twee encoded chars zijn gelijk (enorme constraint :))

'''

import string
import base64
import itertools
import time

def customBase64Decode(s, a='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'):
  STANDARD_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  DECODE_TRANS = string.maketrans(a, STANDARD_ALPHABET)
  return base64.b64decode(s.translate(DECODE_TRANS))

t = 'IyVjGQSXF+XLt1OOH+XPeR4uVGR='

stuff = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
combis4 = []
combis3 = []
combis2 = []
for a in list(stuff):
  for b in list(stuff):
    for c in list(stuff):
      for d in list(stuff):
        combis4.append(a+b+c+d)
      combis3.append(a+b+c)
    combis2.append(a+b)
print len(combis4)
print len(combis3)
print len(combis2)

#t100
valchar = 'abcdefghijklmnopqrstuvwxyz '
valset = set(valchar)
valids4 = []
total = 64*64*64
count = 0
t = time.time()
for subset in combis3:
  count = count + 1
  if len(set(subset)) == 3:
    a = ''.join(subset) + subset[2]
    c = base64.b64decode(a)
    b = list(c)
    if (b[0] in valset):
      if (b[1] in valset):
        if (b[2] in valset):
          valids4.append(a)
          #print a, c 
  if (t < time.time()):
    print '%8d / %8d : %3d %8d' % (count, total, round(100 * count / total), len(valids4))
    t = t + 1

print 'found %d valids4' % len(valids4)

#F+XL (& H+XP)
valchar = 'abcdefghijklmnopqrstuvwxyz '
valset = set(valchar)
valids3 = []
total = len(stuff) * len(stuff) * len(stuff) * len(stuff)
count = 0
t = time.time()
for subset in combis4:
  count = count + 1
  if len(set(subset)) == 4:
    a = ''.join(subset)
    c = base64.b64decode(a)
    b = list(c)
    if (b[0] in valset):
      if (b[1] in valset):
        if (b[2] in valset):
          valids3.append(a)
          #print a, c 
  if (t < time.time()):
    print '%8d / %8d : %3d %8d' % (count, total, round(100 * count / total), len(valids3))
    t = t + 1

print 'found %d valids3' % len(valids3)

#H+XP
valids5 = []
total = len(valids3)
count = 0
for v in valids3:
  count = count + 1
  vl = list(v)
  found = False
  for subset in combis2:
    if (len(set(subset + v)) == 6):
      a = subset[0] + vl[1] + vl[2] + subset[1]
      c = base64.b64decode(a)
      b = list(c)
      if (b[0] in valset) and (b[2] in valset):
        found = True
        break
  if found:
    valids5.append(v)
  if (t < time.time()):
    print '%8d / %8d : %3d %8d' % (count, total, round(100 * count / total), len(valids5))
    t = t + 1

print 'found %d valids5' % len(valids5)
print 'set valid3 to same set'
valids3 = valids5

#VGR=
valchar = 'abcdefghijklmnopqrstuvwxyz0123456789 .!'
valset = set(valchar)
valids7 = []
total = len(stuff) * len(stuff) * len(stuff)
count = 0
t = time.time()
for subset in combis3:
  count = count + 1
  if len(set(subset)) == 3:
    a = ''.join(subset) + '='
    c = base64.b64decode(a)
    b = list(c)
    if (b[0] in valset):
      if (b[1] in valset):
        valids7.append(a)
  if (t < time.time()):
    print '%8d / %8d : %3d %8d' % (count, total, round(100 * count / total), len(valids7))
    t = t + 1

print 'found %d valids7' % len(valids7)

#t100 & VGR=
valids47 = []
total = len(valids4) * len(valids7)
count = 0
t = time.time()
for v in valids4:
  for x in valids7:
    if (len(set(v+x)) == 7):
      valids47.append(v + x)
    count = count + 1
  if (t < time.time()):
    print '%d / %d : %3d %d' % (count, total, round(100 * count / total), len(valids47))
    t = t + 1

print 'found %d valids47' % len(valids47)

#deze duurt heeeeeel lang
#t100 & VGR= & #H+XP
valids457 = []
total = len(valids5) * len(valids47)
count = 0
t = time.time()
for v in valids47:
  for x in valids5:
    if (len(set(v+x)) == 11):
      valids457.append(v + x)
    count = count + 1
  if (t < time.time()):
    print '%d / %d : %3d %d' % (count, total, round(100 * count / total), len(valids457))
    t = t + 1

print 'found %d valids457' % len(valids457)

