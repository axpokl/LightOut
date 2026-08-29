//{$define disp}
program diandeng;

{$mode objfpc}{$H+}

{ H42: multiply reflection-symmetric Laurent polynomials by two half convolutions. }
{ A and B use the same formula, 8-coefficient leaves and 128-bit Karatsuba cutoff. }

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

procedure MakeMat();
var old,old1,prev,cur,nxt,newA,newB:boolean;
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
for j:=k+1 to n do
  begin
  for i:=j downto 0 do
    begin
    old:=y[i];
    if i<j then y[i]:=not(y[i-2] xor y[i-1] xor y[i] xor y1[i-2] xor y_[i-1] xor y_[i] xor y_[i+1] xor y_1[i-1] xor y_1[i])
    else y[i]:=false;
    y1[i]:=old;
    end;
  old:=y_[-2]; y_1[-2]:=old; y_[-2]:=true;
  old:=y_[-1]; y_1[-1]:=old; y_[-1]:=false;
  prev:=y_[0]; y_1[0]:=prev; y_[0]:=y[0];
  for i:=1 to j-1 do
    begin
    cur:=y_[i];
    nxt:=y_[i+1];
    old1:=y_1[i];
    y_1[i]:=cur;
    y_[i]:=prev xor cur xor nxt xor old1;
    prev:=cur;
    end;
  cur:=y_[j]; y_1[j]:=cur; y_[j]:=false;
  if j=1 then
    begin
    f1[0]:=f[0]; c1[0]:=c[0];
    f[0]:=false; c[0]:=true;
    end
  else
    begin
    hiu:=j div 2;
    for i:=hiu downto 0 do
      begin
      old:=f[i]; old1:=c[i];
      if i=0 then newA:=f1[i] else newA:=f1[i] xor c[i-1];
      newB:=f[i] xor c[i] xor c1[i];
      f[i]:=newA; c[i]:=newB;
      f1[i]:=old; c1[i]:=old1;
      end;
    end;
  if j=longint(n div 2) then
    begin
    VecCopyHi(hf,f,j div 2);
    VecCopyHi(hc,c,j div 2);
    VecCopyHi(hf1,f1,j div 2);
    VecCopyHi(hc1,c1,j div 2);
    hk:=j;
    ho:=true;
    end;
  end;
k:=n;
end;

procedure EnsureAB(nn:longword);
var old,old1,newA,newB:boolean;
var jj,ii,hiu:longint;
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
    hf1[0]:=hf[0]; hc1[0]:=hc[0];
    hf[0]:=false; hc[0]:=true;
    end
  else
    begin
    hiu:=jj div 2;
    for ii:=hiu downto 0 do
      begin
      old:=hf[ii]; old1:=hc[ii];
      if ii=0 then newA:=hf1[ii] else newA:=hf1[ii] xor hc[ii-1];
      newB:=hf[ii] xor hc[ii] xor hc1[ii];
      hf[ii]:=newA; hc[ii]:=newB;
      hf1[ii]:=old; hc1[ii]:=old1;
      end;
    end;
  end;
hk:=nn;
end;

function GcdU(const va,vb:TVec; var vg,vu,vv:TVec; hi:longint):longint;
var r0a,r1a,u0a,u1a,v0a,v1a:TVec;
var r0,r1,u0,u1,v0,v1,tt:PVec;
var kr0,kr1,ku0,ku1,kv0,kv1,shift,p,top,lim:longint;
begin
r0:=@r0a; r1:=@r1a; u0:=@u0a; u1:=@u1a; v0:=@v0a; v1:=@v1a;
for p:=0 to hi do
  begin
  r0^[p]:=va[p]; r1^[p]:=vb[p];
  u0^[p]:=false; u1^[p]:=false;
  v0^[p]:=false; v1^[p]:=false;
  end;
