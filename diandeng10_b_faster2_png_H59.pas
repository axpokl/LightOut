//{$define disp}
program diandeng;
{$mode objfpc}{$H+}

{ H59: build Y directly with its Fibonacci-sum polynomial. }
{ A and B use the same operations; only Boolean/LongWord storage differs. }

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
var x,y,f,f1,c,c1:TVec;
var hf,hf1,hc,hc1:TVec;
var perfFreq,lastCounter:Int64;
var hasLastCounter:boolean;
var wn:longint;
var lastMask:LongWord;
var nMask:LongWord;
var nWord:longint;
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

procedure PrepN;
var bits:longint;
var rem:longint;
begin
bits:=longint(n)+1;
wn:=(bits+31) shr 5;
rem:=bits and 31;
if rem=0 then lastMask:=$FFFFFFFF else lastMask:=(LongWord(1) shl rem)-1;
nWord:=(longint(n)-1) shr 5;
rem:=longint(n) and 31;
if rem=0 then nMask:=$FFFFFFFF else nMask:=(LongWord(1) shl rem)-1;
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

function ReverseWord32(x:LongWord):LongWord; inline;
begin
x:=((x and $55555555) shl 1) or ((x shr 1) and $55555555);
x:=((x and $33333333) shl 2) or ((x shr 2) and $33333333);
x:=((x and $0F0F0F0F) shl 4) or ((x shr 4) and $0F0F0F0F);
x:=((x and $00FF00FF) shl 8) or ((x shr 8) and $00FF00FF);
ReverseWord32:=(x shl 16) or (x shr 16);
end;

function ReadVec32Any(const a:TVec; bit0:longint):LongWord;
var w,b:longint;
var r:LongWord;
begin
if bit0>=0 then
  begin
  w:=bit0 shr 5; b:=bit0 and 31;
  if w>mw then begin ReadVec32Any:=0; exit; end;
  r:=a[w] shr b;
  if (b<>0) and (w<mw) then r:=r xor (a[w+1] shl (32-b));
  ReadVec32Any:=r;
  end
else if bit0<=-32 then ReadVec32Any:=0
else ReadVec32Any:=a[0] shl (-bit0);
end;

procedure BuildYFast(var dy_,dy:TVec; const sy_,sy_1,sy,sy1:TVec; deg:longint); inline;
var w,hiw,half,halfw,idx,src:longint;
var mask:LongWord;
begin
hiw:=deg shr 5;
dy_[-2]:=0; dy_[-1]:=0; dy[-2]:=0; dy[-1]:=0;
for w:=0 to hiw do
  dy_[w]:=((sy_[w] shl 1) or (sy_[w-1] shr 31)) xor
          sy_[w] xor
          ((sy_[w] shr 1) or (sy_[w+1] shl 31)) xor
          sy_1[w];
half:=deg div 2;
halfw:=half shr 5;
for w:=0 to halfw do
  dy[w]:=((sy[w] shl 2) or (sy[w-1] shr 30)) xor
         ((sy[w] shl 1) or (sy[w-1] shr 31)) xor
         sy[w] xor
         ((sy1[w] shl 2) or (sy1[w-1] shr 30)) xor
         dy_[w] xor
         ((sy_1[w] shl 1) or (sy_1[w-1] shr 31)) xor
         $FFFFFFFF;
mask:=DegMask(deg);
dy_[hiw]:=dy_[hiw] and mask;
dy[halfw]:=dy[halfw] and DegMask(half);
if half+1<=deg then
  begin
  idx:=half+1; src:=deg-half-1;
  if ((dy[src shr 5] shr (src and 31)) and 1)<>0 then
    dy[idx shr 5]:=dy[idx shr 5] or (LongWord(1) shl (idx and 31))
  else
    dy[idx shr 5]:=dy[idx shr 5] and not(LongWord(1) shl (idx and 31));
  end;
if hiw+1<=mw then dy_[hiw+1]:=0;
end;

procedure ExpandPalindrome(var a:TVec; deg:longint);
var first,bw,hiw,w,off,startP:longint;
var q,lowmask:LongWord;
begin
if deg<0 then exit;
first:=(deg div 2)+1;
bw:=first shr 5;
hiw:=deg shr 5;
for w:=hiw downto bw+1 do
  begin
  startP:=w shl 5;
  a[w]:=ReverseWord32(ReadVec32Any(a,deg-startP-31));
  end;
