//{$define disp}
program diandeng;
{$mode objfpc}{$H+}

{$ifdef disp}
uses Windows, display;
const m=1000;
const sosN=1024;
{$else}
uses Windows;
const m=10000;
const sosN=16384;
{$endif}

const wb=32;
const mw=(m+wb-1)div wb;

type TVec=array[-2..mw]of LongWord;
     TSos=array[0..sosN-1]of byte;

var n:longword;
var i,j:longint;
var x,y,y1,y_,y_1,f,f1:TVec;
var k:longint;
var o:boolean;
var perfFreq,lastCounter:Int64;
var hasLastCounter:boolean;
var wn:longint;
var lastMask:LongWord;
var ones:TVec;
var v0,v1,v2,v3:TVec;

{$ifdef disp}
var bb:pbitbuf;
var bp:pbitmap;
{$endif}

procedure VecNorm(var a:TVec);
var k2:longint;
begin
a[-2]:=0; a[-1]:=0;
for k2:=wn to mw do a[k2]:=0;
a[wn-1]:=a[wn-1] and lastMask;
end;

procedure VecZero(var v:TVec);
var k2:longint;
begin
for k2:=-2 to mw do v[k2]:=0;
end;

procedure VecCopy(var a:TVec;const b:TVec);
var k2:longint;
begin
for k2:=-2 to mw do a[k2]:=b[k2];
VecNorm(a);
end;

procedure VecXorEq(var a:TVec;const b:TVec);
var k2:longint;
begin
for k2:=0 to wn-1 do a[k2]:=a[k2] xor b[k2];
VecNorm(a);
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
for k2:=wn to mw do dst[k2]:=0;
VecNorm(dst);
end;

procedure VecShiftR1(var dst:TVec;const src:TVec);
var k2:longint;
begin
dst[-2]:=0; dst[-1]:=0;
for k2:=0 to wn-1 do
  dst[k2]:=(src[k2] shr 1) or (src[k2+1] shl 31);
for k2:=wn to mw do dst[k2]:=0;
VecNorm(dst);
end;

procedure VecShiftL2(var dst:TVec;const src:TVec);
var k2:longint;
begin
dst[-2]:=0; dst[-1]:=0;
for k2:=0 to wn-1 do
  dst[k2]:=(src[k2] shl 2) or (src[k2-1] shr 30);
for k2:=wn to mw do dst[k2]:=0;
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


function VecIsZero(const a:TVec):boolean;
var k2:longint;
begin
for k2:=0 to wn-1 do if a[k2]<>0 then begin VecIsZero:=false; exit; end;
VecIsZero:=true;
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

procedure BuildC(const vf:TVec; var vc:TVec);
var tmp:TSos;
var bit,base,t:longint;
begin
for base:=0 to sosN-1 do tmp[base]:=0;
for base:=0 to n do if GetBit(vf,base)<>0 then tmp[base]:=1;
bit:=1;
while bit<sosN do
  begin
  base:=0;
  while base<sosN do
    begin
    for t:=0 to bit-1 do tmp[base+t]:=tmp[base+t] xor tmp[base+t+bit];
    inc(base,bit shl 1);
    end;
  bit:=bit shl 1;
  end;
VecZero(vc);
for base:=0 to n do if tmp[base]<>0 then vc[base shr 5]:=vc[base shr 5] or (LongWord(1) shl (base and 31));
VecNorm(vc);
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
var y2,y_2,f2:TVec;
begin
TimeMark('m');
if (not o) or (longint(n)<k) then
  begin
  VecZero(y1); VecZero(y); VecZero(y_1); VecZero(y_);
  VecZero(f1); VecZero(f);
  SetBit(f,0,1);
  k:=0; o:=true;
  end;
for j:=k+1 to n do
  begin
  VecZero(y_2); VecZero(y2);
  VecShiftL1(v1,y_);
  VecShiftR1(v2,y_);
  VecCopy(y_2,v1);
  VecXorEq(y_2,y_);
  VecXorEq(y_2,v2);
  VecXorEq(y_2,y_1);
  MaskDeg(y_2,j-1);
  VecShiftL2(v1,y);
  VecShiftL1(v2,y);
  VecCopy(y2,v1);
  VecXorEq(y2,v2);
  VecXorEq(y2,y);
  VecShiftL2(v1,y1);
  VecXorEq(y2,v1);
  VecShiftL1(v1,y_);
  VecXorEq(y2,v1);
  VecXorEq(y2,y_);
  VecShiftR1(v1,y_);
  VecXorEq(y2,v1);
  VecShiftL1(v1,y_1);
  VecXorEq(y2,v1);
  VecXorEq(y2,y_1);
  VecXorEq(y2,ones);
  MaskDeg(y2,j-1);
  SetBit(y_2,0,GetBit(y2,0));
  y_2[-2]:=1;
  y_1:=y_; y_:=y_2; y1:=y; y:=y2;
  end;
for j:=k+1 to n do
  begin
  VecZero(f2);
  VecShiftL1(v1,f);
  VecCopy(f2,v1);
  VecXorEq(f2,f1);
  MaskDeg(f2,j);
  f1:=f; f:=f2;
  end;
k:=n;
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

function gcd(vf,vg:TVec; var vd,vr:TVec):longint;
var vx,vy:TVec;
var kf,kg:longint;
var done:boolean;
begin
VecNorm(vf); VecNorm(vg);
kf:=TopBit(vf);
kg:=TopBit(vg);
done:=false;
VecZero(vx); VecZero(vy); SetBit(vy,0,1);
repeat
if kf<kg then begin v0:=vf; vf:=vg; vg:=v0; v0:=vx; vx:=vy; vy:=v0; j:=kf; kf:=kg; kg:=j; end;
if kg<0 then begin vd:=vf; vr:=vx; gcd:=kf; done:=true; end;
if not(done) then
  begin
  VecXorShift(vf,vg,kf-kg);
  VecXorShift(vx,vy,kf-kg);
  kf:=TopBit(vf);
  kg:=TopBit(vg);
  end;
