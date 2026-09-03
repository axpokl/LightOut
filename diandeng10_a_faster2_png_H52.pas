//{$define disp}
program diandeng;

{$mode objfpc}{$H+}

{ H52: pair the equal-shift Euclid row updates and accelerate degree lookup. }
{ A and B use the same Euclid and Bezout algorithm without size branching. }

{$ifdef disp}
uses Windows, display;
const m=1000;
{$else}
uses Windows;
const m=100000;
{$endif}

type TVec=array[-2..m]of boolean;
     PVec=^TVec;

var n:longword;
var i,j:longint;
var x,y,y1,y_,y_1,f,f1,c,c1:TVec;
var hf,hf1,hc,hc1:TVec;
var k:longint;
var hk:longint;
var o,ho:boolean;
var uKernel8:array[0..255,0..28] of boolean;
var perfFreq,lastCounter:Int64;
var hasLastCounter:boolean;

{$ifdef disp}
var bb:pbitbuf;
var bp:pbitmap;
{$endif}

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

procedure VecZeroHi(var a:TVec;hi:longint);
var k2:longint;
begin
if hi<-2 then hi:=-2;
for k2:=-2 to hi do a[k2]:=false;
end;

procedure VecCopyHi(var a:TVec; const b:TVec; hi:longint);
var k2:longint;
begin
if hi<-2 then hi:=-2;
for k2:=-2 to hi do a[k2]:=b[k2];
end;

function PolyDeg(const a:TVec;hi:longint):longint;
begin
while (hi>=0) and not(a[hi]) do dec(hi);
PolyDeg:=hi;
end;

procedure XorI(var dst:TVec; const src:TVec; hi:longint); inline;
var k2,k4:longint;
begin
k2:=0;
k4:=hi-3;
while k2<=k4 do
  begin
  dst[k2]:=dst[k2] xor src[k2];
  dst[k2+1]:=dst[k2+1] xor src[k2+1];
  dst[k2+2]:=dst[k2+2] xor src[k2+2];
  dst[k2+3]:=dst[k2+3] xor src[k2+3];
  inc(k2,4);
  end;
while k2<=hi do
  begin
  dst[k2]:=dst[k2] xor src[k2];
  inc(k2);
  end;
end;

procedure XorH(var dst:TVec; const src:TVec; hi:longint); inline;
var k2,k4:longint;
begin
k2:=0;
k4:=hi-3;
while k2<=k4 do
  begin
  dst[k2]:=dst[k2] xor src[k2-1] xor src[k2+1];
  dst[k2+1]:=dst[k2+1] xor src[k2] xor src[k2+2];
  dst[k2+2]:=dst[k2+2] xor src[k2+1] xor src[k2+3];
  dst[k2+3]:=dst[k2+3] xor src[k2+2] xor src[k2+4];
  inc(k2,4);
  end;
while k2<=hi do
  begin
  dst[k2]:=dst[k2] xor src[k2-1] xor src[k2+1];
  inc(k2);
  end;
end;

procedure XorIH(var dst:TVec; const src:TVec; hi:longint); inline;
var k2,k4:longint;
begin
k2:=0;
k4:=hi-3;
while k2<=k4 do
  begin
  dst[k2]:=dst[k2] xor src[k2] xor src[k2-1] xor src[k2+1];
  dst[k2+1]:=dst[k2+1] xor src[k2+1] xor src[k2] xor src[k2+2];
  dst[k2+2]:=dst[k2+2] xor src[k2+2] xor src[k2+1] xor src[k2+3];
  dst[k2+3]:=dst[k2+3] xor src[k2+3] xor src[k2+2] xor src[k2+4];
  inc(k2,4);
  end;
while k2<=hi do
  begin
  dst[k2]:=dst[k2] xor src[k2] xor src[k2-1] xor src[k2+1];
  inc(k2);
  end;
end;

procedure AdvanceU(const src:TVec; var dst:TVec; hi:longint); inline;
var k2,k4:longint;
begin
if hi=0 then
  dst[0]:=false
else
  begin
  dst[0]:=src[0] xor src[1];
  if hi>=2 then dst[0]:=dst[0] xor src[2];
  k2:=1;
  k4:=hi-4;
  while k2<=k4 do
    begin
    dst[k2]:=src[k2-2] xor src[k2-1] xor src[k2+1] xor src[k2+2];
    dst[k2+1]:=src[k2-1] xor src[k2] xor src[k2+2] xor src[k2+3];
    dst[k2+2]:=src[k2] xor src[k2+1] xor src[k2+3] xor src[k2+4];
    dst[k2+3]:=src[k2+1] xor src[k2+2] xor src[k2+4] xor src[k2+5];
    inc(k2,4);
    end;
  while k2<=hi-1 do
    begin
    dst[k2]:=src[k2-2] xor src[k2-1] xor src[k2+1] xor src[k2+2];
    inc(k2);
    end;
  dst[hi]:=src[hi] xor src[hi-1];
  if hi>=2 then dst[hi]:=dst[hi] xor src[hi-2];
  end;
end;


procedure AdvanceUXorI(const src:TVec; var dst,next:TVec; hi:longint); inline;
var k2,k4:longint;
begin
if hi=0 then
  begin
  dst[0]:=dst[0] xor src[0];
  next[0]:=false;
  end
else
  begin
  dst[0]:=dst[0] xor src[0];
  next[0]:=src[0] xor src[1];
  if hi>=2 then next[0]:=next[0] xor src[2];
  k2:=1;
  k4:=hi-4;
  while k2<=k4 do
    begin
    dst[k2]:=dst[k2] xor src[k2];
    next[k2]:=src[k2-2] xor src[k2-1] xor src[k2+1] xor src[k2+2];
    dst[k2+1]:=dst[k2+1] xor src[k2+1];
    next[k2+1]:=src[k2-1] xor src[k2] xor src[k2+2] xor src[k2+3];
    dst[k2+2]:=dst[k2+2] xor src[k2+2];
    next[k2+2]:=src[k2] xor src[k2+1] xor src[k2+3] xor src[k2+4];
    dst[k2+3]:=dst[k2+3] xor src[k2+3];
    next[k2+3]:=src[k2+1] xor src[k2+2] xor src[k2+4] xor src[k2+5];
    inc(k2,4);
    end;
  while k2<=hi-1 do
    begin
    dst[k2]:=dst[k2] xor src[k2];
    next[k2]:=src[k2-2] xor src[k2-1] xor src[k2+1] xor src[k2+2];
    inc(k2);
    end;
  dst[hi]:=dst[hi] xor src[hi];
  next[hi]:=src[hi] xor src[hi-1];
  if hi>=2 then next[hi]:=next[hi] xor src[hi-2];
  end;