startP:=bw shl 5;
q:=ReverseWord32(ReadVec32Any(a,deg-startP-31));
off:=first and 31;
if off=0 then lowmask:=0 else lowmask:=(LongWord(1) shl off)-1;
a[bw]:=(a[bw] and lowmask) or (q and not lowmask);
a[hiw]:=a[hiw] and DegMask(deg);
if hiw+1<=mw then a[hiw+1]:=0;
end;

function SpreadBits32(x:LongWord):QWord; inline;
var z0:QWord;
begin
z0:=x;
z0:=(z0 or (z0 shl 16)) and QWord($0000FFFF0000FFFF);
z0:=(z0 or (z0 shl 8)) and QWord($00FF00FF00FF00FF);
z0:=(z0 or (z0 shl 4)) and QWord($0F0F0F0F0F0F0F0F);
z0:=(z0 or (z0 shl 2)) and QWord($3333333333333333);
z0:=(z0 or (z0 shl 1)) and QWord($5555555555555555);
SpreadBits32:=z0;
end;

procedure PutFCDouble(var a:TWordArray; pos:longint; v:QWord); inline;
begin
if pos<=High(a) then a[pos]:=LongWord(v);
if pos+1<=High(a) then a[pos+1]:=LongWord(v shr 32);
end;

procedure DoubleFCDynW(nn:longword; const af,ac,af1,ac1:TWordArray;
                       var nf,nc,nf1,nc1:TWordArray);
var w0,ow,hi0,words:longint;
var saf,sac,saf1,sac1,sef,soc,vf,vc,vf1,vc1:QWord;
var mask0:LongWord;
begin
hi0:=longint(nn div 2);
words:=(hi0 shr 5)+1;
SetLength(nf,words); SetLength(nc,words);
SetLength(nf1,words); SetLength(nc1,words);
for w0:=0 to High(af) do
  begin
  ow:=w0 shl 1;
  saf:=SpreadBits32(af[w0]); sac:=SpreadBits32(ac[w0]);
  saf1:=SpreadBits32(af1[w0]); sac1:=SpreadBits32(ac1[w0]);
  if (nn and 1)=0 then
    begin
    sef:=saf xor saf1; soc:=sac xor sac1;
    vf:=sef xor (soc shl 1);
    vc:=soc;
    vf1:=sac1 shl 1;
    vc1:=(saf1 xor sac1) xor (sac1 shl 1);
    end
  else
    begin
    vf:=sac shl 1;
    vc:=(saf xor sac) xor (sac shl 1);
    vf1:=(saf xor saf1) xor ((sac xor sac1) shl 1);
    vc1:=sac xor sac1;
    end;
  PutFCDouble(nf,ow,vf); PutFCDouble(nc,ow,vc);
  PutFCDouble(nf1,ow,vf1); PutFCDouble(nc1,ow,vc1);
  end;
mask0:=DegMask(hi0);
nf[High(nf)]:=nf[High(nf)] and mask0;
nc[High(nc)]:=nc[High(nc)] and mask0;
nf1[High(nf1)]:=nf1[High(nf1)] and mask0;
nc1[High(nc1)]:=nc1[High(nc1)] and mask0;
end;

procedure BuildFCDynW(nn:longword; var nf,nc,nf1,nc1:TWordArray);
var af,ac,af1,ac1:TWordArray;
begin
if nn=0 then
  begin
  SetLength(nf,1); SetLength(nc,1);
  SetLength(nf1,1); SetLength(nc1,1);
  nf[0]:=1;
  exit;
  end;
BuildFCDynW(nn div 2,af,ac,af1,ac1);
DoubleFCDynW(nn,af,ac,af1,ac1,nf,nc,nf1,nc1);
end;

procedure CopyFCDynW(var dst:TVec; const src:TWordArray; hi:longint); inline;
var w0:longint;
begin
VecZero(dst);
for w0:=0 to High(src) do dst[w0]:=src[w0];
MaskDeg(dst,hi);
end;

procedure BuildFCPairsFastW(nn:longword; var nf,nc,nf1,nc1,hf0,hc0,hf10,hc10:TVec);
var df,dc,df1,dc1,dhf,dhc,dhf1,dhc1:TWordArray;
var hi0,hhi:longint;
begin
BuildFCDynW(nn div 2,dhf,dhc,dhf1,dhc1);
if nn=0 then
  begin
  df:=dhf; dc:=dhc; df1:=dhf1; dc1:=dhc1;
  end
