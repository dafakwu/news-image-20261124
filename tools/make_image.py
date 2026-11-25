from PIL import Image, ImageDraw, ImageFont
import math
W=H=1024
im=Image.new('RGB',(W,H),'#f5f0e4'); d=ImageDraw.Draw(im)
NAVY='#142b40'; INK='#20394e'; MUT='#52616b'; PAPER='#fffaf0'; RULE='#bcb4a4'; RED='#bd4934'; GOLD='#cf9c42'; TEAL='#287c86'; BLUE='#52658a'; GREEN='#377b60'
ser='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'; sb='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'; san='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; b='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def F(n,bold=False,serif=False): return ImageFont.truetype(sb if serif and bold else ser if serif else b if bold else san,n)
def T(x,y,s,n=11,c=NAVY,bold=False,serif=False): d.text((x,y),s,font=F(n,bold,serif),fill=c)
def fitwrap(s,width,font):
 rows=[]; row=''
 for word in s.split():
  cand=(row+' '+word).strip()
  if d.textbbox((0,0),cand,font=font)[2]<=width: row=cand
  else:
   if row: rows.append(row)
   row=word
 if row: rows.append(row)
 return rows
def wrap(x,y,s,width,n=11,c=INK,bold=False,serif=False,leading=None,maxrows=3,minsize=11,maxheight=None):
 size=n
 while size>=minsize:
  font=F(size,bold,serif); rows=fitwrap(s,width,font)
  step=max(leading or 0, math.ceil(size*1.2))
  step=max(leading or 0, math.ceil(size*1.2))
  height=(len(rows)-1)*step+size+2
  if len(rows)<=maxrows and (maxheight is None or height<=maxheight) and all(d.textbbox((0,0),r,font=font)[2]<=width for r in rows): break
  size-=1
 assert size>=minsize and len(' '.join(rows).split())==len(s.split()), f'Text does not fit: {s}'
 assert y+(len(rows)-1)*step+size+2<=H, f'Text falls outside image: {s}'
 for i,row in enumerate(rows): d.text((x,y+i*step),row,font=font,fill=c)
 return size
def pill(x,y,label,color):
 font=F(10,True); tw=d.textbbox((0,0),label,font=font)[2]; d.rounded_rectangle((x,y,x+tw+14,y+19),radius=6,fill=color); T(x+7,y+3,label,10,'white',True)
def badge(cx,cy,n,r=11):
 d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=RED,outline='white',width=1); s=str(n); bb=d.textbbox((0,0),s,font=F(10,True)); d.text((cx-(bb[2]-bb[0])/2,cy-(bb[3]-bb[1])/2-2),s,font=F(10,True),fill='white')