end;

procedure AdvanceUXorH(const src:TVec; var dst,next:TVec; hi:longint); inline;
var k2,k4:longint;
var h:boolean;
begin
if hi=0 then
  next[0]:=false
else
  begin
  h:=src[1];
  dst[0]:=dst[0] xor h;
  next[0]:=src[0] xor h;
  if hi>=2 then next[0]:=next[0] xor src[2];
  k2:=1;
  k4:=hi-4;
  while k2<=k4 do
    begin
    h:=src[k2-1] xor src[k2+1];
    dst[k2]:=dst[k2] xor h;
    next[k2]:=h xor src[k2-2] xor src[k2+2];
    h:=src[k2] xor src[k2+2];
    dst[k2+1]:=dst[k2+1] xor h;
    next[k2+1]:=h xor src[k2-1] xor src[k2+3];
    h:=src[k2+1] xor src[k2+3];
    dst[k2+2]:=dst[k2+2] xor h;
    next[k2+2]:=h xor src[k2] xor src[k2+4];
    h:=src[k2+2] xor src[k2+4];
    dst[k2+3]:=dst[k2+3] xor h;
    next[k2+3]:=h xor src[k2+1] xor src[k2+5];
    inc(k2,4);
    end;
  while k2<=hi-1 do
    begin
    h:=src[k2-1] xor src[k2+1];
    dst[k2]:=dst[k2] xor h;
    next[k2]:=h xor src[k2-2] xor src[k2+2];
    inc(k2);
    end;
  h:=src[hi-1];
  dst[hi]:=dst[hi] xor h;
  next[hi]:=src[hi] xor h;
  if hi>=2 then next[hi]:=next[hi] xor src[hi-2];
  end;
end;

procedure AdvanceUXorIH(const src:TVec; var dst,next:TVec; hi:longint); inline;
var k2,k4:longint;
var h:boolean;
begin
if hi=0 then
  begin
  dst[0]:=dst[0] xor src[0];
  next[0]:=false;
  end
else
  begin
  h:=src[1];
  dst[0]:=dst[0] xor src[0] xor h;
  next[0]:=src[0] xor h;
  if hi>=2 then next[0]:=next[0] xor src[2];
  k2:=1;
  k4:=hi-4;
  while k2<=k4 do
    begin
    h:=src[k2-1] xor src[k2+1];
    dst[k2]:=dst[k2] xor src[k2] xor h;
    next[k2]:=h xor src[k2-2] xor src[k2+2];
    h:=src[k2] xor src[k2+2];
    dst[k2+1]:=dst[k2+1] xor src[k2+1] xor h;
    next[k2+1]:=h xor src[k2-1] xor src[k2+3];
    h:=src[k2+1] xor src[k2+3];
    dst[k2+2]:=dst[k2+2] xor src[k2+2] xor h;
    next[k2+2]:=h xor src[k2] xor src[k2+4];
    h:=src[k2+2] xor src[k2+4];
    dst[k2+3]:=dst[k2+3] xor src[k2+3] xor h;
    next[k2+3]:=h xor src[k2+1] xor src[k2+5];
    inc(k2,4);
    end;
  while k2<=hi-1 do
    begin
    h:=src[k2-1] xor src[k2+1];
    dst[k2]:=dst[k2] xor src[k2] xor h;
    next[k2]:=h xor src[k2-2] xor src[k2+2];
    inc(k2);
    end;
  h:=src[hi-1];
  dst[hi]:=dst[hi] xor src[hi] xor h;
  next[hi]:=src[hi] xor h;
  if hi>=2 then next[hi]:=next[hi] xor src[hi-2];
  end;
end;