u0^[0]:=true;
v1^[0]:=true;
kr0:=PolyDeg(r0^,hi);
kr1:=PolyDeg(r1^,hi);
ku0:=0; ku1:=-1;
kv0:=-1; kv1:=0;
while true do
  begin
  if kr0<kr1 then
    begin
    tt:=r0; r0:=r1; r1:=tt;
    tt:=u0; u0:=u1; u1:=tt;
    tt:=v0; v0:=v1; v1:=tt;
    p:=kr0; kr0:=kr1; kr1:=p;
    p:=ku0; ku0:=ku1; ku1:=p;
    p:=kv0; kv0:=kv1; kv1:=p;
    end;
  if kr1<0 then
    begin
    VecCopyHi(vg,r0^,hi);
    VecCopyHi(vu,u0^,hi);
    VecCopyHi(vv,v0^,hi);
    GcdU:=kr0;
    exit;
    end;
  while kr0>=kr1 do
    begin
    shift:=kr0-kr1;
    for p:=0 to kr1 do if r1^[p] then r0^[p+shift]:=not r0^[p+shift];
    top:=kr0-1;
    while (top>=0) and not(r0^[top]) do dec(top);
    kr0:=top;
    if ku1>=0 then
      begin
      top:=ku0;
      if ku1+shift>top then top:=ku1+shift;
      if top>hi then top:=hi;
      lim:=ku1;
      if lim>hi-shift then lim:=hi-shift;
      for p:=0 to lim do if u1^[p] then u0^[p+shift]:=not u0^[p+shift];
      while (top>=0) and not(u0^[top]) do dec(top);
      ku0:=top;
      end;
    if kv1>=0 then
      begin
      top:=kv0;
      if kv1+shift>top then top:=kv1+shift;
      if top>hi then top:=hi;
      lim:=kv1;
      if lim>hi-shift then lim:=hi-shift;
      for p:=0 to lim do if v1^[p] then v0^[p+shift]:=not v0^[p+shift];
      while (top>=0) and not(v0^[top]) do dec(top);
      kv0:=top;
      end;
    end;
  end;
end;

type TDynBool=array of boolean;

procedure KarRec(const a:TDynBool; ao:longint; const b:TDynBool; bo:longint;
                 var r:TDynBool; ro,len:longint; var work:TDynBool; wo:longint);
const cut=128;
var i0,j0,h,ax0,bx0,z10,save0,rec0:longint;
var s2:boolean;
begin
if len<=cut then
  begin
  for i0:=0 to len-1 do if a[ao+i0] then
    for j0:=0 to len-1 do if b[bo+j0] then
      r[ro+i0+j0]:=not r[ro+i0+j0];
  exit;
  end;
h:=len shr 1;
KarRec(a,ao,b,bo,r,ro,h,work,wo);
KarRec(a,ao+h,b,bo+h,r,ro+(h shl 1),h,work,wo);
ax0:=wo; bx0:=wo+h; z10:=wo+(h shl 1); save0:=wo+(h shl 2); rec0:=save0+h;
for i0:=0 to h-1 do
  begin
  work[ax0+i0]:=a[ao+i0] xor a[ao+h+i0];
  work[bx0+i0]:=b[bo+i0] xor b[bo+h+i0];
  end;
for i0:=0 to (h shl 1)-1 do work[z10+i0]:=false;
KarRec(work,ax0,work,bx0,work,z10,h,work,rec0);
for i0:=0 to h-1 do work[save0+i0]:=r[ro+(h shl 1)+i0];
for i0:=(h shl 1)-1 downto 0 do r[ro+h+i0]:=r[ro+h+i0] xor r[ro+i0];
for i0:=0 to (h shl 1)-1 do
  begin
  if i0<h then s2:=work[save0+i0] else s2:=r[ro+(h shl 1)+i0];
  r[ro+h+i0]:=r[ro+h+i0] xor s2 xor work[z10+i0];
  end;
end;