# masthead
T(24,8,'THE WORLD IN ONE DAY',11,NAVY,True); T(610,8,'26 STORIES  ·  8 REGIONS  ·  TUESDAY 24 NOVEMBER 2026',10,NAVY,True)
d.line((24,27,1000,27),fill=NAVY,width=1)
T(23,28,'Tuesday 24 November 2026',53,NAVY,True,True)
d.line((24,91,1000,91),fill=NAVY,width=2)
T(24,96,'TOP LINES',11,RED,True,True); T(105,96,"Huang's return lifts Asian chips - Iran says tankers hit mines in Hormuz - Baghdad moves on Kurdish oilfields - Sanofi's $41bn deal",11,NAVY,False,True)
d.line((24,116,1000,116),fill=RULE,width=1)
# Hero panels
hero_y=123; hero_h=250; hero_w=316; xs=[24,354,684]
hero_data=[('ASIA / MARKETS  ·  TAIPEI',"Huang's return sparks record Asian chip rally",'Taiex +8.99% to 40,122, its biggest points gain. Kospi +6.3%; Nikkei +3.9%; TSMC hit its 10% limit.',RED),('GULF  ·  HORMUZ','Iran says 3 tankers hit mines in Hormuz','IRGC Navy says fires broke out on all three. Tehran vows to confront the US naval blockade.',TEAL),('EUROPE / WAR  ·  MOSCOW','Russia says it downed 699 Ukrainian drones','355 aimed at Moscow region. Strike kills 2 in Zaporizhzhia; Russian jet drone flies 20 km into Poland.',BLUE)]
for i,(tag,title,body,col) in enumerate(hero_data):
 x=xs[i]; d.rounded_rectangle((x,hero_y,x+hero_w,hero_y+hero_h),radius=5,fill=PAPER,outline=RULE,width=1); d.rectangle((x,hero_y,x+hero_w,hero_y+125),fill='#dfe9e5'); badge(x+16,hero_y+17,i+1,12)
 if i==0:
  # city and bold upward market chart
  d.rectangle((x,hero_y+95,x+hero_w,hero_y+125),fill='#bfd4ce')
  for bx,bh in [(x+18,32),(x+50,48),(x+84,35),(x+116,62),(x+150,45),(x+185,57),(x+220,38),(x+254,53),(x+285,29)]:
   d.rectangle((bx,hero_y+96-bh,bx+19,hero_y+96),fill='#36566b')
   for wy in range(hero_y+96-bh+7,hero_y+91,11): d.rectangle((bx+5,wy,bx+9,wy+4),fill='#e7c570')
  pts=[(x+12,hero_y+88),(x+61,hero_y+77),(x+104,hero_y+82),(x+150,hero_y+54),(x+198,hero_y+59),(x+247,hero_y+30),(x+294,hero_y+22)]; d.line(pts,fill='#c43e32',width=5)
  for px,py in pts:d.ellipse((px-3,py-3,px+3,py+3),fill='#c43e32')
  d.rounded_rectangle((x+190,hero_y+7,x+302,hero_y+38),radius=5,fill='#c9e3d1',outline=GREEN,width=2); T(x+199,hero_y+8,'+8.99%',24,GREEN,True,True)
  # chip icon
  d.rectangle((x+18,hero_y+17,x+63,hero_y+58),fill='#b9d8c7',outline=NAVY,width=2); d.rectangle((x+27,hero_y+26,x+54,hero_y+49),fill='#f1d37e',outline=NAVY,width=1)
  for j in range(5): d.line((x+23+j*9,hero_y+12,x+23+j*9,hero_y+18),fill=NAVY,width=2); d.line((x+23+j*9,hero_y+58,x+23+j*9,hero_y+64),fill=NAVY,width=2)
 elif i==1:
  d.rectangle((x,hero_y+79,x+hero_w,hero_y+125),fill='#397f89')
  for yy in [92,111]: d.arc((x+8,hero_y+yy,x+132,hero_y+yy+20),180,350,fill='#acd0c6',width=2)
  # tanker with clear hull, deck, smoke and three fire tongues
  d.polygon([(x+47,hero_y+74),(x+282,hero_y+74),(x+249,hero_y+100),(x+75,hero_y+100)],fill='#172f43'); d.rectangle((x+103,hero_y+54,x+225,hero_y+74),fill='#f1eee2',outline=NAVY,width=1); d.rectangle((x+122,hero_y+42,x+147,hero_y+55),fill=RED); d.rectangle((x+187,hero_y+42,x+206,hero_y+55),fill=RED)
  for fx,hh in [(139,29),(167,38),(193,26)]:
   d.polygon([(x+fx,hero_y+53),(x+fx-10,hero_y+37),(x+fx-3,hero_y+25-hh//5),(x+fx+5,hero_y+39),(x+fx+12,hero_y+26),(x+fx+13,hero_y+53)],fill='#f28b35')
  for j in range(4): d.ellipse((x+142+j*8,hero_y+3-j*2,x+159+j*9,hero_y+23-j*2),fill='#667275')
  # sea mine
  d.ellipse((x+40,hero_y+90,x+52,hero_y+102),fill='#293b43')
  for a in range(0,360,45):
   ax=x+46+int(10*math.cos(math.radians(a))); ay=hero_y+96+int(10*math.sin(math.radians(a))); d.line((x+46,hero_y+96,ax,ay),fill='#293b43',width=2)
  # inset map of Hormuz between Iran and Oman
  d.rounded_rectangle((x+234,hero_y+5,x+309,hero_y+54),radius=3,fill='#fffaf0',outline=NAVY,width=1); d.polygon([(x+237,hero_y+10),(x+264,hero_y+8),(x+262,hero_y+30),(x+248,hero_y+35),(x+239,hero_y+28)],fill='#d8ccb4'); d.polygon([(x+274,hero_y+34),(x+300,hero_y+28),(x+305,hero_y+50),(x+277,hero_y+50)],fill='#d8ccb4'); T(x+239,hero_y+10,'IRAN',8,NAVY,True); T(x+274,hero_y+39,'OMAN',8,NAVY,True); T(x+262,hero_y+27,'STRAIT',7,RED,True)
 else:
  # schematic regional map labels, Kyiv, Moscow, Zaporizhzhia, Poland
  d.polygon([(x+23,hero_y+24),(x+56,hero_y+10),(x+94,hero_y+17),(x+102,hero_y+40),(x+89,hero_y+68),(x+61,hero_y+77),(x+34,hero_y+59)],fill='#c8d6c7',outline=NAVY)
  d.polygon([(x+121,hero_y+15),(x+159,hero_y+9),(x+206,hero_y+20),(x+223,hero_y+44),(x+205,hero_y+66),(x+167,hero_y+74),(x+139,hero_y+55),(x+115,hero_y+41)],fill='#dfcfb5',outline=NAVY)
  d.polygon([(x+216,hero_y+57),(x+247,hero_y+47),(x+281,hero_y+58),(x+300,hero_y+82),(x+273,hero_y+95),(x+236,hero_y+87)],fill='#d5dcca',outline=NAVY)
  T(x+27,hero_y+17,'POLAND',9,NAVY,True); T(x+145,hero_y+12,'RUSSIA',9,NAVY,True)
  mx,my=x+174,hero_y+35; d.polygon([(mx,my-7),(mx+2,my-2),(mx+7,my-2),(mx+3,my+1),(mx+5,my+7),(mx,my+3),(mx-5,my+7),(mx-3,my+1),(mx-7,my-2),(mx-2,my-2)],fill=RED)
  # Halo-backed labels keep text clear over borders and routes.
  d.rounded_rectangle((mx+8,my-14,mx+70,my-1),radius=3,fill=PAPER); T(mx+11,my-13,'MOSCOW',8,RED,True)
  d.rounded_rectangle((x+216,hero_y+79,x+303,hero_y+94),radius=3,fill=PAPER); T(x+219,hero_y+80,'UKRAINE',9,NAVY,True)
  # numerous drone marks converge on Moscow
  for dx,dy in [(28,62),(56,91),(89,71),(113,101),(234,18),(281,35)]:
   tx,ty=x+dx,hero_y+dy; d.line((tx,ty,mx,my),fill='#bd4934',width=1); d.polygon([(tx,ty-4),(tx+4,ty),(tx,ty+4),(tx-4,ty)],fill=RED)
  # burst at Zaporizhzhia, Poland incursion crossing arrow
  zx,zy=x+240,hero_y+70
  for a in range(0,360,45):
   ex=zx+int(12*math.cos(math.radians(a))); ey=zy+int(12*math.sin(math.radians(a))); d.line((zx,zy,ex,ey),fill=RED,width=2)
  d.ellipse((zx-4,zy-4,zx+4,zy+4),fill=RED); d.rounded_rectangle((zx-42,zy+10,zx+45,zy+25),radius=3,fill=PAPER); T(zx-39,zy+11,'ZAPORIZHZHIA',7,RED,True)
  d.line((x+96,hero_y+58,x+37,hero_y+38),fill='#175e95',width=3); d.polygon([(x+37,hero_y+38),(x+48,hero_y+36),(x+42,hero_y+47)],fill='#175e95'); T(x+26,hero_y+77,'20 km into Poland',8,'#175e95',True)
 pill(x+10,hero_y+132,tag,col)
 wrap(x+10,hero_y+155,title,296,24,NAVY,True,True,27,2,12)
 wrap(x+10,hero_y+211,body,296,11,MUT,False,False,13,3,11)
# tile grid 4-15 in 6x2 grid
stories=[
('IRAQ','Baghdad moves on Kurdish oil','Kirkuk, Diyala, Salahaddin, Nineveh; Kurdish leaders object.',GOLD,'derrick'),('GAZA','Strike kills Hamas security chief','Naeem Abu Nahel and six others killed.',RED,'fire'),('PARIS / PHARMA','Sanofi buys Insmed for $41bn','$175 a share in cash; biggest pharma deal in 3 years.',BLUE,'pill'),('MALAYSIA','Malaysia to deport 6,803 to Myanmar','1,500 by navy, 5,303 by air in December.',TEAL,'ship'),('INDONESIA','Factory fire toll hits 26','Cikande, Banten; 28 still missing.',RED,'fire'),('PACIFIC','Solomons drop China pact','PM Wale signs a security treaty with Australia.',TEAL,'handshake'),('AFRICA / SPORT','Senegal get AFCON title back','Court overturns award of 2025 title to Morocco.',GREEN,'trophy'),('EU / TRADE','EU caps Chinese hybrids','Quota of 350,000 a year from 1 December.',BLUE,'car'),('BANGLADESH','Pay protests shut 481 factories','Police fire tear gas near Dhaka.',RED,'factory'),('CHESS','World chess title match opens','Sindarov vs Gukesh; Game 1 drawn in 38 moves.',BLUE,'chess'),('KOREA','Russian jets enter Korea zone','Ulleung island briefly told to shelter.',TEAL,'jet'),('UK','UK: record 5,258 heat deaths','Highest summer toll since records began, says UKHSA.',RED,'thermometer')]

def icon(x,y,kind,color):
 # small original vector glyphs, consistently readable
 if kind=='derrick':
  d.line((x+9,y+24,x+18,y+2,x+26,y+24),fill=color,width=2);d.line((x+13,y+14,x+24,y+14),fill=color,width=2);d.line((x+5,y+25,x+29,y+25),fill=color,width=2);d.line((x+18,y+3,x+31,y+3),fill=color,width=2)
 elif kind=='pill':
  d.rounded_rectangle((x+7,y+8,x+31,y+22),radius=7,fill='#f0d19b',outline=color,width=2);d.line((x+19,y+9,x+19,y+21),fill=color,width=2)
 elif kind=='ship':
  d.polygon([(x+4,y+18),(x+32,y+18),(x+26,y+26),(x+10,y+26)],fill=color);d.rectangle((x+13,y+9,x+25,y+18),fill='#d9e6e4',outline=color);d.line((x+3,y+29,x+33,y+29),fill=TEAL,width=2)
 elif kind=='fire':
  d.polygon([(x+18,y+2),(x+9,y+16),(x+13,y+24),(x+20,y+28),(x+28,y+19),(x+25,y+11),(x+21,y+15)],fill='#ed8733');d.ellipse((x+16,y+19,x+22,y+27),fill='#ffe18a')
 elif kind=='handshake':
  d.line((x+5,y+12,x+13,y+7,x+19,y+12,x+25,y+7,x+33,y+12),fill=color,width=3);d.line((x+11,y+14,x+20,y+22,x+27,y+15),fill=color,width=3);d.line((x+5,y+12,x+11,y+20),fill=color,width=3)
 elif kind=='trophy':
  d.rectangle((x+12,y+5,x+24,y+20),fill='#e5bd57',outline=color,width=2);d.arc((x+5,y+6,x+15,y+20),60,290,fill=color,width=2);d.arc((x+21,y+6,x+31,y+20),250,120,fill=color,width=2);d.line((x+18,y+20,x+18,y+27),fill=color,width=2);d.line((x+11,y+28,x+25,y+28),fill=color,width=2)
 elif kind=='car':
  d.rounded_rectangle((x+5,y+13,x+32,y+24),radius=3,fill='#d4e3e8',outline=color,width=2);d.polygon([(x+10,y+13),(x+14,y+7),(x+25,y+7),(x+29,y+13)],fill='#d4e3e8',outline=color);d.ellipse((x+9,y+22,x+15,y+28),fill=NAVY);d.ellipse((x+24,y+22,x+30,y+28),fill=NAVY)
 elif kind=='factory':
  d.rectangle((x+5,y+14,x+32,y+28),fill='#cfd8d4',outline=color,width=2);d.polygon([(x+5,y+14),(x+13,y+8),(x+13,y+14),(x+21,y+8),(x+21,y+14)],fill='#cfd8d4',outline=color);d.rectangle((x+26,y+3,x+30,y+14),fill=color)
 elif kind=='chess':
  d.polygon([(x+7,y+28),(x+12,y+25),(x+10,y+17),(x+14,y+13),(x+13,y+7),(x+18,y+3),(x+23,y+7),(x+22,y+13),(x+26,y+17),(x+24,y+25),(x+29,y+28)],fill='#d9c9a9',outline=color);d.line((x+5,y+29,x+31,y+29),fill=color,width=2)
 elif kind=='jet':
  d.polygon([(x+5,y+17),(x+17,y+14),(x+20,y+4),(x+23,y+4),(x+24,y+14),(x+33,y+17),(x+24,y+20),(x+22,y+27),(x+19,y+27),(x+17,y+20)],fill=color)
 elif kind=='thermometer':
  d.rounded_rectangle((x+14,y+4,x+22,y+24),radius=4,fill='white',outline=color,width=2);d.ellipse((x+11,y+19,x+25,y+33),fill=RED,outline=color,width=2);d.line((x+18,y+10,x+18,y+24),fill=RED,width=3)
# draw tile field
colors=[GOLD,RED,BLUE,TEAL,RED,TEAL,GREEN,BLUE,RED,BLUE,TEAL,RED]
base_y=381; cardw=158; cardh=100; gap=4
for j,(tag,title,body,col,kind) in enumerate(stories):
 row=j//6; coln=j%6; x=24+coln*(cardw+4); y=base_y+row*(cardh+4)
 d.rounded_rectangle((x,y,x+cardw,y+cardh),radius=4,fill=PAPER,outline=RULE,width=1); d.rectangle((x,y,x+3,y+cardh),fill=col); badge(x+14,y+13,j+4,9); icon(x+7,y+31,kind,col)
 # colored filled region tag
 pill(x+41,y+5,tag,col)
 wrap(x+41,y+24,title,110,14,NAVY,True,True,None,3,9,40)
 wrap(x+7,y+65,body,144,11,MUT,False,False,None,3,8,32)
# map and also list fill region
section_y=592
d.line((24,section_y,1000,section_y),fill=NAVY,width=2); T(24,section_y+6,'WHERE IT HAPPENED',13,NAVY,True,True)
# map canvas and list panel
d.rounded_rectangle((24,619,363,971),radius=4,fill='#e7e2d5',outline=RULE,width=1)
# Equirectangular projection fitted to the requested regional bounds.
mapbox=(36,624,351,800)
def xy(lon,lat): return (mapbox[0]+(lon+130)/290*(mapbox[2]-mapbox[0]),mapbox[1]+(70-lat)/115*(mapbox[3]-mapbox[1]))
continents=[
 [(-130,55),(-125,68),(-110,70),(-96,60),(-83,52),(-80,42),(-97,15),(-108,22),(-117,32),(-125,48)],
 [(-81,12),(-70,10),(-52,-2),(-44,-20),(-52,-38),(-68,-45),(-76,-35),(-80,-10)],
 [(-10,70),(30,70),(40,60),(30,50),(10,45),(-10,50)],
 [(-17,36),(0,37),(15,32),(32,31),(43,12),(34,-5),(27,-33),(16,-35),(7,-20),(-5,5),(-17,15)],
 [(30,70),(55,65),(80,60),(105,55),(130,50),(160,58),(150,40),(135,35),(125,20),(110,5),(100,10),(90,22),(75,8),(60,25),(45,35),(35,50)],
 [(112,-11),(133,-10),(151,-17),(154,-29),(138,-39),(116,-34)],
]
for poly in continents: d.polygon([xy(lon,lat) for lon,lat in poly],fill='#c5c4b5',outline='#9b9a8b')
places={1:(121.5,25.0),2:(56.5,26.5),3:(37.6,55.8),4:(44.4,35.5),5:(34.4,31.5),6:(2.35,48.85),7:(101.7,3.1),8:(106.1,-6.2),9:(160.0,-9.4),10:(-17.4,14.7),11:(4.35,50.85),12:(90.4,23.8),14:(130.9,37.5),15:(-0.1,51.5),16:(105.8,21.0),17:(55.9,25.8),18:(30.5,39.8),19:(-75.5,10.4),21:(30.5,50.4),22:(21.0,52.2),23:(32.5,15.6),24:(-74.0,40.7),25:(127.0,37.6),26:(24.1,56.9)}
coords={n:xy(*ll) for n,ll in places.items()}; nudged={}
for n in sorted(coords):
 px,py=coords[n]; qx,qy=px,py
 for attempt in range(160):
  if not any(math.hypot(qx-ox,qy-oy)<15 for ox,oy in nudged.values()): break
  angle=(n*137.5+attempt*31)%360; radius=8+attempt*.55
  qx=px+radius*math.cos(math.radians(angle)); qy=py+radius*math.sin(math.radians(angle))
 assert not any(math.hypot(qx-ox,qy-oy)<15 for ox,oy in nudged.values()), f'Pin collision: {n}'
 nudged[n]=(qx,qy)
 if math.hypot(qx-px,qy-py)>2: d.line((px,py,qx,qy),fill='#4b5660',width=1)
 r=7; d.ellipse((qx-r,qy-r,qx+r,qy+r),fill=RED,outline='white',width=1)
 label=str(n); bb=d.textbbox((0,0),label,font=F(9,True)); d.text((qx-(bb[2]-bb[0])/2,qy-(bb[3]-bb[1])/2-2),label,font=F(9,True),fill='white')
# list adjacent, 2 columns five rows. Numbers follow 1..15 tiles; list continues 16..
T(386,section_y+6,'ALSO ON TUESDAY 24 NOVEMBER',13,NAVY,True,True); d.line((386,section_y+27,1000,section_y+27),fill=RULE)
items=[('Hanoi','Hot pot restaurant gas blast kills 7'),('Ras Al Khaimah (UAE)','Bus hits truck, 13 killed'),('Eskisehir (Turkey)','Air force helicopter crash kills 5 crew'),('Cartagena (Colombia)','Gunmen take 25 hostage after failed robbery'),('Dhaka','Hasina says she will return on 16 December'),('Kyiv','Ukraine calls Libya drone strike self-defence'),('Warsaw','Poland says incursion deliberate; NATO AWACS'),('Khartoum','Army says it downed RSF drones'),('New York','Insmed shares jump 14% on Sanofi deal'),('Seoul','Samsung and SK Hynix jump 6.7%'),('Riga','Latvia: war may reach tipping point in 2027')]
for i,(place,desc) in enumerate(items):
 coln=0 if i<6 else 1; row=i if i<6 else i-6; x=386+coln*307; y=section_y+34+row*34; n=16+i
 badge(x+10,y+11,n,8); T(x+23,y+1,place,11,NAVY,True); wrap(x+23,y+14,desc,270,11,MUT,False,False,12,1,11)
# Day-in-numbers row fills the open space below the additional headlines.
T(386,839,'THE DAY IN NUMBERS',12,RED,True,True); d.line((386,858,1000,858),fill=RULE)
stats=[('40,122','Taiex close, a record points gain'),('5,006','Kospi back above 5,000'),('$175 a share','Sanofi pays for Insmed'),('481','factories halted in Bangladesh')]
for i,(number,detail) in enumerate(stats):
 x=386+i*154
 d.rounded_rectangle((x,867,x+146,967),radius=4,fill=PAPER,outline=RULE,width=1)
 wrap(x+8,875,number,130,14,RED,True,True,None,2,10,32)
 wrap(x+8,914,detail,130,11,NAVY,False,False,None,4,9,45)
# Compact date check occupies the freed space below the map.
d.rounded_rectangle((34,821,353,967),radius=4,fill=PAPER,outline=RULE,width=1)
T(45,829,'DATE CHECK',12,RED,True,True)
wrap(45,850,'Every item happened or was first reported on Tuesday 24 November 2026.',286,11,NAVY,True,False,13,3,11)
wrap(45,891,"Earlier news left out: Huang's reinstatement at Nvidia (Mon 23 Nov); EU's 22nd Russia sanctions package (Mon 23 Nov); COP31 ending without a deal (Sun 22 Nov).",286,11,MUT,False,False,13,6,11)
# footer bar at bottom
fy=978; d.rectangle((0,fy,1024,1024),fill=NAVY); T(24,fy+8,'Sources: Reuters · AP · AFP · BBC · CNA · Yonhap · FIDE · Sanofi · European Commission · UKHSA',10,'#e5e4da'); T(690,fy+8,'TUESDAY 24 NOVEMBER 2026 - ONE PAGE',11,'white',True)
im.save('entry.png',format='PNG',optimize=True)