else
  DoubleFCDynW(nn,dhf,dhc,dhf1,dhc1,df,dc,df1,dc1);
hi0:=longint(nn div 2); hhi:=longint((nn div 2) div 2);
CopyFCDynW(nf,df,hi0); CopyFCDynW(nc,dc,hi0);
CopyFCDynW(nf1,df1,hi0); CopyFCDynW(nc1,dc1,hi0);
CopyFCDynW(hf0,dhf,hhi); CopyFCDynW(hc0,dhc,hhi);
CopyFCDynW(hf10,dhf1,hhi); CopyFCDynW(hc10,dhc1,hhi);
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

procedure ApplyUComboOnesW(const va,vb:TVec; var vdst:TVec; hi,degmax:longint); forward;

procedure MakeMat();
var yp,yq:TVec;
var w0,lastW:longint;
begin
TimeMark('m');
BuildFCPairsFastW(n,f,c,f1,c1,hf,hc,hf1,hc1);
VecZero(yp); VecZero(yq);
lastW:=longint(n div 2) shr 5;
for w0:=0 to lastW do
  yq[w0]:=((f[w0] xor f1[w0]) shr 1) xor
           ((f[w0+1] xor f1[w0+1]) shl 31);
MaskDeg(yq,longint(n div 2)-1);
for w0:=0 to lastW do yp[w0]:=c[w0] xor c1[w0] xor yq[w0];
MaskDeg(yp,longint(n div 2));
ApplyUComboOnesW(yp,yq,y,n-1,longint(n div 2));
end;

function HighBit32(x:LongWord):longint; inline;
begin
if x=0 then HighBit32:=-1 else HighBit32:=BsrDWord(x);
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

procedure XorShiftPair(var ar,av:TVec; const br,bv:TVec;
                       sh,dr,dv:longint); inline;
var ws,bs,wl,wrr,wrv,wrc,k2,si:longint;
var r0,v0,mrr,mrv,mskr,mskv:LongWord;
begin
if dv<0 then
  begin
  VecXorShiftRange(ar,br,sh,dr);
  exit;
  end;
ws:=sh shr 5;
bs:=sh and 31;
wl:=ws;
wrr:=(sh+dr) shr 5;
wrv:=(sh+dv) shr 5;
if wrr<wrv then wrc:=wrr else wrc:=wrv;
if ((sh+dr) and 31)=31 then mrr:=$FFFFFFFF
else mrr:=(LongWord(1) shl (((sh+dr) and 31)+1))-1;
if ((sh+dv) and 31)=31 then mrv:=$FFFFFFFF
else mrv:=(LongWord(1) shl (((sh+dv) and 31)+1))-1;
if bs=0 then
  begin
  for k2:=wl to wrc-1 do
    begin
    si:=k2-ws;
    ar[k2]:=ar[k2] xor br[si];
    av[k2]:=av[k2] xor bv[si];
    end;
  end
  else
    begin
    if wrc>wl then
      begin
      ar[wl]:=ar[wl] xor (br[0] shl bs);
      av[wl]:=av[wl] xor (bv[0] shl bs);
      for k2:=wl+1 to wrc-1 do
        begin
        si:=k2-ws;
        r0:=(br[si] shl bs) or (br[si-1] shr (32-bs));
        v0:=(bv[si] shl bs) or (bv[si-1] shr (32-bs));
        ar[k2]:=ar[k2] xor r0;
        av[k2]:=av[k2] xor v0;
        end;
      end;
    end;
  si:=wrc-ws;
  if bs=0 then
    begin
    r0:=br[si]; v0:=bv[si];
    end
  else if wrc=wl then
    begin
    r0:=br[0] shl bs; v0:=bv[0] shl bs;
    end
  else
    begin
    r0:=(br[si] shl bs) or (br[si-1] shr (32-bs));
    v0:=(bv[si] shl bs) or (bv[si-1] shr (32-bs));
    end;
  mskr:=$FFFFFFFF; mskv:=$FFFFFFFF;
  if wrc=wrr then mskr:=mrr;
  if wrc=wrv then mskv:=mrv;
  ar[wrc]:=ar[wrc] xor (r0 and mskr);
  av[wrc]:=av[wrc] xor (v0 and mskv);