until done;
end;

procedure CalcMat2;
var c,q,g:TVec;
var v,z:TVec;
var g0,g1,g2:TVec;
var i0,r0,jmax:longint;
begin
TimeMark('c');
BuildC(f,c);
TimeMark('q');
r0:=gcd(f,c,g,q);
TimeMark('z');
VecCopy(v,y); MaskDeg(v,n-1);
VecZero(z); VecNorm(z);
for j:=0 to n-1 do 
  begin
  if GetBit(q,j)<>0 then VecXorEq(z,v);
  VecShiftL1(v1,v);
  VecShiftR1(v2,v);
  VecCopy(v,v1);
  VecXorEq(v,v2);
  MaskDeg(v,n-1);
  if VecIsZero(v) then break;
  end;
TimeMark('d');
if r0=0 then
  begin
  x:=z;
  VecNorm(x);
  end
else
begin
VecZero(g0); VecZero(g1); VecZero(g2);
VecZero(v); SetBit(v,0,1);
for j:=0 to r0 do 
  begin
  if GetBit(g,j)<>0 then VecXorEq(g0,v);
  VecShiftL1(v1,v);
  VecShiftR1(v2,v);
  VecCopy(v,v1);
  VecXorEq(v,v2);
  MaskDeg(v,n-1);
  if VecIsZero(v) then break;
  end;
TimeMark('x');
MaskDeg(g0,n-1);
if n-r0-1<0 then jmax:=0 else jmax:=n-r0-1;
if jmax=0 then VecCopy(g1,g0)
else if r0<jmax then
  begin
  VecZero(v);
  VecShiftL1(v1,g0);
  VecShiftR1(v2,g0);
  VecCopy(v,v1);
  VecXorEq(v,v2);
  MaskDeg(v,n-1);
  VecZero(g1); VecZero(g2);
  for i:=0 to n-1 do if GetBit(g0,i)<>0 then SetBit(g1,n-1-i,1);
  for i:=0 to n-1 do if GetBit(v,i)<>0 then SetBit(g2,n-1-i,1);
  MaskDeg(g1,n-1); MaskDeg(g2,n-1);
  for j:=1 to r0 do
    begin
    VecShiftL1(v1,g2);
    VecShiftR1(v2,g2);
    VecCopy(g0,v1);
    VecXorEq(g0,v2);
    VecXorEq(g0,g1);
    MaskDeg(g0,n-1);
    g1:=g2;
    g2:=g0;
    end;
  end
else
  begin
  VecCopy(g1,g0);
  for j:=1 to jmax do
    begin
    VecShiftL1(v1,g1);
    VecShiftR1(v2,g1);
    VecCopy(g0,v1);
    VecXorEq(g0,v2);
    VecXorEq(g0,g2);
    MaskDeg(g0,n-1);
    g2:=g1;
    g1:=g0;
    end;
  end;
VecZero(x); VecNorm(x);
if r0<=n-1 then
for i:=n-1 downto r0 do
  begin
  if GetBit(z,i)<>0 then
  begin
    i0:=i-r0;
    VecXorRange(z,g1,i-r0-r0,i);
    SetBit(x,i0,1);
  end;
  if i>r0 then
    begin
    VecShiftL1(v1,g2);
    VecShiftR1(v2,g2);
    VecCopy(g0,v1);
    VecXorEq(g0,v2);
    VecXorEq(g0,g1);
    MaskDeg(g0,n-1);
    g1:=g2;
    g2:=g0;
    end;
  end;
end;
end;

function GeneMat():boolean;
var wn0:longint;
var mask0:LongWord;
var k2:longint;
var x2,x1,x0:TVec;
begin
TimeMark('g');
VecZero(x2); VecNorm(x2);
VecCopy(x1,x); MaskDeg(x1,n-1);
{$ifdef disp}
while IsNextMsg() do ;
for i:=0 to n-1 do
  if GetBit(x1,i)<>0 then SetBBPixel(bb,i,0,black) else SetBBPixel(bb,i,0,white);
{$endif}
for j:=1 to n-1 do
  begin
  VecShiftL1(v1,x1);
  VecShiftR1(v2,x1);
  VecCopy(x0,v1);
  VecXorEq(x0,x1);
  VecXorEq(x0,v2);
  VecXorEq(x0,x2);
  VecXorEq(x0,ones);
  MaskDeg(x0,n-1);
  {$ifdef disp}
  for i:=0 to n-1 do
    if GetBit(x0,i)<>0 then SetBBPixel(bb,i,j,black) else SetBBPixel(bb,i,j,white);
  {$endif}
  VecCopy(x2,x1);
  VecCopy(x1,x0);
  end;
VecShiftL1(v1,x1);
VecShiftR1(v2,x1);
VecCopy(v3,v1);
VecXorEq(v3,x1);
VecXorEq(v3,v2);
VecXorEq(v3,x2);
MaskDeg(v3,n-1);
wn0:=(longint(n)+31) shr 5;
if (longint(n) and 31)=0 then mask0:=$FFFFFFFF else mask0:=(LongWord(1) shl (longint(n) and 31))-1;
GeneMat:=true;
for k2:=0 to wn0-2 do GeneMat:=GeneMat and (v3[k2]=$FFFFFFFF);
GeneMat:=GeneMat and ((v3[wn0-1] and mask0)=mask0);
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
{$ifdef disp}
for n:=1 to m do
{$else}
for n:=9900 to m do
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
