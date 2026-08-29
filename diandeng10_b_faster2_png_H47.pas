//{$define disp}
program diandeng;
{$mode objfpc}{$H+}

{ H47: keep one Bezout track in Euclid and recover the other by exact division. }
{ A and B use the same one-track Euclid, exact Karatsuba product and division. }

{$ifdef disp}
uses Windows, display;
const m=1000;
{$else}
uses Windows;
const m=100000;
{$endif}

const wb=32;
const mw=(m+wb-1)div wb;

type TVec=array[-2..mw]of LongWord;
     PVec=^TVec;
     TWordArray=array of LongWord;
     TMul8Table=array[0..65535] of Word;

var n:longword;
var i,j:longint;
var x,y,y1,y_,y_1,f,f1,c,c1:TVec;
var hf,hf1,hc,hc1:TVec;
var k:longint;
var hk:longint;
var o,ho:boolean;
var perfFreq,lastCounter:Int64;
var hasLastCounter:boolean;
var wn:longint;
var lastMask:LongWord;
var nMask:LongWord;
var nWord:longint;
var ones:TVec;
var v1,v2:TVec;
var mul8:TMul8Table;
var uKernel8:array[0..255] of LongWord;

{$ifdef disp}
var bb:pbitbuf;
var bp:pbitmap;
{$endif}

procedure VecNorm(var a:TVec);
begin
a[-2]:=0; a[-1]:=0;
if wn<=mw then a[wn]:=0;
if wn+1<=mw then a[wn+1]:=0;
a[wn-1]:=a[wn-1] and lastMask;
end;

procedure VecZero(var v:TVec);
var k2,hiw:longint;
begin
hiw:=wn+1; if hiw>mw then hiw:=mw;
for k2:=-2 to hiw do v[k2]:=0;
end;

procedure VecCopy(var a:TVec;const b:TVec);
var k2,hiw:longint;
begin
hiw:=wn+1; if hiw>mw then hiw:=mw;
for k2:=-2 to hiw do a[k2]:=b[k2];
VecNorm(a);
end;

procedure VecXorEq(var a:TVec;const b:TVec);
var k2:longint;
begin
for k2:=0 to wn-1 do a[k2]:=a[k2] xor b[k2];
VecNorm(a);
end;

procedure VecXorRaw(var a:TVec;const b:TVec); inline;
var k2:longint;
begin
for k2:=0 to wn-1 do a[k2]:=a[k2] xor b[k2];
end;

procedure VecXorHTo(var dst:TVec; const src:TVec; hi:longint); inline;
var k2:longint;
var left,cur,right:LongWord;
begin
left:=src[-1]; cur:=src[0];
for k2:=0 to wn-1 do
  begin
  right:=src[k2+1];
  dst[k2]:=dst[k2] xor (cur shl 1) xor (left shr 31) xor
           (cur shr 1) xor (right shl 31);
  left:=cur; cur:=right;
  end;
end;

procedure VecXorIHTo(var dst:TVec; const src:TVec; hi:longint); inline;
var k2:longint;
var left,cur,right:LongWord;
begin
left:=src[-1]; cur:=src[0];
for k2:=0 to wn-1 do
  begin
  right:=src[k2+1];
  dst[k2]:=dst[k2] xor cur xor (cur shl 1) xor (left shr 31) xor
           (cur shr 1) xor (right shl 31);
  left:=cur; cur:=right;
  end;
end;


procedure MaskDeg(var a:TVec;deg:longint);
var w:longint;
var rem:longint;
var msk:LongWord;
var k2:longint;
begin
if deg<0 then begin for k2:=0 to wn-1 do a[k2]:=0; VecNorm(a); exit; end;
w:=deg shr 5;
rem:=deg and 31;
msk:=LongWord($FFFFFFFF) shr (31-rem);
for k2:=w+1 to wn-1 do a[k2]:=0;
a[w]:=a[w] and msk;
VecNorm(a);
end;

function GetBit(const v:TVec;idx:longint):LongWord;
var w,b2:longint;
begin
if idx<0 then begin GetBit:=0; exit; end;
w:=idx shr 5;
b2:=idx and 31;
if w<0 then begin GetBit:=0; exit; end;
if w>=wn then begin GetBit:=0; exit; end;
GetBit:=(v[w] shr b2) and 1;
end;

procedure SetBit(var v:TVec;idx:longint;bit:LongWord);
var w,b2:longint;
begin
if idx<0 then exit;
w:=idx shr 5;
b2:=idx and 31;
if w<0 then exit;
if w>=wn then exit;
if bit<>0 then v[w]:=v[w] or (LongWord(1) shl b2)
else v[w]:=v[w] and not(LongWord(1) shl b2);
VecNorm(v);
end;

procedure VecShiftL1(var dst:TVec;const src:TVec);
var k2:longint;
begin
dst[-2]:=0; dst[-1]:=0;
for k2:=0 to wn-1 do
  dst[k2]:=(src[k2] shl 1) or (src[k2-1] shr 31);
if wn<=mw then dst[wn]:=0;
if wn+1<=mw then dst[wn+1]:=0;
VecNorm(dst);
end;

procedure VecShiftR1(var dst:TVec;const src:TVec);
var k2:longint;
begin
dst[-2]:=0; dst[-1]:=0;
for k2:=0 to wn-1 do
  dst[k2]:=(src[k2] shr 1) or (src[k2+1] shl 31);
if wn<=mw then dst[wn]:=0;
if wn+1<=mw then dst[wn+1]:=0;
VecNorm(dst);
end;

procedure VecShiftL2(var dst:TVec;const src:TVec);
var k2:longint;
begin
dst[-2]:=0; dst[-1]:=0;
for k2:=0 to wn-1 do
  dst[k2]:=(src[k2] shl 2) or (src[k2-1] shr 30);
if wn<=mw then dst[wn]:=0;
if wn+1<=mw then dst[wn+1]:=0;
VecNorm(dst);
end;

procedure PrepN;
var bits:longint;
var rem:longint;
var k2:longint;
begin
bits:=longint(n)+1;
wn:=(bits+31) shr 5;
rem:=bits and 31;
if rem=0 then lastMask:=$FFFFFFFF else lastMask:=(LongWord(1) shl rem)-1;
nWord:=(longint(n)-1) shr 5;
rem:=longint(n) and 31;
if rem=0 then nMask:=$FFFFFFFF else nMask:=(LongWord(1) shl rem)-1;
VecZero(ones);
for k2:=0 to wn-2 do ones[k2]:=$FFFFFFFF;
ones[wn-1]:=lastMask;
VecNorm(ones);
end;

function TimeMark(ch:char):Double;
var c:Int64;
var ms:Double;
begin
  QueryPerformanceCounter(c);
  if not hasLastCounter then
  begin
    ms:=0;
    hasLastCounter:=true;
  end
  else
    ms:=(c-lastCounter)*1000.0/perfFreq;
  lastCounter:=c;
  TimeMark:=ms;
  write(ms:8:3,#9,ch);
end;

procedure VecXorRange(var a:TVec;const b:TVec;l,r:longint);
var wl,wr,k2:longint;
var ml,mr:LongWord;
begin
if l<0 then l:=0;
if r>longint(n)-1 then r:=longint(n)-1;
if l>r then exit;
wl:=l shr 5; wr:=r shr 5;
ml:=LongWord($FFFFFFFF) shl (l and 31);
if (r and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r and 31)+1))-1;
if wl=wr then
  a[wl]:=a[wl] xor (b[wl] and (ml and mr))
else
  begin
  a[wl]:=a[wl] xor (b[wl] and ml);
  for k2:=wl+1 to wr-1 do a[k2]:=a[k2] xor b[k2];
  a[wr]:=a[wr] xor (b[wr] and mr);
  end;
end;

function DegMask(deg:longint):LongWord; inline;
var rem:longint;
begin
rem:=deg and 31;
if rem=31 then DegMask:=$FFFFFFFF
else DegMask:=(LongWord(1) shl (rem+1))-1;
end;

procedure VecCopyDeg(var a:TVec; const b:TVec; deg:longint); inline;
var k2,hiw:longint;
begin
a[-2]:=0; a[-1]:=0;
if deg<0 then begin a[0]:=0; exit; end;
hiw:=deg shr 5;
if hiw>mw then hiw:=mw;
for k2:=0 to hiw+1 do if k2<=mw then a[k2]:=b[k2];
if hiw+2<=mw then a[hiw+2]:=0;
end;

procedure BuildYFast(var dy_,dy:TVec; const sy_,sy_1,sy,sy1:TVec; deg:longint); inline;
var w,hiw:longint;
var mask:LongWord;
begin
hiw:=deg shr 5;
dy_[-2]:=0; dy_[-1]:=0; dy[-2]:=0; dy[-1]:=0;
for w:=0 to hiw do
  begin
  dy_[w]:=((sy_[w] shl 1) or (sy_[w-1] shr 31)) xor
          sy_[w] xor
          ((sy_[w] shr 1) or (sy_[w+1] shl 31)) xor
          sy_1[w];
  dy[w]:=((sy[w] shl 2) or (sy[w-1] shr 30)) xor
         ((sy[w] shl 1) or (sy[w-1] shr 31)) xor
         sy[w] xor
         ((sy1[w] shl 2) or (sy1[w-1] shr 30)) xor
         dy_[w] xor
         ((sy_1[w] shl 1) or (sy_1[w-1] shr 31)) xor
         $FFFFFFFF;
  end;