if wrr>wrc then
  begin
  for k2:=wrc+1 to wrr-1 do
    begin
    si:=k2-ws;
    if bs=0 then r0:=br[si]
    else r0:=(br[si] shl bs) or (br[si-1] shr (32-bs));
    ar[k2]:=ar[k2] xor r0;
    end;
  si:=wrr-ws;
  if bs=0 then r0:=br[si]
  else r0:=(br[si] shl bs) or (br[si-1] shr (32-bs));
  ar[wrr]:=ar[wrr] xor (r0 and mrr);
  end
else if wrv>wrc then
  begin
  for k2:=wrc+1 to wrv-1 do
    begin
    si:=k2-ws;
    if bs=0 then v0:=bv[si]
    else v0:=(bv[si] shl bs) or (bv[si-1] shr (32-bs));
    av[k2]:=av[k2] xor v0;
    end;
  si:=wrv-ws;
  if bs=0 then v0:=bv[si]
  else v0:=(bv[si] shl bs) or (bv[si-1] shr (32-bs));
  av[wrv]:=av[wrv] xor (v0 and mrv);
  end;
VecNorm(ar); VecNorm(av);
end;
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
    lim:=kv1;
    if lim>hi-shift then lim:=hi-shift;
    XorShiftPair(r0^,v0^,r1^,v1^,shift,kr1,lim);
    kr0:=TopBitLE(r0^,kr0-1);
    if kv1>=0 then
      begin
      top:=kv0;
      if kv1+shift>top then top:=kv1+shift;
      if top>hi then top:=hi;
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
                  var r:TWordArray; ro,lenWords,alen,blen:longint;
                  var work:TWordArray; wo:longint);
const cut=8;
var i0,j0,lenBits,hWords,gWords,ax0,bx0,z10,rec0:longint;
var a0len,a1len,b0len,b1len,axlen,bxlen,aWords,bWords:longint;
var p0:QWord;
begin
lenBits:=lenWords shl 5;
if alen>lenBits then alen:=lenBits;
if blen>lenBits then blen:=lenBits;
if (alen<=0) or (blen<=0) then exit;
if lenWords<=cut then
  begin
  aWords:=(alen+31) shr 5;
  bWords:=(blen+31) shr 5;
  for i0:=0 to aWords-1 do if a[ao+i0]<>0 then
    for j0:=0 to bWords-1 do if b[bo+j0]<>0 then
      begin
      p0:=CLMul32(a[ao+i0],b[bo+j0]);
      r[ro+i0+j0]:=r[ro+i0+j0] xor LongWord(p0);
      r[ro+i0+j0+1]:=r[ro+i0+j0+1] xor LongWord(p0 shr 32);
      end;
  exit;
  end;
hWords:=(lenWords+1) shr 1;
gWords:=lenWords-hWords;
if alen>(hWords shl 5) then begin a0len:=hWords shl 5; a1len:=alen-(hWords shl 5); end
else begin a0len:=alen; a1len:=0; end;
if blen>(hWords shl 5) then begin b0len:=hWords shl 5; b1len:=blen-(hWords shl 5); end
else begin b0len:=blen; b1len:=0; end;
if (a1len=0) and (b1len=0) then
  begin
  KarRecW(a,ao,b,bo,r,ro,hWords,a0len,b0len,work,wo);
  exit;
  end;
KarRecW(a,ao,b,bo,r,ro,hWords,a0len,b0len,work,wo);
KarRecW(a,ao+hWords,b,bo+hWords,r,ro+(hWords shl 1),gWords,a1len,b1len,work,wo);
ax0:=wo; bx0:=wo+hWords; z10:=wo+(hWords shl 1); rec0:=wo+(hWords shl 2);
for i0:=0 to gWords-1 do
  begin
  work[ax0+i0]:=a[ao+i0] xor a[ao+hWords+i0];
  work[bx0+i0]:=b[bo+i0] xor b[bo+hWords+i0];
  end;
for i0:=gWords to hWords-1 do
  begin
  work[ax0+i0]:=a[ao+i0];
  work[bx0+i0]:=b[bo+i0];
  end;