procedure KarMul(const a,b:TDynBool; var r:TDynBool; len:longint);
var work:TDynBool;
var i0:longint;
begin
SetLength(r,len shl 1);
for i0:=0 to High(r) do r[i0]:=false;
SetLength(work,len*6);
KarRec(a,0,b,0,r,0,len,work,0);
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
var h,childBits,j0,p0,aa,bb:longint;
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
h:=count shr 1;
childBits:=(h shl 2)-1;
BuildUComboRecFast(va,vb,first,h,degmax,mode,dst,dst0+(h shl 1),work,work0);
BuildUComboRecFast(va,vb,first+h,h,degmax,mode,work,work0,work,work0+childBits);
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
count:=8;
while count<=degmax do count:=count shl 1;
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
var halfLen,period,halfPad,i0,p,center:longint;
var combo,kernel,ha,hb,hbr,prod0,prod1:TDynBool;
var bit0:boolean;
begin
halfLen:=hi+2;
period:=halfLen shl 1;
halfPad:=1;
while halfPad<=halfLen do halfPad:=halfPad shl 1;
BuildUComboKernelFast(va,vb,degmax,mode,combo,center);
SetLength(kernel,period);
AddCircularKernel(kernel,combo,center,0,period);
SetLength(ha,halfPad); SetLength(hb,halfPad); SetLength(hbr,halfPad);
for p:=0 to halfLen do ha[p]:=kernel[p];
for p:=1 to halfLen-1 do
  begin
  hb[p]:=vsrc[p-1];
  hbr[halfLen-p]:=vsrc[p-1];
  end;
KarMul(ha,hb,prod0,halfPad);
KarMul(ha,hbr,prod1,halfPad);
for i0:=0 to hi do
  begin
  p:=i0+1;
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
var i0,r0,rU,jmax,row1,row2,row3,l0,l1,l2,r1,r2:longint;
var m2,hiS,rr,du,dv:longint;
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
pg0:=@g0; pg1:=@g1; pg2:=@g2;
if n-r0-1<0 then jmax:=0 else jmax:=n-r0-1;
if jmax=0 then begin VecCopyHi(pg1^,pg0^,longint(n)); VecZeroHi(pg2^,longint(n)); end
else if r0<jmax then
  begin
  for i:=-2 to n do v[i]:=false;
  for i:=0 to n-1 do v[i]:=pg0^[i-1] xor pg0^[i+1];
  for i:=-2 to n do begin pg1^[i]:=false; pg2^[i]:=false; end;
  for i:=0 to n-1 do begin pg1^[i]:=pg0^[n-1-i]; pg2^[i]:=v[n-1-i]; end;
  for j:=1 to r0 do
    begin
    for i:=-2 to n do pg0^[i]:=false;
    for i:=0 to n-1 do pg0^[i]:=pg1^[i] xor pg2^[i-1] xor pg2^[i+1];
    pt:=pg0; pg0:=pg1; pg1:=pg2; pg2:=pt;
    end;
  end
else
  begin
  VecZeroHi(pg2^,longint(n));
  VecCopyHi(pg1^,pg0^,longint(n));
  for j:=1 to jmax do
    begin
    for i:=-2 to n do pg0^[i]:=false;
    for i:=0 to n-1 do pg0^[i]:=pg1^[i-1] xor pg1^[i+1] xor pg2^[i];
    pt:=pg0; pg0:=pg2; pg2:=pg1; pg1:=pt;
    end;
  end;
for i:=0 to n-1 do x[i]:=false;
row1:=n-1;
row2:=n-2;
if r0<=n-1 then
for i:=n-1 downto r0 do
  begin
  l1:=row1-(r0 shl 1); if l1<0 then l1:=0; r1:=row1; if r1>longint(n)-1 then r1:=longint(n)-1;
  if z[i] then
    begin
    i0:=i-r0;
    for j:=l1 to r1 do z[j]:=z[j] xor pg1^[j];
    x[i0]:=true;
    end;
  if i>r0 then
    begin
    l2:=row2-(r0 shl 1); if l2<0 then l2:=0; r2:=row2;
    row3:=row2-1;
    l0:=row3-(r0 shl 1); if l0<0 then l0:=0;
    for j:=l0 to row3 do
      pg0^[j]:=(((j>=l1) and (j<=r1)) and pg1^[j]) xor
               (((j-1>=l2) and (j-1<=r2)) and pg2^[j-1]) xor
               (((j+1>=l2) and (j+1<=r2)) and pg2^[j+1]);
    pt:=pg0; pg0:=pg1; pg1:=pg2; pg2:=pt;
    row1:=row2;
    row2:=row3;
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