mask:=DegMask(deg);
dy_[hiw]:=dy_[hiw] and mask;
dy[hiw]:=dy[hiw] and mask;
if hiw+1<=mw then begin dy_[hiw+1]:=0; dy[hiw+1]:=0; end;
end;

procedure BuildFCFast(var nf,nc:TVec; const oldf,oldf1,oldc,oldc1:TVec; hi:longint); inline;
var w,hiw:longint;
var mask:LongWord;
begin
hiw:=hi shr 5;
nf[-2]:=0; nf[-1]:=0; nc[-2]:=0; nc[-1]:=0;
for w:=0 to hiw do
  begin
  nf[w]:=((oldc[w] shl 1) or (oldc[w-1] shr 31)) xor oldf1[w];
  nc[w]:=oldf[w] xor oldc[w] xor oldc1[w];
  end;
mask:=DegMask(hi);
nf[hiw]:=nf[hiw] and mask;
nc[hiw]:=nc[hiw] and mask;
if hiw+1<=mw then begin nf[hiw+1]:=0; nc[hiw+1]:=0; end;
end;

{$ifdef disp}
procedure SaveMat(s:ansistring);
begin
SetBB(bb);
FreshWin();
bp:=CreateBMP(n,n);
DrawBMP(_pmain,bp,0,0,n,n,0,0,n,n);
SaveBMP(bp,'png'+s+'/'+i2s(n)+'.png');
ReleaseBMP(bp);
end;
{$endif}

procedure MakeMat();
var y2,y_2,f2,c2:TVec;
var py,py1,py_,py_1,py2,py_2,pf,pf1,pf2,pc,pc1,pc2,pt:PVec;
var hiu:longint;
begin
TimeMark('m');
if (not o) or (longint(n)<k) then
  begin
  VecZero(y1); VecZero(y); VecZero(y_1); VecZero(y_);
  VecZero(f1); VecZero(f);
  VecZero(c1); VecZero(c);
  f[0]:=1;
  k:=0; o:=true; ho:=false;
  end;
py1:=@y1; py:=@y; py_1:=@y_1; py_:=@y_; py2:=@y2; py_2:=@y_2;
pf1:=@f1; pf:=@f; pf2:=@f2; pc1:=@c1; pc:=@c; pc2:=@c2;
for j:=k+1 to n do
  begin
  BuildYFast(py_2^,py2^,py_^,py_1^,py^,py1^,j-1);
  if (py2^[0] and 1)<>0 then py_2^[0]:=py_2^[0] or 1
  else py_2^[0]:=py_2^[0] and not(LongWord(1));
  py_2^[-2]:=1;
  if j=1 then
    begin
    pf2^[-2]:=0; pf2^[-1]:=0; pf2^[0]:=0; pf2^[1]:=0;
    pc2^[-2]:=0; pc2^[-1]:=0; pc2^[0]:=1; pc2^[1]:=0;
    end
  else
    begin
    hiu:=j div 2;
    BuildFCFast(pf2^,pc2^,pf^,pf1^,pc^,pc1^,hiu);
    end;
  pt:=py_1; py_1:=py_; py_:=py_2; py_2:=pt;
  pt:=py1; py1:=py; py:=py2; py2:=pt;
  pt:=pf1; pf1:=pf; pf:=pf2; pf2:=pt;
  pt:=pc1; pc1:=pc; pc:=pc2; pc2:=pt;
  if j=longint(n div 2) then
    begin
    VecCopyDeg(hf,pf^,j div 2);
    VecCopyDeg(hc,pc^,j div 2);
    VecCopyDeg(hf1,pf1^,j div 2);
    VecCopyDeg(hc1,pc1^,j div 2);
    MaskDeg(hf,j div 2);
    MaskDeg(hc,j div 2);
    MaskDeg(hf1,j div 2);
    MaskDeg(hc1,j div 2);
    hk:=j;
    ho:=true;
    end;
  end;
VecCopyDeg(y1,py1^,longint(n)); VecCopyDeg(y,py^,longint(n));
VecCopyDeg(y_1,py_1^,longint(n)); VecCopyDeg(y_,py_^,longint(n));
VecCopyDeg(f1,pf1^,longint(n div 2)); VecCopyDeg(f,pf^,longint(n div 2));
VecCopyDeg(c1,pc1^,longint(n div 2)); VecCopyDeg(c,pc^,longint(n div 2));
k:=n;
end;

procedure EnsureAB(nn:longword);
var jj,hiu:longint;
var tf,tc:TVec;
begin
if (not ho) or (longint(nn)<hk) then
  begin
  VecZero(hf); VecZero(hc); VecZero(hf1); VecZero(hc1);
  hf[0]:=1;
  hk:=0; ho:=true;
  end;
for jj:=hk+1 to nn do
  begin
  if jj=1 then
    begin
    tf[-2]:=0; tf[-1]:=0; tf[0]:=0; tf[1]:=0;
    tc[-2]:=0; tc[-1]:=0; tc[0]:=1; tc[1]:=0;
    end
  else
    begin
    hiu:=jj div 2;
    BuildFCFast(tf,tc,hf,hf1,hc,hc1,hiu);
    end;
  VecCopyDeg(hf1,hf,jj div 2);
  VecCopyDeg(hc1,hc,jj div 2);
  VecCopyDeg(hf,tf,jj div 2);
  VecCopyDeg(hc,tc,jj div 2);
  end;
hk:=nn;
end;

function HighBit32(x:LongWord):longint;
var k2:longint;
begin
for k2:=31 downto 0 do if (x and (LongWord(1) shl k2))<>0 then begin HighBit32:=k2; exit; end;
HighBit32:=-1;
end;

function TopBit(const v:TVec):longint;
var w,h:longint;
begin
for w:=wn-1 downto 0 do
  if v[w]<>0 then
    begin
    h:=HighBit32(v[w]);
    TopBit:=(w shl 5)+h;
    exit;
    end;
TopBit:=-1;
end;

function TopBitLE(const v:TVec;hi:longint):longint;
var w,h:longint;
var x:LongWord;
begin
if hi<0 then begin TopBitLE:=-1; exit; end;
if hi>longint(n) then hi:=longint(n);
w:=hi shr 5;
if (hi and 31)=31 then x:=v[w]
else x:=v[w] and ((LongWord(1) shl ((hi and 31)+1))-1);
while w>=0 do
  begin
  if x<>0 then
    begin
    h:=HighBit32(x);
    TopBitLE:=(w shl 5)+h;
    exit;
    end;
  dec(w);
  if w>=0 then x:=v[w];
  end;
TopBitLE:=-1;
end;


function LowBit32(x:LongWord):longint;
var k2:longint;
begin
for k2:=0 to 31 do if (x and (LongWord(1) shl k2))<>0 then begin LowBit32:=k2; exit; end;
LowBit32:=-1;
end;

function FirstBitRange(const v:TVec;l,r:longint):longint;
var wl,wr,w:longint;
var x,ml,mr:LongWord;
begin
if l<0 then l:=0;
if r>longint(n)-1 then r:=longint(n)-1;
if l>r then begin FirstBitRange:=-1; exit; end;
wl:=l shr 5; wr:=r shr 5;
ml:=LongWord($FFFFFFFF) shl (l and 31);
if (r and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r and 31)+1))-1;
for w:=wl to wr do
  begin
  x:=v[w];
  if w=wl then x:=x and ml;
  if w=wr then x:=x and mr;
  if x<>0 then begin FirstBitRange:=(w shl 5)+LowBit32(x); exit; end;
  end;
FirstBitRange:=-1;
end;

function LastBitRange(const v:TVec;l,r:longint):longint;
var wl,wr,w,h:longint;
var x,ml,mr:LongWord;
begin
if l<0 then l:=0;
if r>longint(n)-1 then r:=longint(n)-1;
if l>r then begin LastBitRange:=-1; exit; end;
wl:=l shr 5; wr:=r shr 5;
ml:=LongWord($FFFFFFFF) shl (l and 31);
if (r and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r and 31)+1))-1;
for w:=wr downto wl do
  begin
  x:=v[w];
  if w=wl then x:=x and ml;
  if w=wr then x:=x and mr;
  if x<>0 then
    begin
    h:=HighBit32(x);
    LastBitRange:=(w shl 5)+h;
    exit;
    end;
  end;
LastBitRange:=-1;
end;