for i0:=0 to (hWords shl 1)-1 do work[z10+i0]:=0;
axlen:=a0len; if a1len>axlen then axlen:=a1len;
bxlen:=b0len; if b1len>bxlen then bxlen:=b1len;
KarRecW(work,ax0,work,bx0,work,z10,hWords,axlen,bxlen,work,rec0);
for i0:=0 to (gWords shl 1)-1 do
  work[z10+i0]:=work[z10+i0] xor r[ro+i0] xor r[ro+(hWords shl 1)+i0];
for i0:=(gWords shl 1) to (hWords shl 1)-1 do
  work[z10+i0]:=work[z10+i0] xor r[ro+i0];
for i0:=0 to (hWords shl 1)-1 do
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor work[z10+i0];
end;

procedure KarMulFastW(const a,b:TWordArray; var r:TWordArray;
                      lenWords,alen,blen:longint);
var work:TWordArray;
var i0:longint;
begin
SetLength(r,lenWords shl 1);
for i0:=0 to High(r) do r[i0]:=0;
SetLength(work,lenWords*5);
KarRecW(a,0,b,0,r,0,lenWords,alen,blen,work,0);
end;

procedure KarRecPairW(const a:TWordArray; ao:longint;
                      const b:TWordArray; bo:longint;
                      const c:TWordArray; co:longint;
                      var r:TWordArray; ro:longint;
                      var s:TWordArray; so,lenWords,alen,blen,clen:longint;
                      var work:TWordArray; wo:longint);
const cut=8;
var i0,j0,lenBits,hWords,gWords,ax0,bx0,cx0,zr0,zs0,saver0,saves0,rec0:longint;
var a0len,a1len,b0len,b1len,c0len,c1len,axlen,bxlen,cxlen,common:longint;
var aWords,bWords,cWords:longint;
var p0:QWord;
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
  common:=bWords; if cWords<common then common:=cWords;
  for i0:=0 to aWords-1 do if a[ao+i0]<>0 then
    begin
    for j0:=0 to common-1 do
      begin
      if b[bo+j0]<>0 then
        begin
        p0:=CLMul32(a[ao+i0],b[bo+j0]);
        r[ro+i0+j0]:=r[ro+i0+j0] xor LongWord(p0);
        r[ro+i0+j0+1]:=r[ro+i0+j0+1] xor LongWord(p0 shr 32);
        end;
      if c[co+j0]<>0 then
        begin
        p0:=CLMul32(a[ao+i0],c[co+j0]);
        s[so+i0+j0]:=s[so+i0+j0] xor LongWord(p0);
        s[so+i0+j0+1]:=s[so+i0+j0+1] xor LongWord(p0 shr 32);
        end;
      end;
    for j0:=common to bWords-1 do if b[bo+j0]<>0 then
      begin
      p0:=CLMul32(a[ao+i0],b[bo+j0]);
      r[ro+i0+j0]:=r[ro+i0+j0] xor LongWord(p0);
      r[ro+i0+j0+1]:=r[ro+i0+j0+1] xor LongWord(p0 shr 32);
      end;
    for j0:=common to cWords-1 do if c[co+j0]<>0 then
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
for i0:=0 to gWords-1 do
  begin
  work[ax0+i0]:=a[ao+i0] xor a[ao+hWords+i0];
  work[bx0+i0]:=b[bo+i0] xor b[bo+hWords+i0];
  work[cx0+i0]:=c[co+i0] xor c[co+hWords+i0];
  end;
for i0:=gWords to hWords-1 do
  begin
  work[ax0+i0]:=a[ao+i0];
  work[bx0+i0]:=b[bo+i0];
  work[cx0+i0]:=c[co+i0];
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
  work[saver0+i0]:=r[ro+(hWords shl 1)+i0];
  work[saves0+i0]:=s[so+(hWords shl 1)+i0];
  end;
for i0:=(hWords shl 1)-1 downto 0 do
  begin
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor r[ro+i0];
  s[so+hWords+i0]:=s[so+hWords+i0] xor s[so+i0];
  end;
for i0:=0 to hWords-1 do
  begin
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor work[saver0+i0] xor work[zr0+i0];
  s[so+hWords+i0]:=s[so+hWords+i0] xor work[saves0+i0] xor work[zs0+i0];
  end;
for i0:=hWords to (gWords shl 1)-1 do
  begin
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor r[ro+(hWords shl 1)+i0] xor work[zr0+i0];
  s[so+hWords+i0]:=s[so+hWords+i0] xor s[so+(hWords shl 1)+i0] xor work[zs0+i0];
  end;
