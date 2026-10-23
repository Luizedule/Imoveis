#!/usr/bin/env python3
"""Aplica a marca d'água (logo colorido, centro, 30% de opacidade, altura = 5,4% da largura da foto)
nas fotos das páginas. Idempotente: só marca arquivos que ainda não constam em _assets/marcadas.txt.
Uso: python3 _assets/marca.py vl0128 [vl0182 ...]   (sem argumentos: todas as pastas com fotos/)
Originais ficam no histórico do git (commit anterior) — para desfazer: git checkout <commit>^ -- <pasta>/fotos"""
import os, sys
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO=Image.open(R+'/_assets/logo_marca.png').convert('RGBA')
LST=R+'/_assets/marcadas.txt'
feitas=set(open(LST).read().split('\n')) if os.path.exists(LST) else set()
pastas=sys.argv[1:] or sorted(d for d in os.listdir(R) if os.path.isdir(f'{R}/{d}/fotos') and d not in ('fotos',))
n=0
for p in pastas:
    for f in sorted(os.listdir(f'{R}/{p}/fotos')):
        if not f.lower().endswith(('.webp','.jpg','.jpeg','.png')): continue
        rel=f'{p}/fotos/{f}'
        if rel in feitas: continue
        im=Image.open(f'{R}/{rel}').convert('RGBA')
        h=max(1,int(im.width*0.09*0.6)); lg=LOGO.resize((int(LOGO.width*h/LOGO.height),h),Image.LANCZOS)
        lg.putalpha(lg.split()[3].point(lambda v:int(v*0.30)))
        im.alpha_composite(lg,((im.width-lg.width)//2,(im.height-lg.height)//2))
        im=im.convert('RGB')
        if f.lower().endswith('.webp'): im.save(f'{R}/{rel}','WEBP',quality=85,method=6)
        else: im.save(f'{R}/{rel}',quality=88)
        feitas.add(rel); n+=1
open(LST,'w').write('\n'.join(sorted(x for x in feitas if x)))
print('marcadas:',n)