procedure VecStepRange(var dst:TVec;const src:TVec;l,r,hi:longint);
var l2,r2,wl,wr,w:longint;
var ml,mr:LongWord;
begin
if l<0 then l:=0;
if r>hi then r:=hi;
if l>r then begin VecZero(dst); exit; end;
l2:=l-1; if l2<0 then l2:=0;
r2:=r+1; if r2>hi then r2:=hi;
wl:=l2 shr 5; wr:=r2 shr 5;
if wl-1>=-2 then dst[wl-1]:=0;
if wr+1<=mw then dst[wr+1]:=0;
for w:=wl to wr do
  dst[w]:=(((src[w] shl 1) or (src[w-1] shr 31)) xor ((src[w] shr 1) or (src[w+1] shl 31)));
ml:=LongWord($FFFFFFFF) shl (l2 and 31);
if (r2 and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r2 and 31)+1))-1;
if wl=wr then
  dst[wl]:=dst[wl] and (ml and mr)
else
  begin
  dst[wl]:=dst[wl] and ml;
  dst[wr]:=dst[wr] and mr;
  end;
VecNorm(dst);
end;

procedure ApplyPoly(const va,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var d,j2,l,r,l2,r2:longint;
begin
VecZero(cur0); VecZero(cur1); VecZero(vdst);
VecCopy(cur0,vsrc);
MaskDeg(cur0,hi);
d:=TopBitLE(va,degmax);
if d<0 then exit;
l:=FirstBitRange(cur0,0,hi);
if l<0 then exit;
r:=LastBitRange(cur0,l,hi);
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  if GetBit(va,j2)<>0 then VecXorRange(vdst,pcur^,l,r);
  if j2>=d then break;
  l2:=l-1; if l2<0 then l2:=0;
  r2:=r+1; if r2>hi then r2:=hi;
  VecStepRange(pnxt^,pcur^,l,r,hi);
  l:=FirstBitRange(pnxt^,l2,r2);
  if l<0 then break;
  r:=LastBitRange(pnxt^,l,r2);
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
VecNorm(vdst);
end;


procedure VecXorShift(var a:TVec;const b:TVec;sh:longint);
var ws,bs:longint;
var x0,x1:LongWord;
var k2:longint;
begin
if sh<0 then exit;
ws:=sh shr 5;
bs:=sh and 31;
if bs=0 then
  begin
  for k2:=wn-1 downto ws do a[k2]:=a[k2] xor b[k2-ws];
  end
else
  begin
  for k2:=wn-1 downto ws do
    begin
    x0:=b[k2-ws] shl bs;
    x1:=0;
    if k2-ws-1>=0 then x1:=b[k2-ws-1] shr (32-bs);
    a[k2]:=a[k2] xor (x0 or x1);
    end;
  end;
VecNorm(a);
end;

procedure VecXorShiftRange(var a:TVec;const b:TVec;sh,r:longint);
var ws,bs,wl,wr,k2:longint;
var x0,x1,ml,mr,msk:LongWord;
begin
if sh<0 then exit;
if r<0 then exit;
if sh>longint(n) then exit;
if r>longint(n)-sh then r:=longint(n)-sh;
ws:=sh shr 5;
bs:=sh and 31;
wl:=sh shr 5;
wr:=(sh+r) shr 5;
ml:=LongWord($FFFFFFFF) shl (sh and 31);
if ((sh+r) and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl (((sh+r) and 31)+1))-1;
for k2:=wl to wr do
  begin
  if bs=0 then
    begin
    x0:=b[k2-ws];
    x1:=0;
    end
  else
    begin
    x0:=b[k2-ws] shl bs;
    x1:=0;
    if k2-ws-1>=0 then x1:=b[k2-ws-1] shr (32-bs);
    end;
  msk:=$FFFFFFFF;
  if k2=wl then msk:=msk and ml;
  if k2=wr then msk:=msk and mr;
  a[k2]:=a[k2] xor ((x0 or x1) and msk);
  end;
VecNorm(a);
end;

function gcd(const vf,vg:TVec; var vd,vr:TVec):longint;
var f0a,g0a,vxa,vya:TVec;
var f0,g0,vx,vy,vt:PVec;
var kf,kg,kvx,kvy,shift,p,top,lim:longint;
begin
f0:=@f0a; g0:=@g0a; vx:=@vxa; vy:=@vya;
VecCopy(f0^,vf); VecCopy(g0^,vg);
kf:=TopBit(f0^);
kg:=TopBit(g0^);
kvx:=-1;
kvy:=0;
VecZero(vx^); VecZero(vy^); SetBit(vy^,0,1);
while true do
  begin
  if kf<kg then begin vt:=f0; f0:=g0; g0:=vt; vt:=vx; vx:=vy; vy:=vt; p:=kf; kf:=kg; kg:=p; p:=kvx; kvx:=kvy; kvy:=p; end;
  if kg<0 then begin VecCopy(vd,f0^); VecCopy(vr,vx^); gcd:=kf; exit; end;
  while kf>=kg do
    begin
    shift:=kf-kg;
    VecXorShift(f0^,g0^,shift);
    kf:=TopBitLE(f0^,kf-1);
    if kvy>=0 then
      begin
      top:=kvx;
      if kvy+shift>longint(n) then top:=longint(n)
      else if kvy+shift>top then top:=kvy+shift;
      lim:=kvy;
      if lim>longint(n)-shift then lim:=longint(n)-shift;
      VecXorShiftRange(vx^,vy^,shift,lim);
      kvx:=TopBitLE(vx^,top);
      end;
    end;
  end;
end;

procedure RecoverBezoutU(const va,vb,vg,vv:TVec; var vu:TVec; hi:longint); forward;

function GcdU(const va,vb:TVec; var vg,vu,vv:TVec; hi:longint):longint;
var r0a,r1a,v0a,v1a:TVec;
var r0,r1,v0,v1,tt:PVec;
var kr0,kr1,kv0,kv1,shift,p,top,lim:longint;
begin
r0:=@r0a; r1:=@r1a; v0:=@v0a; v1:=@v1a;
VecCopy(r0^,va); MaskDeg(r0^,hi);
VecCopy(r1^,vb); MaskDeg(r1^,hi);
VecZero(v0^); VecZero(v1^);
SetBit(v1^,0,1);
kr0:=TopBitLE(r0^,hi);
kr1:=TopBitLE(r1^,hi);
kv0:=-1; kv1:=0;
while true do
  begin
  if kr0<kr1 then
    begin
    tt:=r0; r0:=r1; r1:=tt;
    tt:=v0; v0:=v1; v1:=tt;
    p:=kr0; kr0:=kr1; kr1:=p;
    p:=kv0; kv0:=kv1; kv1:=p;
    end;
  if kr1<0 then
    begin
    VecCopy(vg,r0^); MaskDeg(vg,hi);
    VecCopy(vv,v0^); MaskDeg(vv,hi);
    RecoverBezoutU(va,vb,vg,vv,vu,hi);
    GcdU:=kr0;
    exit;
    end;
  while kr0>=kr1 do
    begin
    shift:=kr0-kr1;
    VecXorShiftRange(r0^,r1^,shift,kr1);
    kr0:=TopBitLE(r0^,kr0-1);
    if kv1>=0 then
      begin
      top:=kv0;
      if kv1+shift>top then top:=kv1+shift;
      if top>hi then top:=hi;
      lim:=kv1;
      if lim>hi-shift then lim:=hi-shift;
      VecXorShiftRange(v0^,v1^,shift,lim);
      kv0:=TopBitLE(v0^,top);
      end;
    end;
  end;
end;

procedure VecStepJ(var dst:TVec; const src:TVec; hi:longint); inline;
var k2:longint;
var left,cur,right:LongWord;
begin
if hi<=0 then begin VecZero(dst); exit; end;
dst[-2]:=0; dst[-1]:=0;
left:=src[-1]; cur:=src[0];
for k2:=0 to wn-1 do
  begin
  right:=src[k2+1];
  dst[k2]:=(cur shl 2) xor (left shr 30) xor
           (cur shr 2) xor (right shl 30) xor
           (cur shl 1) xor (left shr 31) xor
           (cur shr 1) xor (right shl 31);
  left:=cur; cur:=right;
  end;
if (src[0] and 1)<>0 then dst[0]:=dst[0] xor 1;
if (hi>0) and (((src[hi shr 5] shr (hi and 31)) and 1)<>0) then
  dst[hi shr 5]:=dst[hi shr 5] xor (LongWord(1) shl (hi and 31));
if wn<=mw then dst[wn]:=0;
if wn+1<=mw then dst[wn+1]:=0;
dst[nWord]:=dst[nWord] and nMask;
if nWord+1<=mw then dst[nWord+1]:=0;
end;

procedure VecStepJHi(var dst:TVec; const src:TVec; hi:longint); inline;
var k2,hiw,rem:longint;
var left,cur,right,mask:LongWord;
begin
if hi<=0 then begin VecZero(dst); exit; end;
hiw:=hi shr 5;
dst[-2]:=0; dst[-1]:=0;
left:=src[-1]; cur:=src[0];
for k2:=0 to hiw do
  begin
  right:=src[k2+1];
  dst[k2]:=(cur shl 2) xor (left shr 30) xor
           (cur shr 2) xor (right shl 30) xor
           (cur shl 1) xor (left shr 31) xor
           (cur shr 1) xor (right shl 31);
  left:=cur; cur:=right;
  end;
if (src[0] and 1)<>0 then dst[0]:=dst[0] xor 1;
if (((src[hi shr 5] shr (hi and 31)) and 1)<>0) then
  dst[hi shr 5]:=dst[hi shr 5] xor (LongWord(1) shl (hi and 31));
rem:=hi and 31;
if rem=31 then mask:=$FFFFFFFF else mask:=(LongWord(1) shl (rem+1))-1;
dst[hiw]:=dst[hiw] and mask;
if hiw+1<=mw then dst[hiw+1]:=0;
if hiw+2<=mw then dst[hiw+2]:=0;
end;

procedure VecStepJXorTo(var acc,dst:TVec; const src:TVec; hi,mode:longint); inline;
var k2:longint;
var left,cur,right,h:LongWord;
begin
if hi<=0 then begin VecZero(dst); exit; end;
dst[-2]:=0; dst[-1]:=0;
left:=src[-1]; cur:=src[0];
for k2:=0 to wn-1 do
  begin
  right:=src[k2+1];
  h:=(cur shl 1) xor (left shr 31) xor (cur shr 1) xor (right shl 31);
  case mode of
    1: acc[k2]:=acc[k2] xor cur;
    2: acc[k2]:=acc[k2] xor h;
    3: acc[k2]:=acc[k2] xor cur xor h;
    end;
  dst[k2]:=(cur shl 2) xor (left shr 30) xor
           (cur shr 2) xor (right shl 30) xor h;
  left:=cur; cur:=right;
  end;
if (src[0] and 1)<>0 then dst[0]:=dst[0] xor 1;
if (hi>0) and (((src[hi shr 5] shr (hi and 31)) and 1)<>0) then
  dst[hi shr 5]:=dst[hi shr 5] xor (LongWord(1) shl (hi and 31));
if wn<=mw then dst[wn]:=0;
if wn+1<=mw then dst[wn+1]:=0;
dst[nWord]:=dst[nWord] and nMask;
if nWord+1<=mw then dst[nWord+1]:=0;
end;

procedure VecH(var dst:TVec; const src:TVec; hi:longint);
var k2:longint;
var left,cur,right:LongWord;
begin
dst[-2]:=0; dst[-1]:=0;
left:=src[-1]; cur:=src[0];
for k2:=0 to wn-1 do
  begin
  right:=src[k2+1];
  dst[k2]:=(cur shl 1) xor (left shr 31) xor (cur shr 1) xor (right shl 31);
  left:=cur; cur:=right;
  end;
if wn<=mw then dst[wn]:=0;
if wn+1<=mw then dst[wn+1]:=0;
MaskDeg(dst,hi);
end;

procedure ApplyPolyU(const va,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var d,j2:longint;
begin
VecZero(cur0); VecZero(cur1); VecZero(vdst);
VecCopy(cur0,vsrc);
MaskDeg(cur0,hi);
d:=TopBitLE(va,degmax);
if d<0 then exit;
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  if GetBit(va,j2)<>0 then VecXorRaw(vdst,pcur^);
  if j2>=d then break;
  VecStepJ(pnxt^,pcur^,hi);
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
MaskDeg(vdst,hi);
end;

procedure ApplyPolyU0(const va:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var d,j2,k2,curHi,nextHi,curWord:longint;
begin
VecZero(cur0); VecZero(cur1); VecZero(vdst);
d:=TopBitLE(va,degmax);
if d<0 then exit;
cur0[0]:=1;
pcur:=@cur0;
pnxt:=@cur1;
curHi:=0;
for j2:=0 to d do
  begin
  if GetBit(va,j2)<>0 then
    begin
    curWord:=curHi shr 5;
    for k2:=0 to curWord do vdst[k2]:=vdst[k2] xor pcur^[k2];
    end;
  if j2>=d then break;
  nextHi:=curHi+2; if nextHi>hi then nextHi:=hi;
  VecStepJHi(pnxt^,pcur^,nextHi);
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  curHi:=nextHi;
  end;
MaskDeg(vdst,hi);
end;

function CLMul8(a,b:LongWord):LongWord; inline;
begin
CLMul8:=mul8[(a shl 8) or b];
end;

function CLMul16(a,b:LongWord):LongWord; inline;
var z0,z1,z2:LongWord;
begin
z0:=CLMul8(a and $FF,b and $FF);
z2:=CLMul8(a shr 8,b shr 8);
z1:=CLMul8((a xor (a shr 8)) and $FF,(b xor (b shr 8)) and $FF);
CLMul16:=z0 xor ((z0 xor z1 xor z2) shl 8) xor (z2 shl 16);
end;

function CLMul32(a,b:LongWord):QWord; inline;
var z0,z1,z2:LongWord;
begin
z0:=CLMul16(a and $FFFF,b and $FFFF);
z2:=CLMul16(a shr 16,b shr 16);
z1:=CLMul16((a xor (a shr 16)) and $FFFF,(b xor (b shr 16)) and $FFFF);
CLMul32:=QWord(z0) xor (QWord(z0 xor z1 xor z2) shl 16) xor (QWord(z2) shl 32);
end;

procedure InitMul8;
var a0,b0,k0,r0:longint;
begin
for a0:=0 to 255 do for b0:=0 to 255 do
  begin
  r0:=0;
  for k0:=0 to 7 do if ((b0 shr k0) and 1)<>0 then r0:=r0 xor (a0 shl k0);
  mul8[(a0 shl 8) or b0]:=r0;
  end;
end;

procedure InitUKernel8;
var a0,j0:longint;
var p0,k0:QWord;
begin
for a0:=0 to 255 do
  begin
  p0:=QWord(1) shl 14;
  k0:=0;
  for j0:=0 to 7 do
    begin
    if ((a0 shr j0) and 1)<>0 then k0:=k0 xor p0;
    if j0<7 then p0:=(p0 shl 2) xor (p0 shl 1) xor (p0 shr 1) xor (p0 shr 2);
    end;
  uKernel8[a0]:=LongWord(k0);
  end;
end;

procedure KarRecW(const a:TWordArray; ao:longint; const b:TWordArray; bo:longint;
                  var r:TWordArray; ro,len:longint; var work:TWordArray; wo:longint);
const cut=4;
var i0,j0,h,ax0,bx0,z10,save0,rec0:longint;
var p0:QWord;
var s2:LongWord;
begin
if len<=cut then
  begin
  for i0:=0 to len-1 do if a[ao+i0]<>0 then
    for j0:=0 to len-1 do if b[bo+j0]<>0 then
      begin
      p0:=CLMul32(a[ao+i0],b[bo+j0]);
      r[ro+i0+j0]:=r[ro+i0+j0] xor LongWord(p0);
      r[ro+i0+j0+1]:=r[ro+i0+j0+1] xor LongWord(p0 shr 32);
      end;
  exit;
  end;
h:=len shr 1;
KarRecW(a,ao,b,bo,r,ro,h,work,wo);
KarRecW(a,ao+h,b,bo+h,r,ro+(h shl 1),h,work,wo);
ax0:=wo; bx0:=wo+h; z10:=wo+(h shl 1); save0:=wo+(h shl 2); rec0:=save0+h;
for i0:=0 to h-1 do
  begin
  work[ax0+i0]:=a[ao+i0] xor a[ao+h+i0];
  work[bx0+i0]:=b[bo+i0] xor b[bo+h+i0];
  end;
for i0:=0 to (h shl 1)-1 do work[z10+i0]:=0;
KarRecW(work,ax0,work,bx0,work,z10,h,work,rec0);
for i0:=0 to h-1 do work[save0+i0]:=r[ro+(h shl 1)+i0];
for i0:=(h shl 1)-1 downto 0 do r[ro+h+i0]:=r[ro+h+i0] xor r[ro+i0];
for i0:=0 to (h shl 1)-1 do
  begin
  if i0<h then s2:=work[save0+i0] else s2:=r[ro+(h shl 1)+i0];
  r[ro+h+i0]:=r[ro+h+i0] xor s2 xor work[z10+i0];
  end;
end;

procedure KarMulFastW(const a,b:TWordArray; var r:TWordArray; len:longint);
var work:TWordArray;
var i0:longint;
begin
SetLength(r,len shl 1);
for i0:=0 to High(r) do r[i0]:=0;
SetLength(work,len*6);
KarRecW(a,0,b,0,r,0,len,work,0);
end;

procedure KarRecPairW(const a:TWordArray; ao:longint;
                      const b:TWordArray; bo:longint;
                      const c:TWordArray; co:longint;
                      var r:TWordArray; ro:longint;
                      var s:TWordArray; so,lenWords,alen,blen,clen:longint;
                      var work:TWordArray; wo:longint);
const cut=4;
var i0,j0,lenBits,hWords,gWords,ax0,bx0,cx0,zr0,zs0,saver0,saves0,rec0:longint;
var a0len,a1len,b0len,b1len,c0len,c1len,axlen,bxlen,cxlen,maxbc:longint;
var aWords,bWords,cWords:longint;
var p0:QWord;
var tr,ts:LongWord;
begin
lenBits:=lenWords shl 5;
if alen>lenBits then alen:=lenBits;
if blen>lenBits then blen:=lenBits;
if clen>lenBits then clen:=lenBits;
if (alen<=0) or ((blen<=0) and (clen<=0)) then exit;
if lenWords<=cut then
  begin
  aWords:=(alen+31) shr 5;
  bWords:=(blen+31) shr 5;
  cWords:=(clen+31) shr 5;
  maxbc:=bWords; if cWords>maxbc then maxbc:=cWords;
  for i0:=0 to aWords-1 do if a[ao+i0]<>0 then
    for j0:=0 to maxbc-1 do
      begin
      if (j0<bWords) and (b[bo+j0]<>0) then
        begin
        p0:=CLMul32(a[ao+i0],b[bo+j0]);
        r[ro+i0+j0]:=r[ro+i0+j0] xor LongWord(p0);
        r[ro+i0+j0+1]:=r[ro+i0+j0+1] xor LongWord(p0 shr 32);
        end;
      if (j0<cWords) and (c[co+j0]<>0) then
        begin
        p0:=CLMul32(a[ao+i0],c[co+j0]);
        s[so+i0+j0]:=s[so+i0+j0] xor LongWord(p0);
        s[so+i0+j0+1]:=s[so+i0+j0+1] xor LongWord(p0 shr 32);
        end;
      end;
  exit;
  end;
hWords:=(lenWords+1) shr 1;
gWords:=lenWords-hWords;
if alen>(hWords shl 5) then begin a0len:=hWords shl 5; a1len:=alen-(hWords shl 5); end
else begin a0len:=alen; a1len:=0; end;
if blen>(hWords shl 5) then begin b0len:=hWords shl 5; b1len:=blen-(hWords shl 5); end
else begin b0len:=blen; b1len:=0; end;
if clen>(hWords shl 5) then begin c0len:=hWords shl 5; c1len:=clen-(hWords shl 5); end
else begin c0len:=clen; c1len:=0; end;
if (a1len=0) and (b1len=0) and (c1len=0) then
  begin
  KarRecPairW(a,ao,b,bo,c,co,r,ro,s,so,hWords,a0len,b0len,c0len,work,wo);
  exit;
  end;
KarRecPairW(a,ao,b,bo,c,co,r,ro,s,so,hWords,a0len,b0len,c0len,work,wo);
KarRecPairW(a,ao+hWords,b,bo+hWords,c,co+hWords,
            r,ro+(hWords shl 1),s,so+(hWords shl 1),gWords,
            a1len,b1len,c1len,work,wo);
ax0:=wo; bx0:=wo+hWords; cx0:=wo+(hWords shl 1);
zr0:=wo+hWords*3; zs0:=wo+hWords*5;
saver0:=wo+hWords*7; saves0:=wo+hWords*8; rec0:=wo+hWords*9;
for i0:=0 to hWords-1 do
  begin
  work[ax0+i0]:=a[ao+i0];
  work[bx0+i0]:=b[bo+i0];
  work[cx0+i0]:=c[co+i0];
  if i0<gWords then
    begin
    work[ax0+i0]:=work[ax0+i0] xor a[ao+hWords+i0];
    work[bx0+i0]:=work[bx0+i0] xor b[bo+hWords+i0];
    work[cx0+i0]:=work[cx0+i0] xor c[co+hWords+i0];
    end;
  end;
for i0:=0 to (hWords shl 1)-1 do
  begin
  work[zr0+i0]:=0;
  work[zs0+i0]:=0;
  end;
axlen:=a0len; if a1len>axlen then axlen:=a1len;
bxlen:=b0len; if b1len>bxlen then bxlen:=b1len;
cxlen:=c0len; if c1len>cxlen then cxlen:=c1len;
KarRecPairW(work,ax0,work,bx0,work,cx0,
            work,zr0,work,zs0,hWords,axlen,bxlen,cxlen,work,rec0);
for i0:=0 to hWords-1 do
  begin
  if i0<(gWords shl 1) then
    begin
    work[saver0+i0]:=r[ro+(hWords shl 1)+i0];
    work[saves0+i0]:=s[so+(hWords shl 1)+i0];
    end
  else
    begin
    work[saver0+i0]:=0;
    work[saves0+i0]:=0;
    end;
  end;
for i0:=(hWords shl 1)-1 downto 0 do
  begin
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor r[ro+i0];
  s[so+hWords+i0]:=s[so+hWords+i0] xor s[so+i0];
  end;
for i0:=0 to (hWords shl 1)-1 do
  begin
  if i0<hWords then
    begin
    tr:=work[saver0+i0];
    ts:=work[saves0+i0];
    end
  else if i0<(gWords shl 1) then
    begin
    tr:=r[ro+(hWords shl 1)+i0];
    ts:=s[so+(hWords shl 1)+i0];
    end
  else
    begin
    tr:=0;
    ts:=0;
    end;
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor tr xor work[zr0+i0];
  s[so+hWords+i0]:=s[so+hWords+i0] xor ts xor work[zs0+i0];
  end;
end;

procedure KarMulPairFastW(const a,b,c:TWordArray; var r,s:TWordArray;
                          lenWords,alen,blen,clen:longint);
var work:TWordArray;
var i0:longint;
begin
SetLength(r,lenWords shl 1);
SetLength(s,lenWords shl 1);
for i0:=0 to High(r) do
  begin
  r[i0]:=0;
  s[i0]:=0;
  end;
SetLength(work,lenWords*10);
KarRecPairW(a,0,b,0,c,0,r,0,s,0,lenWords,alen,blen,clen,work,0);
end;

{ vg=vu*va+vv*vb, hence vu=(vg+vv*vb)/va. }
{ A and B use the same 32-coefficient reciprocal-block exact division. }
procedure RecoverBezoutU(const va,vb,vg,vv:TVec; var vu:TVec; hi:longint);
var aa,bb,empty,prod,dummy:TWordArray;
var num:TVec;
var lenWords,da,db,dv,top,dq,count,k,s,p,lastWord,sWord:longint;
var drev,iv,rword,rrev,qrev,qblock,mask0:LongWord;
var z0:QWord;

function BlockMask(bits:longint):LongWord; inline;
begin
if bits>=32 then BlockMask:=$FFFFFFFF
else BlockMask:=(LongWord(1) shl bits)-1;
end;

function ReverseWord(x0:LongWord):LongWord; inline;
begin
x0:=((x0 and $55555555) shl 1) or ((x0 shr 1) and $55555555);
x0:=((x0 and $33333333) shl 2) or ((x0 shr 2) and $33333333);
x0:=((x0 and $0F0F0F0F) shl 4) or ((x0 shr 4) and $0F0F0F0F);
x0:=((x0 and $00FF00FF) shl 8) or ((x0 shr 8) and $00FF00FF);
ReverseWord:=(x0 shl 16) or (x0 shr 16);
end;

function ReadVec32At(const src:TVec; bit0:longint):LongWord; inline;
var w0,b0:longint;
begin
if bit0>=0 then
  begin
  w0:=bit0 shr 5; b0:=bit0 and 31;
  ReadVec32At:=src[w0] shr b0;
  if b0<>0 then ReadVec32At:=ReadVec32At xor (src[w0+1] shl (32-b0));
  end
else if bit0<=-32 then ReadVec32At:=0
else ReadVec32At:=src[0] shl (-bit0);
end;
begin
da:=TopBitLE(va,hi);
db:=TopBitLE(vb,hi);
dv:=TopBitLE(vv,hi);
VecZero(vu);
if da<0 then exit;
lenWords:=(hi+32) shr 5;
SetLength(aa,lenWords); SetLength(bb,lenWords); SetLength(empty,lenWords);
for p:=0 to lenWords-1 do begin aa[p]:=vv[p]; bb[p]:=vb[p]; end;
KarMulPairFastW(aa,bb,empty,prod,dummy,lenWords,dv+1,db+1,0);
VecZero(num);
for p:=0 to High(prod) do num[p]:=prod[p];
lastWord:=hi shr 5;
for p:=0 to lastWord do num[p]:=num[p] xor vg[p];
top:=TopBitLE(num,(hi shl 1)+1);
drev:=ReverseWord(ReadVec32At(va,da-31));
iv:=1;
for k:=1 to 31 do
  begin
  mask0:=LongWord(1) shl k;
  if (LongWord(CLMul32(drev,iv)) and mask0)<>0 then iv:=iv or mask0;
  end;
dq:=top-da;
while dq>=0 do
  begin
  count:=dq+1; k:=count and 31; if k=0 then k:=32; s:=count-k;
  mask0:=BlockMask(k);
  rword:=ReadVec32At(num,da+s) and mask0;
  rrev:=ReverseWord(rword) shr (32-k);
  qrev:=LongWord(CLMul32(rrev,iv)) and mask0;
  qblock:=ReverseWord(qrev) shr (32-k);
  sWord:=s shr 5;
  vu[sWord]:=qblock;
  for p:=0 to (da shr 5) do
    begin
    z0:=CLMul32(va[p],qblock);
    num[sWord+p]:=num[sWord+p] xor LongWord(z0);
    num[sWord+p+1]:=num[sWord+p+1] xor LongWord(z0 shr 32);
    end;
  dq:=s-1;
  end;
MaskDeg(vu,hi);
end;

function LowMask32(bits:longint):LongWord; inline;
begin
if bits<=0 then LowMask32:=0
else if bits>=32 then LowMask32:=$FFFFFFFF
else LowMask32:=(LongWord(1) shl bits)-1;
end;

function Reverse32(x:LongWord):LongWord; inline;
begin
x:=((x and $55555555) shl 1) or ((x shr 1) and $55555555);
x:=((x and $33333333) shl 2) or ((x shr 2) and $33333333);
x:=((x and $0F0F0F0F) shl 4) or ((x shr 4) and $0F0F0F0F);
x:=((x and $00FF00FF) shl 8) or ((x shr 8) and $00FF00FF);
Reverse32:=(x shl 16) or (x shr 16);
end;

procedure ClearDynBits(var a:TWordArray; bit0,len:longint);
var w0,w1,b0,b1,k0:longint;
var mask0:LongWord;
begin
if len<=0 then exit;
w0:=bit0 shr 5; b0:=bit0 and 31;
w1:=(bit0+len-1) shr 5; b1:=(bit0+len-1) and 31;
if w0=w1 then
  begin
  mask0:=LowMask32(len) shl b0;
  a[w0]:=a[w0] and not mask0;
  exit;
  end;
a[w0]:=a[w0] and LowMask32(b0);
for k0:=w0+1 to w1-1 do a[k0]:=0;
a[w1]:=a[w1] and not LowMask32(b1+1);
end;

function ReadDyn32(const a:TWordArray; bit0:longint):LongWord; inline;
var w0,b0:longint;
var r0:LongWord;
begin
w0:=bit0 shr 5; b0:=bit0 and 31;
if (w0<0) or (w0>High(a)) then begin ReadDyn32:=0; exit; end;
r0:=a[w0] shr b0;
if (b0<>0) and (w0<High(a)) then r0:=r0 xor (a[w0+1] shl (32-b0));
ReadDyn32:=r0;
end;

function ReadDyn32Any(const a:TWordArray; bit0:longint):LongWord; inline;
begin
if bit0>=0 then ReadDyn32Any:=ReadDyn32(a,bit0)
else if bit0<=-32 then ReadDyn32Any:=0
else ReadDyn32Any:=a[0] shl (-bit0);
end;

function ReadDyn32Reverse(const a:TWordArray; endBit:longint):LongWord; inline;
begin
ReadDyn32Reverse:=Reverse32(ReadDyn32Any(a,endBit-31));
end;

procedure XorDyn32(var a:TWordArray; bit0:longint; v0:LongWord); inline;
var w0,b0:longint;
begin
if v0=0 then exit;
w0:=bit0 shr 5; b0:=bit0 and 31;
if (w0<0) or (w0>High(a)) then exit;
a[w0]:=a[w0] xor (v0 shl b0);
if (b0<>0) and (w0<High(a)) then a[w0+1]:=a[w0+1] xor (v0 shr (32-b0));
end;

procedure XorDynBits(var dst:TWordArray; dstBit:longint;
                     const src:TWordArray; srcBit,len:longint);
var take:longint;
var q0:LongWord;
begin
while len>0 do
  begin
  if len>32 then take:=32 else take:=len;
  q0:=ReadDyn32(src,srcBit) and LowMask32(take);
  XorDyn32(dst,dstBit,q0);
  inc(srcBit,take); inc(dstBit,take); dec(len,take);
  end;
end;

function CoeffByte(const coeff:TVec; first,degmax:longint):LongWord; inline;
var keep:longint;
begin
if first>degmax then begin CoeffByte:=0; exit; end;
keep:=degmax-first+1;
if keep>8 then keep:=8;
CoeffByte:=((coeff[first shr 5] shr (first and 31)) and $FF) and LowMask32(keep);
end;

procedure BuildUKernelRec(const coeff:TVec; first,count,degmax:longint;
                          var dst:TWordArray; dstBit:longint;
                          var work:TWordArray; workWord:longint);
var h,childBits,childWords,workBit:longint;
begin
ClearDynBits(dst,dstBit,(count shl 2)-3);
if count=8 then
  begin
  XorDyn32(dst,dstBit,uKernel8[CoeffByte(coeff,first,degmax)]);
  exit;
  end;
h:=count shr 1;
childBits:=(h shl 2)-3;
childWords:=(childBits+31) shr 5;
BuildUKernelRec(coeff,first,h,degmax,dst,dstBit+(h shl 1),work,workWord);
workBit:=workWord shl 5;
BuildUKernelRec(coeff,first+h,h,degmax,work,workBit,work,workWord+childWords);
XorDynBits(dst,dstBit,work,workBit,childBits);
XorDynBits(dst,dstBit+h,work,workBit,childBits);
XorDynBits(dst,dstBit+h*3,work,workBit,childBits);
XorDynBits(dst,dstBit+(h shl 2),work,workBit,childBits);
end;

procedure BuildUKernelFastW(const coeff:TVec; degmax:longint;
                            var r:TWordArray; var center:longint);
var count,bits,k0:longint;
var work:TWordArray;
begin
count:=8;
while count<=degmax do count:=count shl 1;
bits:=(count shl 2)-3;
SetLength(r,(bits+31) shr 5);
for k0:=0 to High(r) do r[k0]:=0;
SetLength(work,count div 8+64);
for k0:=0 to High(work) do work[k0]:=0;
BuildUKernelRec(coeff,0,count,degmax,r,0,work,0);
center:=(count shl 1)-2;
end;

procedure BuildUComboRecW(const va,vb:TVec; first,count,degmax,mode:longint;
                          var dst:TWordArray; dstBit:longint;
                          var work:TWordArray; workWord:longint);
var h,childBits,childWords,workBit:longint;
var aa,bb:LongWord;
begin
ClearDynBits(dst,dstBit,(count shl 2)-1);
if count=8 then
  begin
  aa:=uKernel8[CoeffByte(va,first,degmax)];
  bb:=uKernel8[CoeffByte(vb,first,degmax)];
  if mode=0 then
    begin
    XorDyn32(dst,dstBit+1,bb);
    XorDyn32(dst,dstBit,aa);
    XorDyn32(dst,dstBit+2,aa);
    end
  else
    begin
    XorDyn32(dst,dstBit+1,aa);
    XorDyn32(dst,dstBit,bb);
    XorDyn32(dst,dstBit+1,bb);
    XorDyn32(dst,dstBit+2,bb);
    end;
  exit;
  end;
h:=count shr 1;
childBits:=(h shl 2)-1;
childWords:=(childBits+31) shr 5;
BuildUComboRecW(va,vb,first,h,degmax,mode,dst,dstBit+(h shl 1),work,workWord);
workBit:=workWord shl 5;
BuildUComboRecW(va,vb,first+h,h,degmax,mode,work,workBit,work,workWord+childWords);
XorDynBits(dst,dstBit,work,workBit,childBits);
XorDynBits(dst,dstBit+h,work,workBit,childBits);
XorDynBits(dst,dstBit+h*3,work,workBit,childBits);
XorDynBits(dst,dstBit+(h shl 2),work,workBit,childBits);
end;

procedure BuildUComboKernelFastW(const va,vb:TVec; degmax,mode:longint;
                                 var r:TWordArray; var center:longint);
var count,bits,k0:longint;
var work:TWordArray;
begin
count:=8;
while count<=degmax do count:=count shl 1;
bits:=(count shl 2)-1;
SetLength(r,(bits+31) shr 5);
for k0:=0 to High(r) do r[k0]:=0;
SetLength(work,count div 8+64);
for k0:=0 to High(work) do work[k0]:=0;
BuildUComboRecW(va,vb,0,count,degmax,mode,r,0,work,0);
center:=(count shl 1)-1;
end;

procedure AddCircularKernelW(var dst:TWordArray; const src:TWordArray; center,shift,period:longint);
var w0,b0,p0,i0:longint;
var q0:LongWord;
begin
for w0:=0 to High(src) do
  begin
  q0:=src[w0];
  while q0<>0 do
    begin
    b0:=LowBit32(q0);
    i0:=(w0 shl 5)+b0;
    p0:=(i0-center+shift) mod period;
    if p0<0 then inc(p0,period);
    dst[p0 shr 5]:=dst[p0 shr 5] xor (LongWord(1) shl (p0 and 31));
    q0:=q0 and (q0-1);
    end;
  end;
end;

function DynBit(const a:TWordArray; p0:longint):LongWord; inline;
begin
DynBit:=(a[p0 shr 5] shr (p0 and 31)) and 1;
end;

{ D=A*B, E=A*reverse(B); all additions below are in GF(2). }
{ C[p]=D[p]+D[2L-p]+E[L-p]+E[L+p]+A[0]B[p]+A[L]B[L-p]. }
procedure ApplyFastUComboW(const va,vb,vsrc:TVec; var vdst:TVec; hi,degmax,mode:longint);
var halfLen,period,convWords,kernelWords,lastWord:longint;
var w0,center,keep,srcBits,lastSrcWord,targetBit,startP:longint;
var q0,bit0:LongWord;
var combo,kernel,ha,hb,hbr,prod0,prod1:TWordArray;
begin
halfLen:=hi+2;
period:=halfLen shl 1;
convWords:=(halfLen+32) shr 5;
BuildUComboKernelFastW(va,vb,degmax,mode,combo,center);
kernelWords:=(period+31) shr 5;
SetLength(kernel,kernelWords);
AddCircularKernelW(kernel,combo,center,0,period);
SetLength(ha,convWords); SetLength(hb,convWords); SetLength(hbr,convWords);
lastWord:=halfLen shr 5;
for w0:=0 to lastWord do ha[w0]:=kernel[w0];
keep:=(halfLen and 31)+1;
if keep<32 then ha[lastWord]:=ha[lastWord] and LowMask32(keep);
srcBits:=hi+1;
lastSrcWord:=hi shr 5;
for w0:=0 to lastSrcWord do
  begin
  q0:=vsrc[w0];
  if w0=lastSrcWord then q0:=q0 and LowMask32(srcBits-(w0 shl 5));
  hb[w0]:=hb[w0] xor (q0 shl 1);
  if w0+1<convWords then hb[w0+1]:=hb[w0+1] xor (q0 shr 31);
  bit0:=Reverse32(q0);
  targetBit:=srcBits-(w0 shl 5)-31;
  if targetBit>=0 then XorDyn32(hbr,targetBit,bit0)
  else if targetBit>-32 then hbr[0]:=hbr[0] xor (bit0 shr (-targetBit));
  end;
KarMulPairFastW(ha,hb,hbr,prod0,prod1,convWords,
                halfLen+1,halfLen,halfLen);
VecZero(vdst);
lastWord:=hi shr 5;
for w0:=0 to lastWord do
  begin
  startP:=(w0 shl 5)+1;
  q0:=ReadDyn32(prod0,startP) xor
      ReadDyn32Reverse(prod0,period-startP) xor
      ReadDyn32Reverse(prod1,halfLen-startP) xor
      ReadDyn32(prod1,halfLen+startP);
  if DynBit(ha,0)<>0 then q0:=q0 xor ReadDyn32(hb,startP);
  if DynBit(ha,halfLen)<>0 then
    q0:=q0 xor ReadDyn32Reverse(hb,halfLen-startP);
  vdst[w0]:=q0;
  end;
MaskDeg(vdst,hi);
end;


procedure ApplyBezoutU(const vu,vv,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var d,du,dv,j2:longint;
var bu,bv:boolean;
begin
VecZero(cur0); VecZero(cur1); VecZero(vdst);
VecCopy(cur0,vsrc);
MaskDeg(cur0,hi);
du:=TopBitLE(vu,degmax);
dv:=TopBitLE(vv,degmax);
if du>dv then d:=du else d:=dv;
if d<0 then exit;
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  bu:=GetBit(vu,j2)<>0;
  bv:=GetBit(vv,j2)<>0;
  if j2>=d then
    begin
    if bu and bv then VecXorIHTo(vdst,pcur^,hi)
    else if bv then VecXorRaw(vdst,pcur^)
    else if bu then VecXorHTo(vdst,pcur^,hi);
    break;
    end;
  if bu and bv then VecStepJXorTo(vdst,pnxt^,pcur^,hi,3)
  else if bv then VecStepJXorTo(vdst,pnxt^,pcur^,hi,1)
  else if bu then VecStepJXorTo(vdst,pnxt^,pcur^,hi,2)
  else VecStepJ(pnxt^,pcur^,hi);
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
MaskDeg(vdst,hi);
end;

procedure ApplyCU(const va,vb,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var d,da,db,j2:longint;
var ba,bb:boolean;
begin
VecZero(cur0); VecZero(cur1); VecZero(vdst);
VecCopy(cur0,vsrc);
MaskDeg(cur0,hi);
da:=TopBitLE(va,degmax);
db:=TopBitLE(vb,degmax);
if da>db then d:=da else d:=db;
if d<0 then exit;
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  ba:=GetBit(va,j2)<>0;
  bb:=GetBit(vb,j2)<>0;
  if j2>=d then
    begin
    if ba and bb then VecXorHTo(vdst,pcur^,hi)
    else if bb then VecXorIHTo(vdst,pcur^,hi)
    else if ba then VecXorRaw(vdst,pcur^);
    break;
    end;
  if ba and bb then VecStepJXorTo(vdst,pnxt^,pcur^,hi,2)
  else if bb then VecStepJXorTo(vdst,pnxt^,pcur^,hi,3)
  else if ba then VecStepJXorTo(vdst,pnxt^,pcur^,hi,1)
  else VecStepJ(pnxt^,pcur^,hi);
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
MaskDeg(vdst,hi);
end;

function BuildOddGUV(const ma,mb,mg,mu,mv:TVec; var gu,qu,qv:TVec; hi,srcHi:longint; extra:boolean):boolean;
var tu,tv:TVec;
var p,dg,du,dv,s:longint;
begin
VecZero(gu);
VecZero(qu);
VecZero(qv);
VecCopy(tu,mu); MaskDeg(tu,srcHi);
VecCopy(tv,mv); MaskDeg(tv,srcHi);
if (not extra) and ((GetBit(tu,0) xor GetBit(tv,0))<>0) then
  begin
  VecXorEq(tu,mb); MaskDeg(tu,srcHi);
  VecXorEq(tv,ma); MaskDeg(tv,srcHi);
  end;
if (not extra) and ((GetBit(tu,0) xor GetBit(tv,0))<>0) then
  begin
  BuildOddGUV:=false;
  exit;
  end;
dg:=TopBitLE(mg,srcHi);
if dg>=0 then
  for p:=0 to dg do if GetBit(mg,p)<>0 then
    begin
    s:=p shl 1;
    if extra then inc(s);
    if s<=hi then SetBit(gu,s,GetBit(gu,s) xor 1);
    end;
du:=TopBitLE(tu,srcHi);
dv:=TopBitLE(tv,srcHi);
if extra then
  begin
  if du>=0 then
    for p:=0 to du do if GetBit(tu,p)<>0 then
      begin
      s:=p shl 1;
      if s<=hi then SetBit(qu,s,GetBit(qu,s) xor 1);
      if s+1<=hi then
        begin
        SetBit(qu,s+1,GetBit(qu,s+1) xor 1);
        SetBit(qv,s+1,GetBit(qv,s+1) xor 1);
        end;
      end;
  if dv>=0 then
    for p:=0 to dv do if GetBit(tv,p)<>0 then
      begin
      s:=p shl 1;
      if s<=hi then SetBit(qu,s,GetBit(qu,s) xor 1);
      end;
  end
else
  begin
  if du>=0 then
    for p:=0 to du do if GetBit(tu,p)<>0 then
      begin
      s:=p shl 1;
      if s<=hi+1 then SetBit(qu,s,GetBit(qu,s) xor 1);
      if s+1<=hi+1 then SetBit(qu,s+1,GetBit(qu,s+1) xor 1);
      if s<=hi then SetBit(qv,s,GetBit(qv,s) xor 1);
      end;
  if dv>=0 then
    for p:=0 to dv do if GetBit(tv,p)<>0 then
      begin
      s:=p shl 1;
      if s<=hi+1 then SetBit(qu,s,GetBit(qu,s) xor 1);
      end;
  if GetBit(qu,0)<>0 then
    begin
    BuildOddGUV:=false;
    exit;
    end;
  for p:=0 to hi do SetBit(qu,p,GetBit(qu,p+1));
  SetBit(qu,hi+1,0);
  MaskDeg(qu,hi);
  end;
MaskDeg(gu,hi);
MaskDeg(qu,hi);
MaskDeg(qv,hi);
BuildOddGUV:=true;
end;

procedure CalcMat2;
var gu,qu,qv:TVec;
var sa,sb,hu,su,sv:TVec;
var v,z:TVec;
var g0,g1,g2:TVec;
var i0,r0,rU,jmax,row1,row2,row3,l0,l1,l2,r1,r2,w,wl,wr:longint;
var m2,hiS,rr,du,dv:longint;
var tm,val:LongWord;
var pg0,pg1,pg2,pt:PVec;

function RangeMask(w,l,r:longint):LongWord;
var wl0,wr0:longint;
var ml,mr:LongWord;
begin
if (l>r) or (w<0) or (w>=wn) then begin RangeMask:=0; exit; end;
wl0:=l shr 5;
wr0:=r shr 5;
if (w<wl0) or (w>wr0) then begin RangeMask:=0; exit; end;
if wl0=wr0 then
  begin
  ml:=LongWord($FFFFFFFF) shl (l and 31);
  if (r and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r and 31)+1))-1;
  RangeMask:=ml and mr;
  end
else if w=wl0 then
  RangeMask:=LongWord($FFFFFFFF) shl (l and 31)
else if w=wr0 then
  begin
  if (r and 31)=31 then RangeMask:=$FFFFFFFF else RangeMask:=(LongWord(1) shl ((r and 31)+1))-1;
  end
else
  RangeMask:=$FFFFFFFF;
end;

procedure CropRange(var a:TVec;l,r:longint);
var wl0,wr0,k2:longint;
var ml,mr:LongWord;
begin
if l<0 then l:=0;
if r>longint(n)-1 then r:=longint(n)-1;
if l>r then begin VecZero(a); VecNorm(a); exit; end;
wl0:=l shr 5;
wr0:=r shr 5;
for k2:=0 to wl0-1 do a[k2]:=0;
if wl0=wr0 then
  begin
  ml:=LongWord($FFFFFFFF) shl (l and 31);
  if (r and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r and 31)+1))-1;
  a[wl0]:=a[wl0] and (ml and mr);
  end
else
  begin
  ml:=LongWord($FFFFFFFF) shl (l and 31);
  if (r and 31)=31 then mr:=$FFFFFFFF else mr:=(LongWord(1) shl ((r and 31)+1))-1;
  a[wl0]:=a[wl0] and ml;
  a[wr0]:=a[wr0] and mr;
  end;
for k2:=wr0+1 to wn-1 do a[k2]:=0;
VecNorm(a);
end;

begin
TimeMark('c');
TimeMark('q');
if (n and 1)=0 then
  begin
  m2:=longint(n div 2);
  EnsureAB(m2);
  hiS:=m2 div 2;
  VecZero(gu); VecZero(qu); VecZero(qv);
  VecCopy(sa,hf);
  VecXorEq(sa,hf1);
  MaskDeg(sa,hiS);
  VecCopy(sb,hc);
  VecXorEq(sb,hc1);
  MaskDeg(sb,hiS);
  rr:=GcdU(sa,sb,hu,su,sv,hiS);
  for i:=0 to rr do if GetBit(hu,i)<>0 then SetBit(gu,i shl 1,1);
  du:=TopBitLE(su,hiS);
  for i:=0 to du do if GetBit(su,i)<>0 then
    begin
    SetBit(qu,i shl 1,1);
    if (i shl 1)+1<=longint(n div 2) then SetBit(qv,(i shl 1)+1,GetBit(qv,(i shl 1)+1) xor 1);
    end;
  dv:=TopBitLE(sv,hiS);
  for i:=0 to dv do if GetBit(sv,i)<>0 then SetBit(qv,i shl 1,GetBit(qv,i shl 1) xor 1);
  rU:=rr shl 1;
  end
else
  begin
  m2:=longint(n div 2);
  EnsureAB(m2);
  hiS:=m2 div 2;
  rr:=GcdU(hf,hc,hu,su,sv,hiS);
  if BuildOddGUV(hf,hc,hu,su,sv,gu,qu,qv,longint(n div 2),hiS,(m2 mod 3)=2) then
    rU:=TopBitLE(gu,longint(n div 2))
  else
    rU:=GcdU(f,c,gu,qu,qv,longint(n div 2));
  end;
r0:=rU*2;
TimeMark('z');
ApplyFastUComboW(qu,qv,y,z,n-1,longint(n div 2),0);
TimeMark('d');
if r0=0 then
  begin
  VecCopy(x,z);
  end
else
begin
TimeMark('x');
ApplyPolyU0(gu,g0,n-1,rU);
pg0:=@g0; pg1:=@g1; pg2:=@g2;
if n-r0-1<0 then jmax:=0 else jmax:=n-r0-1;
if jmax=0 then begin VecCopy(pg1^,pg0^); VecZero(pg2^); end
else if r0<jmax then
  begin
  VecZero(v);
  VecShiftL1(v1,pg0^);
  VecShiftR1(v2,pg0^);
  VecCopy(v,v1);
  VecXorEq(v,v2);
  MaskDeg(v,n-1);
  VecZero(pg1^); VecZero(pg2^);
  for i:=0 to n-1 do if ((pg0^[i shr 5] shr (i and 31)) and 1)<>0 then pg1^[(n-1-i) shr 5]:=pg1^[(n-1-i) shr 5] or (LongWord(1) shl ((n-1-i) and 31));
  for i:=0 to n-1 do if ((v[i shr 5] shr (i and 31)) and 1)<>0 then pg2^[(n-1-i) shr 5]:=pg2^[(n-1-i) shr 5] or (LongWord(1) shl ((n-1-i) and 31));
  MaskDeg(pg1^,n-1); MaskDeg(pg2^,n-1);
  for j:=1 to r0 do
    begin
    VecShiftL1(v1,pg2^);
    VecShiftR1(v2,pg2^);
    VecCopy(pg0^,v1);
    VecXorEq(pg0^,v2);
    VecXorEq(pg0^,pg1^);
    MaskDeg(pg0^,n-1);
    pt:=pg0; pg0:=pg1; pg1:=pg2; pg2:=pt;
    end;
  end
else
  begin
  VecZero(pg2^);
  VecCopy(pg1^,pg0^);
  for j:=1 to jmax do
    begin
    VecShiftL1(v1,pg1^);
    VecShiftR1(v2,pg1^);
    VecCopy(pg0^,v1);
    VecXorEq(pg0^,v2);
    VecXorEq(pg0^,pg2^);
    MaskDeg(pg0^,n-1);
    pt:=pg0; pg0:=pg2; pg2:=pg1; pg1:=pt;
    end;
  end;
VecZero(x); VecNorm(x);
row1:=n-1;
row2:=n-2;
l1:=row1-(r0 shl 1); if l1<0 then l1:=0; r1:=row1; if r1>longint(n)-1 then r1:=longint(n)-1;
l2:=row2-(r0 shl 1); if l2<0 then l2:=0; r2:=row2;
CropRange(pg1^,l1,r1);
CropRange(pg2^,l2,r2);
VecZero(pg0^); VecNorm(pg0^);
if r0<=n-1 then
for i:=n-1 downto r0 do
  begin
  if ((z[i shr 5] shr (i and 31)) and 1)<>0 then
  begin
    i0:=i-r0;
    VecXorRange(z,pg1^,l1,r1);
    x[i0 shr 5]:=x[i0 shr 5] or (LongWord(1) shl (i0 and 31));
  end;
  if i>r0 then
    begin
    row3:=row2-1;
    l0:=row3-(r0 shl 1); if l0<0 then l0:=0;
    wl:=l0 shr 5;
    wr:=row3 shr 5;
    for w:=wl to wr do
      begin
      tm:=RangeMask(w,l0,row3);
      val:=pg1^[w] xor (pg2^[w] shl 1) xor (pg2^[w-1] shr 31) xor (pg2^[w] shr 1) xor (pg2^[w+1] shl 31);
      pg0^[w]:=val and tm;
      end;
    if wr+1<wn then pg0^[wr+1]:=0;
    pt:=pg0; pg0:=pg1; pg1:=pg2; pg2:=pt;
    row1:=row2;
    row2:=row3;
    l1:=l2; r1:=r2;
    l2:=l0; r2:=row3;
    end;
  end;
VecNorm(x);
end;
end;

function GeneMat():boolean;
var t:TVec;
var wn0:longint;
var mask0:LongWord;
var k2:longint;
begin
TimeMark('g');
ApplyFastUComboW(f,c,x,t,n-1,longint(n div 2),1);
wn0:=(longint(n)+31) shr 5;
if (longint(n) and 31)=0 then mask0:=$FFFFFFFF else mask0:=(LongWord(1) shl (longint(n) and 31))-1;
GeneMat:=true;
for k2:=0 to wn0-2 do GeneMat:=GeneMat and (t[k2]=y[k2]);
GeneMat:=GeneMat and (((t[wn0-1] xor y[wn0-1]) and mask0)=0);
write(GeneMat);
end;

begin
{$ifdef disp}
CreateWin(m,m);
bb:=CreateBB(GetWin());
bp:=CreateBMP(m,m);
{$endif}
QueryPerformanceFrequency(perfFreq);
QueryPerformanceCounter(lastCounter);
hasLastCounter:=false;
InitMul8;
InitUKernel8;
{$ifdef disp}
for n:=1 to m do
{$else}
for n:=9900 to 10000 do
{$endif}
  begin
  PrepN;
  write(n,#9);
  MakeMat();
  CalcMat2();
  GeneMat();{$ifdef disp}write('%');SaveMat('_T2');{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