for i0:=(gWords shl 1) to (hWords shl 1)-1 do
  begin
  r[ro+hWords+i0]:=r[ro+hWords+i0] xor work[zr0+i0];
  s[so+hWords+i0]:=s[so+hWords+i0] xor work[zs0+i0];
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
var aa,bb,prod:TWordArray;
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
SetLength(aa,lenWords); SetLength(bb,lenWords);
for p:=0 to lenWords-1 do begin aa[p]:=vv[p]; bb[p]:=vb[p]; end;
KarMulFastW(aa,bb,prod,lenWords,dv+1,db+1);
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

function ReadDyn32Any(const a:TWordArray; bit0:longint):LongWord;
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

procedure XorDynBits4(var dst:TWordArray; dstBit:longint;
                      const src:TWordArray; srcBit,len,h:longint);
var take:longint;
var q0:LongWord;
begin
while len>0 do
  begin
  if len>32 then take:=32 else take:=len;
  q0:=ReadDyn32(src,srcBit) and LowMask32(take);
  XorDyn32(dst,dstBit,q0);
  XorDyn32(dst,dstBit+h,q0);
  XorDyn32(dst,dstBit+h*3,q0);
  XorDyn32(dst,dstBit+(h shl 2),q0);
  inc(srcBit,take); inc(dstBit,take); dec(len,take);
  end;
end;

function CoeffByte(const coeff:TVec; first,degmax:longint):LongWord; inline;
var keep:longint;
begin
if first>degmax then begin CoeffByte:=0; exit; end;
keep:=degmax-first+1;
if keep>8 then keep:=8;
CoeffByte:=((coeff[first shr 5] shr (first and 31)) and $FF) and ((LongWord(1) shl keep)-1);
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
XorDynBits4(dst,dstBit,work,workBit,childBits,h);
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
var h,g,childBits,childWords,workBit:longint;
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
h:=8;
while (h shl 1)<count do h:=h shl 1;
g:=count-h;
childBits:=(g shl 2)-1;
childWords:=(childBits+31) shr 5;
BuildUComboRecW(va,vb,first,h,degmax,mode,dst,dstBit+(g shl 1),work,workWord);
workBit:=workWord shl 5;
BuildUComboRecW(va,vb,first+h,g,degmax,mode,work,workBit,work,workWord+childWords);
XorDynBits4(dst,dstBit,work,workBit,childBits,h);
end;

procedure BuildUComboKernelFastW(const va,vb:TVec; degmax,mode:longint;
                                 var r:TWordArray; var center:longint);
var count,bits,k0:longint;
var work:TWordArray;
begin
count:=((degmax+8) div 8) shl 3;
if count<8 then count:=8;
bits:=(count shl 2)-1;
SetLength(r,(bits+31) shr 5);
for k0:=0 to High(r) do r[k0]:=0;
SetLength(work,count div 8+64);
for k0:=0 to High(work) do work[k0]:=0;
BuildUComboRecW(va,vb,0,count,degmax,mode,r,0,work,0);
center:=(count shl 1)-1;
end;

procedure AddCircularKernelW(var dst:TWordArray; const src:TWordArray; center,shift,period,limit:longint);
var src0,p0,p1,take:longint;
var q0:LongWord;
begin
src0:=center-shift;
while src0>0 do dec(src0,period);
while src0+period<=0 do inc(src0,period);
while src0<=(High(src) shl 5)+31 do
  begin
  p0:=0; if src0<0 then p0:=-src0;
  p1:=limit;
  if src0+p1>(High(src) shl 5)+31 then p1:=(High(src) shl 5)+31-src0;
  while p0<=p1 do
    begin
    take:=p1-p0+1; if take>32 then take:=32;
    q0:=ReadDyn32(src,src0+p0) and LowMask32(take);
    XorDyn32(dst,p0,q0);
    inc(p0,take);
    end;
  inc(src0,period);
  end;
end;

function DynBit(const a:TWordArray; p0:longint):LongWord; inline;
begin
DynBit:=(a[p0 shr 5] shr (p0 and 31)) and 1;
end;