procedure ApplyPoly(const va,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var k2,d,j2,l,r,l2,r2:longint;
begin
for k2:=-2 to hi+1 do begin cur0[k2]:=false; cur1[k2]:=false; vdst[k2]:=false; end;
for k2:=0 to hi do cur0[k2]:=vsrc[k2];
cur0[-1]:=false;
cur0[hi+1]:=false;
d:=PolyDeg(va,degmax);
if d<0 then exit;
l:=0; while (l<=hi) and not(cur0[l]) do inc(l);
if l>hi then exit;
r:=hi; while (r>=l) and not(cur0[r]) do dec(r);
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  if va[j2] then for k2:=l to r do vdst[k2]:=vdst[k2] xor pcur^[k2];
  if j2>=d then break;
  l2:=l-1; if l2<0 then l2:=0;
  r2:=r+1; if r2>hi then r2:=hi;
  pcur^[l-2]:=false;
  pcur^[l-1]:=false;
  pcur^[r+1]:=false;
  if r+2<=hi+1 then pcur^[r+2]:=false;
  for k2:=l2 to r2 do pnxt^[k2]:=pcur^[k2-1] xor pcur^[k2+1];
  while (l2<=r2) and not(pnxt^[l2]) do inc(l2);
  if l2>r2 then break;
  while not(pnxt^[r2]) do dec(r2);
  pnxt^[l2-2]:=false;
  pnxt^[l2-1]:=false;
  pnxt^[r2+1]:=false;
  if r2+2<=hi+1 then pnxt^[r2+2]:=false;
  pt:=pcur;
  pcur:=pnxt;
  pnxt:=pt;
  l:=l2;
  r:=r2;
  end;
end;

procedure BuildYFast(var dy_,dy:TVec; const sy_,sy_1,sy,sy1:TVec; deg:longint); inline;
var ii,half:longint;
begin
dy_[-2]:=false; dy_[-1]:=false; dy[-2]:=false; dy[-1]:=false;
for ii:=0 to deg-1 do
  dy_[ii]:=sy_[ii-1] xor sy_[ii] xor sy_[ii+1] xor sy_1[ii];
dy_[deg]:=sy_[deg-1] xor sy_[deg];
half:=deg div 2;
for ii:=0 to half do
  begin
  dy[ii]:=not(sy[ii-2] xor sy[ii-1] xor sy[ii] xor sy1[ii-2] xor
              dy_[ii] xor sy_1[ii-1]);
  end;
if half+1<=deg then dy[half+1]:=dy[deg-half-1];
dy_[deg+1]:=false;
dy[deg+1]:=false;
end;

procedure ExpandPalindrome(var a:TVec; deg:longint);
var ii:longint;
begin
if deg<0 then exit;
for ii:=(deg div 2)+1 to deg do a[ii]:=a[deg-ii];
a[deg+1]:=false;
end;

procedure BuildFCFast(var nf,nc:TVec; const oldf,oldf1,oldc,oldc1:TVec; hi:longint); inline;
var ii:longint;
begin
nf[-2]:=false; nf[-1]:=false; nc[-2]:=false; nc[-1]:=false;
for ii:=0 to hi do
  begin
  if ii=0 then nf[ii]:=oldf1[ii] else nf[ii]:=oldc[ii-1] xor oldf1[ii];
  nc[ii]:=oldf[ii] xor oldc[ii] xor oldc1[ii];
  end;
nf[hi+1]:=false;
nc[hi+1]:=false;
end;

procedure MakeMat();
var y2,y_2,f2,c2:TVec;
var py,py1,py_,py_1,py2,py_2,pf,pf1,pf2,pc,pc1,pc2,pt:PVec;
var hiu:longint;
begin
TimeMark('m');
if (not o) or (longint(n)<k) then
  begin
  VecZeroHi(y1,longint(n)); VecZeroHi(y,longint(n)); VecZeroHi(y_1,longint(n)); VecZeroHi(y_,longint(n));
  VecZeroHi(f1,longint(n)); VecZeroHi(f,longint(n));
  VecZeroHi(c1,longint(n)); VecZeroHi(c,longint(n));
  f[0]:=true;
  k:=0; o:=true; ho:=false;
  end;
py1:=@y1; py:=@y; py_1:=@y_1; py_:=@y_; py2:=@y2; py_2:=@y_2;
pf1:=@f1; pf:=@f; pf2:=@f2; pc1:=@c1; pc:=@c; pc2:=@c2;
for j:=k+1 to n do
  begin
  BuildYFast(py_2^,py2^,py_^,py_1^,py^,py1^,j-1);
  py_2^[0]:=py2^[0];
  py_2^[-2]:=true;
  if j=1 then
    begin
    pf2^[-2]:=false; pf2^[-1]:=false; pf2^[0]:=false; pf2^[1]:=false;
    pc2^[-2]:=false; pc2^[-1]:=false; pc2^[0]:=true; pc2^[1]:=false;
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
    VecCopyHi(hf,pf^,j div 2);
    VecCopyHi(hc,pc^,j div 2);
    VecCopyHi(hf1,pf1^,j div 2);
    VecCopyHi(hc1,pc1^,j div 2);
    hk:=j;
    ho:=true;
    end;
  end;
ExpandPalindrome(py^,longint(n)-1);
ExpandPalindrome(py1^,longint(n)-2);
VecCopyHi(y1,py1^,longint(n)); VecCopyHi(y,py^,longint(n));
VecCopyHi(y_1,py_1^,longint(n)); VecCopyHi(y_,py_^,longint(n));
VecCopyHi(f1,pf1^,longint(n div 2)); VecCopyHi(f,pf^,longint(n div 2));
VecCopyHi(c1,pc1^,longint(n div 2)); VecCopyHi(c,pc^,longint(n div 2));
k:=n;
end;

procedure EnsureAB(nn:longword);
var jj,hiu:longint;
var tf,tc:TVec;
begin
if (not ho) or (longint(nn)<hk) then
  begin
  VecZeroHi(hf,longint(nn div 2)); VecZeroHi(hc,longint(nn div 2));
  VecZeroHi(hf1,longint(nn div 2)); VecZeroHi(hc1,longint(nn div 2));
  hf[0]:=true;
  hk:=0; ho:=true;
  end;
for jj:=hk+1 to nn do
  begin
  if jj=1 then
    begin
    tf[-2]:=false; tf[-1]:=false; tf[0]:=false; tf[1]:=false;
    tc[-2]:=false; tc[-1]:=false; tc[0]:=true; tc[1]:=false;
    end
  else
    begin
    hiu:=jj div 2;
    BuildFCFast(tf,tc,hf,hf1,hc,hc1,hiu);
    end;
  VecCopyHi(hf1,hf,jj div 2);
  VecCopyHi(hc1,hc,jj div 2);
  VecCopyHi(hf,tf,jj div 2);
  VecCopyHi(hc,tc,jj div 2);
  end;
hk:=nn;
end;

procedure RecoverBezoutU(const va,vb,vg,vv:TVec; var vu:TVec; hi:longint); forward;

function GcdU(const va,vb:TVec; var vg,vu,vv:TVec; hi:longint):longint;
var r0a,r1a,v0a,v1a:TVec;
var r0,r1,v0,v1,tt:PVec;
var kr0,kr1,kv0,kv1,shift,p,top,lim:longint;

procedure XorShiftPair(var ar,av:TVec; const br,bv:TVec;
                       sh,dr,dv:longint);
var p0,common:longint;
begin
common:=dr; if dv<common then common:=dv;
for p0:=0 to common do
  begin
  if br[p0] then ar[p0+sh]:=not ar[p0+sh];
  if bv[p0] then av[p0+sh]:=not av[p0+sh];
  end;
if dr>common then
  begin
  for p0:=common+1 to dr do if br[p0] then ar[p0+sh]:=not ar[p0+sh];
  end
else if dv>common then
  begin
  for p0:=common+1 to dv do if bv[p0] then av[p0+sh]:=not av[p0+sh];
  end;
end;
begin
r0:=@r0a; r1:=@r1a; v0:=@v0a; v1:=@v1a;
for p:=0 to hi do
  begin
  r0^[p]:=va[p]; r1^[p]:=vb[p];
  v0^[p]:=false; v1^[p]:=false;
  end;
v1^[0]:=true;
kr0:=PolyDeg(r0^,hi);
kr1:=PolyDeg(r1^,hi);
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
    VecCopyHi(vg,r0^,hi);
    VecCopyHi(vv,v0^,hi);
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
    top:=kr0-1;
    while (top>=0) and not(r0^[top]) do dec(top);
    kr0:=top;
    if kv1>=0 then
      begin
      top:=kv0;
      if kv1+shift>top then top:=kv1+shift;
      if top>hi then top:=hi;
      while (top>=0) and not(v0^[top]) do dec(top);
      kv0:=top;
      end;
    end;
  end;
end;

type TDynBool=array of boolean;

procedure KarRec(const a:TDynBool; ao:longint; const b:TDynBool; bo:longint;
                 var r:TDynBool; ro,lenWords,alen,blen:longint;
                 var work:TDynBool; wo:longint);
const cut=8;
var i0,j0,lenBits,hWords,gWords,h,g,ax0,bx0,z10,rec0:longint;
var a0len,a1len,b0len,b1len,axlen,bxlen:longint;
begin
lenBits:=lenWords shl 5;
if alen>lenBits then alen:=lenBits;
if blen>lenBits then blen:=lenBits;
if (alen<=0) or (blen<=0) then exit;
if lenWords<=cut then
  begin
  for i0:=0 to alen-1 do if a[ao+i0] then
    for j0:=0 to blen-1 do if b[bo+j0] then
      r[ro+i0+j0]:=not r[ro+i0+j0];
  exit;
  end;
hWords:=(lenWords+1) shr 1;
gWords:=lenWords-hWords;
h:=hWords shl 5;
g:=gWords shl 5;
if alen>h then begin a0len:=h; a1len:=alen-h; end
else begin a0len:=alen; a1len:=0; end;
if blen>h then begin b0len:=h; b1len:=blen-h; end
else begin b0len:=blen; b1len:=0; end;
if (a1len=0) and (b1len=0) then
  begin
  KarRec(a,ao,b,bo,r,ro,hWords,a0len,b0len,work,wo);
  exit;
  end;
KarRec(a,ao,b,bo,r,ro,hWords,a0len,b0len,work,wo);
KarRec(a,ao+h,b,bo+h,r,ro+(h shl 1),gWords,a1len,b1len,work,wo);
ax0:=wo; bx0:=wo+h; z10:=wo+(h shl 1); rec0:=wo+(h shl 2);
for i0:=0 to h-1 do
  begin
  work[ax0+i0]:=a[ao+i0];
  work[bx0+i0]:=b[bo+i0];
  if i0<g then
    begin
    work[ax0+i0]:=work[ax0+i0] xor a[ao+h+i0];
    work[bx0+i0]:=work[bx0+i0] xor b[bo+h+i0];
    end;
  end;
for i0:=0 to (h shl 1)-1 do work[z10+i0]:=false;
axlen:=a0len; if a1len>axlen then axlen:=a1len;
bxlen:=b0len; if b1len>bxlen then bxlen:=b1len;
KarRec(work,ax0,work,bx0,work,z10,hWords,axlen,bxlen,work,rec0);
for i0:=0 to (g shl 1)-1 do
  work[z10+i0]:=work[z10+i0] xor r[ro+i0] xor r[ro+(h shl 1)+i0];
for i0:=(g shl 1) to (h shl 1)-1 do
  work[z10+i0]:=work[z10+i0] xor r[ro+i0];
for i0:=0 to (h shl 1)-1 do
  r[ro+h+i0]:=r[ro+h+i0] xor work[z10+i0];
end;

procedure KarMul(const a,b:TDynBool; var r:TDynBool;
                 lenWords,alen,blen:longint);
var work:TDynBool;
var i0,lenBits:longint;
begin
lenBits:=lenWords shl 5;
SetLength(r,lenBits shl 1);
for i0:=0 to High(r) do r[i0]:=false;
SetLength(work,lenBits*5);
KarRec(a,0,b,0,r,0,lenWords,alen,blen,work,0);
end;

procedure KarRecPair(const a:TDynBool; ao:longint;
                     const b:TDynBool; bo:longint;
                     const c:TDynBool; co:longint;
                     var r:TDynBool; ro:longint;
                     var s:TDynBool; so,lenWords,alen,blen,clen:longint;
                     var work:TDynBool; wo:longint);
const cut=8;
var i0,j0,lenBits,hWords,gWords,h,g,ax0,bx0,cx0,zr0,zs0,saver0,saves0,rec0:longint;
var a0len,a1len,b0len,b1len,c0len,c1len,axlen,bxlen,cxlen,maxbc:longint;
var tr,ts:boolean;
begin
lenBits:=lenWords shl 5;
if alen>lenBits then alen:=lenBits;
if blen>lenBits then blen:=lenBits;
if clen>lenBits then clen:=lenBits;
if (alen<=0) or ((blen<=0) and (clen<=0)) then exit;
if lenWords<=cut then
  begin
  maxbc:=blen; if clen>maxbc then maxbc:=clen;
  for i0:=0 to alen-1 do if a[ao+i0] then
    for j0:=0 to maxbc-1 do
      begin
      if (j0<blen) and b[bo+j0] then r[ro+i0+j0]:=not r[ro+i0+j0];
      if (j0<clen) and c[co+j0] then s[so+i0+j0]:=not s[so+i0+j0];
      end;
  exit;
  end;
hWords:=(lenWords+1) shr 1;
gWords:=lenWords-hWords;
h:=hWords shl 5;
g:=gWords shl 5;
if alen>h then begin a0len:=h; a1len:=alen-h; end
else begin a0len:=alen; a1len:=0; end;
if blen>h then begin b0len:=h; b1len:=blen-h; end
else begin b0len:=blen; b1len:=0; end;
if clen>h then begin c0len:=h; c1len:=clen-h; end
else begin c0len:=clen; c1len:=0; end;
if (a1len=0) and (b1len=0) and (c1len=0) then
  begin
  KarRecPair(a,ao,b,bo,c,co,r,ro,s,so,hWords,a0len,b0len,c0len,work,wo);
  exit;
  end;
KarRecPair(a,ao,b,bo,c,co,r,ro,s,so,hWords,a0len,b0len,c0len,work,wo);
KarRecPair(a,ao+h,b,bo+h,c,co+h,r,ro+(h shl 1),s,so+(h shl 1),gWords,
           a1len,b1len,c1len,work,wo);
ax0:=wo; bx0:=wo+h; cx0:=wo+(h shl 1);
zr0:=wo+h*3; zs0:=wo+h*5;
saver0:=wo+h*7; saves0:=wo+h*8; rec0:=wo+h*9;
for i0:=0 to h-1 do
  begin
  work[ax0+i0]:=a[ao+i0];
  work[bx0+i0]:=b[bo+i0];
  work[cx0+i0]:=c[co+i0];
  if i0<g then
    begin
    work[ax0+i0]:=work[ax0+i0] xor a[ao+h+i0];
    work[bx0+i0]:=work[bx0+i0] xor b[bo+h+i0];
    work[cx0+i0]:=work[cx0+i0] xor c[co+h+i0];
    end;
  end;
for i0:=0 to (h shl 1)-1 do
  begin
  work[zr0+i0]:=false;
  work[zs0+i0]:=false;
  end;
axlen:=a0len; if a1len>axlen then axlen:=a1len;
bxlen:=b0len; if b1len>bxlen then bxlen:=b1len;
cxlen:=c0len; if c1len>cxlen then cxlen:=c1len;
KarRecPair(work,ax0,work,bx0,work,cx0,
           work,zr0,work,zs0,hWords,axlen,bxlen,cxlen,work,rec0);
for i0:=0 to h-1 do
  begin
  if i0<(g shl 1) then
    begin
    work[saver0+i0]:=r[ro+(h shl 1)+i0];
    work[saves0+i0]:=s[so+(h shl 1)+i0];
    end
  else
    begin
    work[saver0+i0]:=false;
    work[saves0+i0]:=false;
    end;
  end;
for i0:=(h shl 1)-1 downto 0 do
  begin
  r[ro+h+i0]:=r[ro+h+i0] xor r[ro+i0];
  s[so+h+i0]:=s[so+h+i0] xor s[so+i0];
  end;
for i0:=0 to (h shl 1)-1 do
  begin
  if i0<h then
    begin
    tr:=work[saver0+i0];
    ts:=work[saves0+i0];
    end
  else if i0<(g shl 1) then
    begin
    tr:=r[ro+(h shl 1)+i0];
    ts:=s[so+(h shl 1)+i0];
    end
  else
    begin
    tr:=false;
    ts:=false;
    end;
  r[ro+h+i0]:=r[ro+h+i0] xor tr xor work[zr0+i0];
  s[so+h+i0]:=s[so+h+i0] xor ts xor work[zs0+i0];
  end;
end;

procedure KarMulPair(const a,b,c:TDynBool; var r,s:TDynBool;
                     lenWords,alen,blen,clen:longint);
var work:TDynBool;
var i0,lenBits:longint;
begin
lenBits:=lenWords shl 5;
SetLength(r,lenBits shl 1);
SetLength(s,lenBits shl 1);
for i0:=0 to High(r) do
  begin
  r[i0]:=false;
  s[i0]:=false;
  end;
SetLength(work,lenBits*10);
KarRecPair(a,0,b,0,c,0,r,0,s,0,lenWords,alen,blen,clen,work,0);
end;

{ vg=vu*va+vv*vb, hence vu=(vg+vv*vb)/va. }
{ A and B use the same 32-coefficient reciprocal-block exact division. }
procedure RecoverBezoutU(const va,vb,vg,vv:TVec; var vu:TVec; hi:longint);
type TBool32=array[0..31] of boolean;
var aa,bb,empty,prod,dummy:TDynBool;
var drev,iv,rrev,qrev,qblock:TBool32;
var lenWords,lenBits,da,db,dv,top,dq,count,k,s,p,i0,j0:longint;
begin
da:=PolyDeg(va,hi);
db:=PolyDeg(vb,hi);
dv:=PolyDeg(vv,hi);
VecZeroHi(vu,hi);
if da<0 then exit;
lenWords:=(hi+32) shr 5;
lenBits:=lenWords shl 5;
SetLength(aa,lenBits); SetLength(bb,lenBits); SetLength(empty,lenBits);
for p:=0 to dv do aa[p]:=vv[p];
for p:=0 to db do bb[p]:=vb[p];
KarMulPair(aa,bb,empty,prod,dummy,lenWords,dv+1,db+1,0);
for p:=0 to PolyDeg(vg,hi) do if vg[p] then prod[p]:=not prod[p];
top:=High(prod);
while (top>=0) and not(prod[top]) do dec(top);
for i0:=0 to 31 do begin drev[i0]:=false; iv[i0]:=false; end;
for i0:=0 to 31 do if da-i0>=0 then drev[i0]:=va[da-i0];
iv[0]:=true;
for i0:=1 to 31 do
  begin
  for j0:=1 to i0 do if drev[j0] and iv[i0-j0] then iv[i0]:=not iv[i0];
  end;
dq:=top-da;
while dq>=0 do
  begin
  count:=dq+1; k:=count and 31; if k=0 then k:=32; s:=count-k;
  for i0:=0 to 31 do begin rrev[i0]:=false; qrev[i0]:=false; qblock[i0]:=false; end;
  for i0:=0 to k-1 do rrev[i0]:=prod[da+s+k-1-i0];
  for i0:=0 to k-1 do
    for j0:=0 to i0 do if rrev[j0] and iv[i0-j0] then qrev[i0]:=not qrev[i0];
  for i0:=0 to k-1 do
    begin
    qblock[i0]:=qrev[k-1-i0];
    vu[s+i0]:=qblock[i0];
    end;
  for i0:=0 to k-1 do if qblock[i0] then
    for p:=0 to da do if va[p] then prod[s+i0+p]:=not prod[s+i0+p];
  dq:=s-1;
  end;
end;
procedure BuildUKernel(const coeff:TVec; first,count,degmax:longint; var r:TDynBool);
var h,i0,center,subcenter:longint;
var lo,hi:TDynBool;

procedure ToggleShift(shift:longint);
var p:longint;
begin
for p:=0 to High(hi) do if hi[p] then
  r[center+(p-subcenter)+shift]:=not r[center+(p-subcenter)+shift];
end;

begin
if count=1 then
  begin
  SetLength(r,1);
  if first<=degmax then r[0]:=coeff[first];
  exit;
  end;
h:=count shr 1;
BuildUKernel(coeff,first,h,degmax,lo);
BuildUKernel(coeff,first+h,h,degmax,hi);
SetLength(r,(count shl 2)-3);
center:=(count shl 1)-2;
subcenter:=(h shl 1)-2;
for i0:=0 to High(lo) do if lo[i0] then r[center+(i0-subcenter)]:=true;
ToggleShift(-(h shl 1));
ToggleShift(-h);
ToggleShift(h);
ToggleShift(h shl 1);
end;

procedure InitUKernel8;
var a0,j0,p0:longint;
var basis,nextBasis:array[0..28] of boolean;
begin
for a0:=0 to 255 do
  begin
  for p0:=0 to 28 do
    begin
    uKernel8[a0,p0]:=false;
    basis[p0]:=false;
    end;
  basis[14]:=true;
  for j0:=0 to 7 do
    begin
    if ((a0 shr j0) and 1)<>0 then
      for p0:=0 to 28 do if basis[p0] then
        uKernel8[a0,p0]:=not uKernel8[a0,p0];
    if j0<7 then
      begin
      for p0:=0 to 28 do nextBasis[p0]:=false;
      for p0:=0 to 28 do if basis[p0] then
        begin
        if p0>=2 then nextBasis[p0-2]:=not nextBasis[p0-2];
        if p0>=1 then nextBasis[p0-1]:=not nextBasis[p0-1];
        if p0<=27 then nextBasis[p0+1]:=not nextBasis[p0+1];
        if p0<=26 then nextBasis[p0+2]:=not nextBasis[p0+2];
        end;
      for p0:=0 to 28 do basis[p0]:=nextBasis[p0];
      end;
    end;
  end;
end;

procedure ClearBoolRange(var a:TDynBool; p0,len:longint); inline;
var k0:longint;
begin
for k0:=p0 to p0+len-1 do a[k0]:=false;
end;

procedure XorBoolRange(var dst:TDynBool; dst0:longint;
                       const src:TDynBool; src0,len:longint); inline;
var k0:longint;
begin
for k0:=0 to len-1 do if src[src0+k0] then dst[dst0+k0]:=not dst[dst0+k0];
end;

procedure BuildUKernelRecFast(const coeff:TVec; first,count,degmax:longint;
                              var dst:TDynBool; dst0:longint;
                              var work:TDynBool; work0:longint);
var h,childBits,j0,p0,a0:longint;
begin
ClearBoolRange(dst,dst0,(count shl 2)-3);
if count=8 then
  begin
  a0:=0;
  for j0:=0 to 7 do if (first+j0<=degmax) and coeff[first+j0] then
    a0:=a0 or (1 shl j0);
  for p0:=0 to 28 do if uKernel8[a0,p0] then
    dst[dst0+p0]:=not dst[dst0+p0];
  exit;
  end;
h:=count shr 1;
childBits:=(h shl 2)-3;
BuildUKernelRecFast(coeff,first,h,degmax,dst,dst0+(h shl 1),work,work0);
BuildUKernelRecFast(coeff,first+h,h,degmax,work,work0,work,work0+childBits);
XorBoolRange(dst,dst0,work,work0,childBits);
XorBoolRange(dst,dst0+h,work,work0,childBits);
XorBoolRange(dst,dst0+h*3,work,work0,childBits);
XorBoolRange(dst,dst0+(h shl 2),work,work0,childBits);
end;

procedure BuildUKernelFast(const coeff:TVec; degmax:longint;
                           var r:TDynBool; var center:longint);
var count,bits:longint;
var work:TDynBool;
begin
count:=8;
while count<=degmax do count:=count shl 1;
bits:=(count shl 2)-3;
SetLength(r,bits);
SetLength(work,count shl 2);
BuildUKernelRecFast(coeff,0,count,degmax,r,0,work,0);
center:=(count shl 1)-2;
end;

procedure BuildUComboRecFast(const va,vb:TVec; first,count,degmax,mode:longint;
                             var dst:TDynBool; dst0:longint;
                             var work:TDynBool; work0:longint);
var h,g,childBits,j0,p0,aa,bb:longint;
begin
ClearBoolRange(dst,dst0,(count shl 2)-1);
if count=8 then
  begin
  aa:=0; bb:=0;
  for j0:=0 to 7 do if first+j0<=degmax then
    begin
    if va[first+j0] then aa:=aa or (1 shl j0);
    if vb[first+j0] then bb:=bb or (1 shl j0);
    end;
  if mode=0 then
    for p0:=0 to 28 do
      begin
      if uKernel8[bb,p0] then dst[dst0+p0+1]:=not dst[dst0+p0+1];
      if uKernel8[aa,p0] then
        begin
        dst[dst0+p0]:=not dst[dst0+p0];
        dst[dst0+p0+2]:=not dst[dst0+p0+2];
        end;
      end
  else
    for p0:=0 to 28 do
      begin
      if uKernel8[aa,p0] then dst[dst0+p0+1]:=not dst[dst0+p0+1];
      if uKernel8[bb,p0] then
        begin
        dst[dst0+p0]:=not dst[dst0+p0];
        dst[dst0+p0+1]:=not dst[dst0+p0+1];
        dst[dst0+p0+2]:=not dst[dst0+p0+2];
        end;
      end;
  exit;
  end;
h:=8;
while (h shl 1)<count do h:=h shl 1;
g:=count-h;
childBits:=(g shl 2)-1;
BuildUComboRecFast(va,vb,first,h,degmax,mode,dst,dst0+(g shl 1),work,work0);
BuildUComboRecFast(va,vb,first+h,g,degmax,mode,work,work0,work,work0+childBits);
XorBoolRange(dst,dst0,work,work0,childBits);
XorBoolRange(dst,dst0+h,work,work0,childBits);
XorBoolRange(dst,dst0+h*3,work,work0,childBits);
XorBoolRange(dst,dst0+(h shl 2),work,work0,childBits);
end;

procedure BuildUComboKernelFast(const va,vb:TVec; degmax,mode:longint;
                                var r:TDynBool; var center:longint);
var count,bits:longint;
var work:TDynBool;
begin
count:=((degmax+8) div 8) shl 3;
if count<8 then count:=8;
bits:=(count shl 2)-1;
SetLength(r,bits);
SetLength(work,(count shl 2)+64);
BuildUComboRecFast(va,vb,0,count,degmax,mode,r,0,work,0);
center:=(count shl 1)-1;
end;


procedure AddCircularKernel(var dst:TDynBool; const src:TDynBool; center,shift,period:longint);
var i0,p:longint;
begin
for i0:=0 to High(src) do if src[i0] then
  begin
  p:=(i0-center+shift) mod period;
  if p<0 then inc(p,period);
  dst[p]:=not dst[p];
  end;
end;

{ D=A*B, E=A*reverse(B); all additions below are in GF(2). }
{ C[p]=D[p]+D[2L-p]+E[L-p]+E[L+p]+A[0]B[p]+A[L]B[L-p]. }
procedure ApplyFastUCombo(const va,vb,vsrc:TVec; var vdst:TVec; hi,degmax,mode:longint);
var halfLen,period,convWords,convBits,i0,p,center:longint;
var combo,kernel,ha,hb,hbr,prod0,prod1:TDynBool;
var bit0:boolean;
begin
halfLen:=hi+2;
period:=halfLen shl 1;
convWords:=(halfLen+32) shr 5;
convBits:=convWords shl 5;
BuildUComboKernelFast(va,vb,degmax,mode,combo,center);
SetLength(kernel,period);
AddCircularKernel(kernel,combo,center,0,period);
SetLength(ha,convBits); SetLength(hb,convBits);
if mode<>0 then SetLength(hbr,convBits);
for p:=0 to halfLen do ha[p]:=kernel[p];
for p:=1 to halfLen-1 do
  begin
  hb[p]:=vsrc[p-1];
  if mode<>0 then hbr[halfLen-p]:=vsrc[p-1];
  end;
if mode=0 then
  KarMul(ha,hb,prod0,convWords,halfLen+1,halfLen)
else
  KarMulPair(ha,hb,hbr,prod0,prod1,convWords,halfLen+1,halfLen,halfLen);
for i0:=0 to hi do
  begin
  p:=i0+1;
  if mode=0 then
    bit0:=prod0[p] xor prod0[period-p] xor prod0[halfLen-p] xor prod0[halfLen+p]
  else
    bit0:=prod0[p] xor prod0[period-p] xor prod1[halfLen-p] xor prod1[halfLen+p];
  if ha[0] and hb[p] then bit0:=not bit0;
  if ha[halfLen] and hb[halfLen-p] then bit0:=not bit0;
  vdst[i0]:=bit0;
  end;
vdst[-2]:=false; vdst[-1]:=false; vdst[hi+1]:=false;
end;

procedure ApplyPolyU(const va,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var k2,d,j2:longint;
begin
for k2:=-2 to hi+1 do begin cur0[k2]:=false; cur1[k2]:=false; vdst[k2]:=false; end;
for k2:=0 to hi do cur0[k2]:=vsrc[k2];
d:=PolyDeg(va,degmax);
if d<0 then exit;
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  if va[j2] then XorI(vdst,pcur^,hi);
  if j2>=d then break;
  pcur^[-2]:=false; pcur^[-1]:=false; pcur^[hi+1]:=false;
  AdvanceU(pcur^,pnxt^,hi);
  pnxt^[-2]:=false; pnxt^[-1]:=false; pnxt^[hi+1]:=false;
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
end;

procedure ApplyPolyU0(const va:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var k2,d,j2,curHi,nextHi,maxHi:longint;
begin
d:=PolyDeg(va,degmax);
if (d shl 1)<hi then maxHi:=d shl 1 else maxHi:=hi;
for k2:=-2 to maxHi+1 do begin cur0[k2]:=false; cur1[k2]:=false; end;
for k2:=-2 to hi+1 do vdst[k2]:=false;
if d<0 then exit;
cur0[0]:=true;
pcur:=@cur0;
pnxt:=@cur1;
curHi:=0;
for j2:=0 to d do
  begin
  if va[j2] then XorI(vdst,pcur^,curHi);
  if j2>=d then break;
  nextHi:=curHi+2; if nextHi>hi then nextHi:=hi;
  for k2:=curHi+1 to nextHi+1 do pcur^[k2]:=false;
  AdvanceU(pcur^,pnxt^,nextHi);
  pnxt^[-2]:=false; pnxt^[-1]:=false; pnxt^[nextHi+1]:=false;
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  curHi:=nextHi;
  end;
end;

procedure ApplyBezoutU(const vu,vv,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var k2,d,du,dv,j2:longint;
begin
for k2:=-2 to hi+1 do begin cur0[k2]:=false; cur1[k2]:=false; vdst[k2]:=false; end;
for k2:=0 to hi do cur0[k2]:=vsrc[k2];
du:=PolyDeg(vu,degmax);
dv:=PolyDeg(vv,degmax);
if du>dv then d:=du else d:=dv;
if d<0 then exit;
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  pcur^[-2]:=false; pcur^[-1]:=false; pcur^[hi+1]:=false;
  if j2>=d then
    begin
    if vv[j2] and vu[j2] then XorIH(vdst,pcur^,hi)
    else if vv[j2] then XorI(vdst,pcur^,hi)
    else if vu[j2] then XorH(vdst,pcur^,hi);
    break;
    end;
  if vv[j2] and vu[j2] then AdvanceUXorIH(pcur^,vdst,pnxt^,hi)
  else if vv[j2] then AdvanceUXorI(pcur^,vdst,pnxt^,hi)
  else if vu[j2] then AdvanceUXorH(pcur^,vdst,pnxt^,hi)
  else AdvanceU(pcur^,pnxt^,hi);
  pnxt^[-2]:=false; pnxt^[-1]:=false; pnxt^[hi+1]:=false;
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
end;

procedure ApplyCU(const va,vb,vsrc:TVec; var vdst:TVec; hi,degmax:longint);
var cur0,cur1:TVec;
var pcur,pnxt,pt:PVec;
var k2,d,da,db,j2:longint;
begin
for k2:=-2 to hi+1 do begin cur0[k2]:=false; cur1[k2]:=false; vdst[k2]:=false; end;
for k2:=0 to hi do cur0[k2]:=vsrc[k2];
da:=PolyDeg(va,degmax);
db:=PolyDeg(vb,degmax);
if da>db then d:=da else d:=db;
if d<0 then exit;
pcur:=@cur0;
pnxt:=@cur1;
for j2:=0 to d do
  begin
  pcur^[-2]:=false; pcur^[-1]:=false; pcur^[hi+1]:=false;
  if j2>=d then
    begin
    if va[j2] and vb[j2] then XorH(vdst,pcur^,hi)
    else if vb[j2] then XorIH(vdst,pcur^,hi)
    else if va[j2] then XorI(vdst,pcur^,hi);
    break;
    end;
  if va[j2] and vb[j2] then AdvanceUXorH(pcur^,vdst,pnxt^,hi)
  else if vb[j2] then AdvanceUXorIH(pcur^,vdst,pnxt^,hi)
  else if va[j2] then AdvanceUXorI(pcur^,vdst,pnxt^,hi)
  else AdvanceU(pcur^,pnxt^,hi);
  pnxt^[-2]:=false; pnxt^[-1]:=false; pnxt^[hi+1]:=false;
  pt:=pcur; pcur:=pnxt; pnxt:=pt;
  end;
end;

function BuildOddGUV(const ma,mb,mg,mu,mv:TVec; var gu,qu,qv:TVec; hi,srcHi:longint; extra:boolean):boolean;
var tu,tv:TVec;
var p,dg,du,dv,s:longint;
begin
VecZeroHi(gu,hi);
VecZeroHi(qu,hi+1);
VecZeroHi(qv,hi);
VecZeroHi(tu,srcHi);
VecZeroHi(tv,srcHi);
for p:=0 to srcHi do begin tu[p]:=mu[p]; tv[p]:=mv[p]; end;
if (not extra) and (tu[0] xor tv[0]) then
  for p:=0 to srcHi do
    begin
    tu[p]:=tu[p] xor mb[p];
    tv[p]:=tv[p] xor ma[p];
    end;
if (not extra) and (tu[0] xor tv[0]) then
  begin
  BuildOddGUV:=false;
  exit;
  end;
dg:=PolyDeg(mg,srcHi);
if dg>=0 then
  for p:=0 to dg do if mg[p] then
    begin
    s:=p shl 1;
    if extra then inc(s);
    if s<=hi then gu[s]:=not gu[s];
    end;
du:=PolyDeg(tu,srcHi);
dv:=PolyDeg(tv,srcHi);
if extra then
  begin
  if du>=0 then
    for p:=0 to du do if tu[p] then
      begin
      s:=p shl 1;
      if s<=hi then qu[s]:=not qu[s];
      if s+1<=hi then begin qu[s+1]:=not qu[s+1]; qv[s+1]:=not qv[s+1]; end;
      end;
  if dv>=0 then
    for p:=0 to dv do if tv[p] then
      begin
      s:=p shl 1;
      if s<=hi then qu[s]:=not qu[s];
      end;
  end
else
  begin
  if du>=0 then
    for p:=0 to du do if tu[p] then
      begin
      s:=p shl 1;
      if s<=hi+1 then qu[s]:=not qu[s];
      if s+1<=hi+1 then qu[s+1]:=not qu[s+1];
      if s<=hi then qv[s]:=not qv[s];
      end;
  if dv>=0 then
    for p:=0 to dv do if tv[p] then
      begin
      s:=p shl 1;
      if s<=hi+1 then qu[s]:=not qu[s];
      end;
  if qu[0] then
    begin
    BuildOddGUV:=false;
    exit;
    end;
  for p:=0 to hi do qu[p]:=qu[p+1];
  qu[hi+1]:=false;
  end;
BuildOddGUV:=true;
end;

procedure CalcMat2;
var gu,qu,qv:TVec;
var sa,sb,hu,su,sv:TVec;
var v,z:TVec;
var g0,g1,g2:TVec;
var pg0,pg1,pg2,pt:PVec;
var i0,r0,rU,jmax,target,high:longint;
var m2,hiS,rr,du,dv:longint;

procedure DivMonicBlock(var rem:TVec; const divisor:TVec;
                        var quotient:TVec; top,d:longint);
type TBool32=array[0..31] of boolean;
var drev,iv,rrev,qrev,qblock:TBool32;
var dq,count,k0,s0,p0,i1,j1:longint;
begin
VecZeroHi(quotient,longint(n));
for i1:=0 to 31 do begin drev[i1]:=false; iv[i1]:=false; end;
for i1:=0 to 31 do if d-i1>=0 then drev[i1]:=divisor[d-i1];
iv[0]:=true;
for i1:=1 to 31 do
  for j1:=1 to i1 do if drev[j1] and iv[i1-j1] then iv[i1]:=not iv[i1];
dq:=top-d;
while dq>=0 do
  begin
  count:=dq+1; k0:=count and 31; if k0=0 then k0:=32; s0:=count-k0;
  for i1:=0 to 31 do begin rrev[i1]:=false; qrev[i1]:=false; qblock[i1]:=false; end;
  for i1:=0 to k0-1 do rrev[i1]:=rem[d+s0+k0-1-i1];
  for i1:=0 to k0-1 do
    for j1:=0 to i1 do if rrev[j1] and iv[i1-j1] then qrev[i1]:=not qrev[i1];
  for i1:=0 to k0-1 do
    begin
    qblock[i1]:=qrev[k0-1-i1];
    quotient[s0+i1]:=qblock[i1];
    end;
  for i1:=0 to k0-1 do if qblock[i1] then
    for p0:=0 to d do if divisor[p0] then rem[s0+i1+p0]:=not rem[s0+i1+p0];
  dq:=s0-1;
  end;
end;
begin
TimeMark('c');
TimeMark('q');
if (n and 1)=0 then
  begin
  m2:=longint(n div 2);
  EnsureAB(m2);
  hiS:=m2 div 2;
  for i:=0 to longint(n div 2) do
    begin
    gu[i]:=false; qu[i]:=false; qv[i]:=false;
    end;
  for i:=0 to hiS do
    begin
    sa[i]:=hf[i] xor hf1[i];
    sb[i]:=hc[i] xor hc1[i];
    end;
  rr:=GcdU(sa,sb,hu,su,sv,hiS);
  for i:=0 to rr do if hu[i] then gu[i shl 1]:=true;
  du:=PolyDeg(su,hiS);
  for i:=0 to du do if su[i] then
    begin
    qu[i shl 1]:=true;
    if (i shl 1)+1<=longint(n div 2) then qv[(i shl 1)+1]:=not qv[(i shl 1)+1];
    end;
  dv:=PolyDeg(sv,hiS);
  for i:=0 to dv do if sv[i] then qv[i shl 1]:=not qv[i shl 1];
  rU:=rr shl 1;
  end
else
  begin
  m2:=longint(n div 2);
  EnsureAB(m2);
  hiS:=m2 div 2;
  rr:=GcdU(hf,hc,hu,su,sv,hiS);
  if BuildOddGUV(hf,hc,hu,su,sv,gu,qu,qv,longint(n div 2),hiS,(m2 mod 3)=2) then
    rU:=PolyDeg(gu,longint(n div 2))
  else
    rU:=GcdU(f,c,gu,qu,qv,longint(n div 2));
  end;
r0:=rU*2;
TimeMark('z');
ApplyFastUCombo(qu,qv,y,z,n-1,longint(n div 2),0);
TimeMark('d');
if r0=0 then
  begin
  for i:=0 to n-1 do x[i]:=z[i];
  end
else
begin
TimeMark('x');
ApplyPolyU0(gu,g0,n-1,rU);
pg1:=@g0; pg2:=@g1; pg0:=@g2;
VecZeroHi(pg2^,longint(n)); VecZeroHi(pg0^,longint(n));
for i:=0 to n-1 do x[i]:=false;
jmax:=longint(n)-r0-1;
if jmax>=0 then
  begin
  target:=r0;
  if target>jmax+1 then target:=jmax+1;
  for j:=1 to target do
    begin
    high:=r0+j; if high>longint(n)-1 then high:=longint(n)-1;
    for i:=-2 to high+1 do pg0^[i]:=false;
    for i:=0 to high do pg0^[i]:=pg1^[i-1] xor pg1^[i+1] xor pg2^[i];
    pt:=pg0; pg0:=pg2; pg2:=pg1; pg1:=pt;
    end;

  if jmax>=r0 then
    begin
    DivMonicBlock(z,pg1^,v,longint(n)-1,r0 shl 1);
    for i:=0 to jmax-r0 do x[i+r0]:=v[i];
    end;

  j:=r0-1; if j>jmax then j:=jmax;
  while j>=0 do
    begin
    i:=j+r0;
    if z[i] then
      begin
      for i0:=0 to i do z[i0]:=z[i0] xor pg2^[i0];
      x[j]:=true;
      end;
    if j>0 then
      begin
      high:=i-1;
      for i0:=-2 to high+1 do pg0^[i0]:=false;
      for i0:=0 to high do pg0^[i0]:=pg2^[i0-1] xor pg2^[i0+1] xor pg1^[i0];
      pt:=pg0; pg0:=pg1; pg1:=pg2; pg2:=pt;
      end;
    dec(j);
    end;
  end;
end;
end;

function GeneMat():boolean;
var t:TVec;
begin
TimeMark('g');
ApplyFastUCombo(f,c,x,t,n-1,longint(n div 2),1);
GeneMat:=true;
for i:=0 to n-1 do GeneMat:=GeneMat and (t[i]=y[i]);
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
InitUKernel8;
{$ifdef disp}
for n:=1 to m do
{$else}
for n:=9900 to 10000 do
{$endif}
  begin
  write(n,#9);
  MakeMat();
  CalcMat2();
  GeneMat();{$ifdef disp}write('%');SaveMat('_T2');{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
