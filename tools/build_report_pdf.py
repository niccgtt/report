import json, os, sys
import fitz
repo=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path=os.path.join(repo,'Page3','report-data.json')
out=os.path.join(repo,'Page3','generated-report.pdf')
font_candidates=['C:/Windows/Fonts\\msyh.ttc','C:/Windows/Fonts\\simsun.ttc','/c/Windows/Fonts/msyh.ttc','/c/Windows/Fonts/msyh.ttf','/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']
font=next((p for p in font_candidates if os.path.exists(p)),None)
if not font: raise SystemExit('CJK font not found')
with open(data_path,encoding='utf-8') as f: d=json.load(f)
labels=[('设备名称','deviceName'),('制造单位','manufacturer'),('设备类别','category'),('产品编号','productNo'),('设备型号','model'),('检验人员','inspector'),('检验类型','inspectionType'),('报告编号','reportNo'),('检验日期','inspectionDate'),('防伪码','antiFakeCode'),('检验单位','inspectionUnit')]
doc=fitz.open(); page=doc.new_page(width=595,height=842)
# neutral technical-report layout with the same data source; no external backend required
page.draw_rect(fitz.Rect(0,0,595,842),color=(0.94,0.97,1),fill=(0.94,0.97,1))
page.insert_text((48,52),d.get('title','报告'),fontfile=font,fontsize=22,color=(0.03,0.25,0.55))
page.draw_line((48,68),(547,68),color=(0.15,0.45,0.8),width=1.2)
y=105
for label,key in labels:
 page.draw_rect(fitz.Rect(48,y-18,160,y+10),color=(0.65,0.76,0.88),fill=(0.87,0.93,0.98),width=.6)
 page.draw_rect(fitz.Rect(160,y-18,547,y+10),color=(0.65,0.76,0.88),fill=(1,1,1),width=.6)
 page.insert_text((58,y),label,fontfile=font,fontsize=10,color=(0.05,0.18,0.35))
 value=str(d.get(key,''))
 # wrap long values across the value cell without clipping
 words=[]; line=''
 for ch in value:
  test=line+ch
  if fitz.get_text_length(test,fontname='china-s',fontsize=10)>375 and line:
   words.append(line); line=ch
  else: line=test
 words.append(line)
 for i,line in enumerate(words[:2]): page.insert_text((170,y+i*13),line,fontfile=font,fontsize=10,color=(0.1,0.1,0.1))
 y+=34 if len(words)>1 else 28
page.insert_text((48,730),'报告预览文件由页面数据生成',fontfile=font,fontsize=10,color=(0.35,0.35,0.35))
page.insert_text((48,770),d.get('support',''),fontfile=font,fontsize=10,color=(0.05,0.25,0.55))
doc.save(out,garbage=4,deflate=True)
print(out,os.path.getsize(out))