{ Mode-1 action on an all-one source: interval prefix XOR replaces Karatsuba. }
procedure ApplyUComboOnesW(const va,vb:TVec; var vdst:TVec; hi,degmax:longint);
var halfLen,period,convWords,lastWord,center,keep,p,i0,w0,lo,hi0:longint;
var combo,ha,prod,prefix:TWordArray;
var bit0,q0,carry:LongWord;
begin
halfLen:=hi+2;
period:=halfLen shl 1;
convWords:=(halfLen+32) shr 5;
BuildUComboKernelFastW(va,vb,degmax,1,combo,center);
SetLength(ha,convWords);
AddCircularKernelW(ha,combo,center,0,period,halfLen);
lastWord:=halfLen shr 5;
keep:=(halfLen and 31)+1;
if keep<32 then ha[lastWord]:=ha[lastWord] and LowMask32(keep);
SetLength(prefix,convWords);
carry:=0;
for w0:=0 to lastWord do
  begin
  q0:=ha[w0];
  q0:=q0 xor (q0 shl 1);
  q0:=q0 xor (q0 shl 2);
  q0:=q0 xor (q0 shl 4);
  q0:=q0 xor (q0 shl 8);
  q0:=q0 xor (q0 shl 16);
  if carry<>0 then q0:=not q0;
  prefix[w0]:=q0;
  carry:=q0 shr 31;
  end;
if keep<32 then prefix[lastWord]:=prefix[lastWord] and LowMask32(keep);
SetLength(prod,(period shr 5)+1);
for p:=0 to period do
  begin
  lo:=p-(halfLen-1); if lo<0 then lo:=0;
  hi0:=p-1; if hi0>halfLen then hi0:=halfLen;
  if lo<=hi0 then
    begin
    bit0:=DynBit(prefix,hi0);
    if lo>0 then bit0:=bit0 xor DynBit(prefix,lo-1);
    if bit0<>0 then prod[p shr 5]:=prod[p shr 5] or (LongWord(1) shl (p and 31));
    end;
  end;
VecZero(vdst);
for i0:=0 to hi do
  begin
  p:=i0+1;
  bit0:=DynBit(prod,p) xor DynBit(prod,period-p) xor
        DynBit(prod,halfLen-p) xor DynBit(prod,halfLen+p) xor
        DynBit(ha,0) xor DynBit(ha,halfLen);
  if bit0<>0 then vdst[i0 shr 5]:=vdst[i0 shr 5] or (LongWord(1) shl (i0 and 31));
  end;
MaskDeg(vdst,hi);
end;

{ D=A*B, E=A*reverse(B); all additions below are in GF(2). }
{ C[p]=D[p]+D[2L-p]+E[L-p]+E[L+p]+A[0]B[p]+A[L]B[L-p]. }
procedure ApplyFastUComboW(const va,vb,vsrc:TVec; var vdst:TVec; hi,degmax,mode:longint);
var halfLen,period,convWords,lastWord:longint;
var w0,center,keep,srcBits,lastSrcWord,targetBit,startP:longint;
var q0,bit0:LongWord;
var combo,ha,hb,hbr,prod0,prod1:TWordArray;
begin
halfLen:=hi+2;
period:=halfLen shl 1;
convWords:=(halfLen+32) shr 5;
BuildUComboKernelFastW(va,vb,degmax,mode,combo,center);
SetLength(ha,convWords); SetLength(hb,convWords);
AddCircularKernelW(ha,combo,center,0,period,halfLen);
if mode<>0 then SetLength(hbr,convWords);
lastWord:=halfLen shr 5;
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
  if mode<>0 then
    begin
    bit0:=Reverse32(q0);
    targetBit:=srcBits-(w0 shl 5)-31;
    if targetBit>=0 then XorDyn32(hbr,targetBit,bit0)
    else if targetBit>-32 then hbr[0]:=hbr[0] xor (bit0 shr (-targetBit));
    end;
  end;
if mode=0 then
  KarMulFastW(ha,hb,prod0,convWords,halfLen+1,halfLen)
else
  KarMulPairFastW(ha,hb,hbr,prod0,prod1,convWords,
                  halfLen+1,halfLen,halfLen);
VecZero(vdst);
lastWord:=hi shr 5;
for w0:=0 to lastWord do
  begin
  startP:=(w0 shl 5)+1;
  if mode=0 then
    q0:=ReadDyn32(prod0,startP) xor
        ReadDyn32Reverse(prod0,period-startP) xor
        ReadDyn32Reverse(prod0,halfLen-startP) xor
        ReadDyn32(prod0,halfLen+startP)
  else
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
var r0,rU,jmax,target,high,w:longint;
var m2,hiS,rr,du,dv:longint;
var pg0,pg1,pg2,pt:PVec;

procedure StepHColumn(var dst:TVec; const cur,other:TVec; hi:longint);
var w0,hiw,rem0:longint;
var left0,cur0,right0,mask0:LongWord;
begin
hiw:=hi shr 5;
dst[-2]:=0; dst[-1]:=0;
left0:=cur[-1]; cur0:=cur[0];
for w0:=0 to hiw do
  begin
  right0:=cur[w0+1];
  dst[w0]:=(cur0 shl 1) xor (left0 shr 31) xor
           (cur0 shr 1) xor (right0 shl 31) xor other[w0];
  left0:=cur0; cur0:=right0;
  end;
rem0:=hi and 31;
if rem0=31 then mask0:=$FFFFFFFF else mask0:=(LongWord(1) shl (rem0+1))-1;
dst[hiw]:=dst[hiw] and mask0;
if hiw+1<=mw then dst[hiw+1]:=0;
if hiw+2<=mw then dst[hiw+2]:=0;
end;

procedure DivMonicBlock(var rem:TVec; const divisor:TVec;
                        var quotient:TVec; top,d:longint);
var dq,count,k0,s0,p0,sWord:longint;
var drev,iv,rword,rrev,qrev,qblock,mask0:LongWord;
var z0:QWord;
begin
VecZero(quotient);
drev:=ReverseWord32(ReadVec32Any(divisor,d-31));
iv:=1;
for k0:=1 to 31 do
  begin
  mask0:=LongWord(1) shl k0;
  if (LongWord(CLMul32(drev,iv)) and mask0)<>0 then iv:=iv or mask0;
  end;
dq:=top-d;
while dq>=0 do
  begin
  count:=dq+1; k0:=count and 31; if k0=0 then k0:=32; s0:=count-k0;
  if k0=32 then mask0:=$FFFFFFFF else mask0:=(LongWord(1) shl k0)-1;
  rword:=ReadVec32Any(rem,d+s0) and mask0;
  rrev:=ReverseWord32(rword) shr (32-k0);
  qrev:=LongWord(CLMul32(rrev,iv)) and mask0;
  qblock:=ReverseWord32(qrev) shr (32-k0);
  sWord:=s0 shr 5;
  quotient[sWord]:=qblock;
  for p0:=0 to (d shr 5) do
    begin
    z0:=CLMul32(divisor[p0],qblock);
    rem[sWord+p0]:=rem[sWord+p0] xor LongWord(z0);
    rem[sWord+p0+1]:=rem[sWord+p0+1] xor LongWord(z0 shr 32);
    end;
  dq:=s0-1;
  end;
end;

begin
TimeMark('c');
TimeMark('q');
if (n and 1)=0 then
  begin
  m2:=longint(n div 2);
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
pg1:=@g0; pg2:=@g1; pg0:=@g2;
VecZero(pg2^); VecZero(pg0^);
VecZero(x); VecNorm(x);
jmax:=longint(n)-r0-1;
if jmax>=0 then
  begin
  target:=r0;
  if target>jmax+1 then target:=jmax+1;
  for j:=1 to target do
    begin
    high:=r0+j; if high>longint(n)-1 then high:=longint(n)-1;
    StepHColumn(pg0^,pg1^,pg2^,high);
    pt:=pg0; pg0:=pg2; pg2:=pg1; pg1:=pt;
    end;

  if jmax>=r0 then
    begin
    DivMonicBlock(z,pg1^,v,longint(n)-1,r0 shl 1);
    for w:=0 to wn-1 do x[w]:=ReadVec32Any(v,(w shl 5)-r0);
    VecNorm(x);
    end;

  j:=r0-1; if j>jmax then j:=jmax;
  while j>=0 do
    begin
    i:=j+r0;
    if ((z[i shr 5] shr (i and 31)) and 1)<>0 then
      begin
      VecXorRange(z,pg2^,0,i);
      x[j shr 5]:=x[j shr 5] or (LongWord(1) shl (j and 31));
      end;
    if j>0 then
      begin
      high:=i-1;
      StepHColumn(pg0^,pg2^,pg1^,high);
      pt:=pg0; pg0:=pg1; pg1:=pg2; pg2:=pt;
      end;
    dec(j);
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
