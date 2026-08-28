{$define disp}
program diandeng;

{$mode objfpc}{$H+}
{$optimization on}
{$inline on}

{ H43 debug/output build: the same Laurent-kernel and exact NTT algorithm. }

{$ifdef disp}
uses display;
{$endif}

const m=2000;
const nttMod:LongWord=998244353;
const nttRoot:LongWord=3;
const nttR:LongWord=301989884;
const nttR2:LongWord=932051910;

type TVec=array[-2..m]of boolean;
     PVec=^TVec;
     TDynBool=array of boolean;
     TModArray=array of LongWord;
     TIntArray=array of longint;

var n:longword;
var i,j:longint;
var x,y,y1,y_,y_1,f,f1,c,c1:TVec;
var hf,hf1,hc,hc1:TVec;
var k:longint;
var hk:longint;
var o,ho:boolean;
var uBasis8:array[0..7,0..28] of boolean;
var nttPrime:LongWord;
var nttRoots:TModArray;
var nttRev:TIntArray;
var nttA,nttB:TModArray;
var nttCacheN:longint;

{$ifdef disp}
var bb:pbitbuf;
var bp:pbitmap;
{$endif}

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
  if l-2>=-2 then pcur^[l-2]:=false;
  if l-1>=-2 then pcur^[l-1]:=false;
  if r+1<=hi+1 then pcur^[r+1]:=false;
  if r+2<=hi+1 then pcur^[r+2]:=false;
  for k2:=l2 to r2 do pnxt^[k2]:=pcur^[k2-1] xor pcur^[k2+1];
  while (l2<=r2) and not(pnxt^[l2]) do inc(l2);
  if l2>r2 then break;
  while not(pnxt^[r2]) do dec(r2);
  if l2-2>=-2 then pnxt^[l2-2]:=false;
  if l2-1>=-2 then pnxt^[l2-1]:=false;
  if r2+1<=hi+1 then pnxt^[r2+1]:=false;
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
write('A ');for i:=0 to n div 2 do if f[i] then write(1) else write(0);writeln;
write('B ');for i:=0 to n div 2 do if c[i] then write(1) else write(0);writeln;
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

function gcd(const vf,vg:TVec; var vd,vr:TVec):longint;
var f0a,g0a,vxa,vya:TVec;
var f0,g0,vx,vy,vt:PVec;
var kf,kg,kvx,kvy,shift,p,top,lim:longint;
begin
f0:=@f0a; g0:=@g0a; vx:=@vxa; vy:=@vya;
for p:=0 to n do
  begin
  f0^[p]:=vf[p]; g0^[p]:=vg[p];
  vx^[p]:=false; vy^[p]:=false;
  end;
kf:=n; while (kf>=0) and not(f0^[kf]) do dec(kf);
kg:=n; while (kg>=0) and not(g0^[kg]) do dec(kg);
kvx:=-1;
kvy:=0;
vy^[0]:=true;
while true do
  begin
  if kf<kg then
    begin
    vt:=f0; f0:=g0; g0:=vt;
    vt:=vx; vx:=vy; vy:=vt;
    p:=kf; kf:=kg; kg:=p;
    p:=kvx; kvx:=kvy; kvy:=p;
    end;
  if kg<0 then
    begin
    VecCopyHi(vd,f0^,longint(n));
    VecCopyHi(vr,vx^,longint(n));
    gcd:=kf;
    exit;
    end;
  while kf>=kg do
    begin
    shift:=kf-kg;
    for p:=0 to kg do if g0^[p] then f0^[p+shift]:=f0^[p+shift] xor true;
    top:=kf-1;
    while (top>=0) and not(f0^[top]) do dec(top);
    kf:=top;
    if kvy>=0 then
      begin
      top:=kvx;
      if kvy+shift>longint(n) then top:=longint(n)
      else if kvy+shift>top then top:=kvy+shift;
      lim:=kvy;
      if lim>longint(n)-shift then lim:=longint(n)-shift;
      for p:=0 to lim do if vy^[p] then vx^[p+shift]:=vx^[p+shift] xor true;
      while (top>=0) and not(vx^[top]) do dec(top);
      kvx:=top;
      end;
    end;
  end;
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

procedure InitUKernel8;
var j0,p0:longint;
begin
for j0:=0 to 7 do for p0:=0 to 28 do uBasis8[j0,p0]:=false;
uBasis8[0,14]:=true;
for j0:=1 to 7 do
  for p0:=0 to 28 do if uBasis8[j0-1,p0] then
    begin
    if p0>=2 then uBasis8[j0,p0-2]:=not uBasis8[j0,p0-2];
    if p0>=1 then uBasis8[j0,p0-1]:=not uBasis8[j0,p0-1];
    if p0<=27 then uBasis8[j0,p0+1]:=not uBasis8[j0,p0+1];
    if p0<=26 then uBasis8[j0,p0+2]:=not uBasis8[j0,p0+2];
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
var h,childBits,j0,p0:longint;
begin
ClearBoolRange(dst,dst0,(count shl 2)-3);
if count=8 then
  begin
  for j0:=0 to 7 do if (first+j0<=degmax) and coeff[first+j0] then
    for p0:=0 to 28 do if uBasis8[j0,p0] then
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

function NTTMontMul(a,b:LongWord):LongWord; inline;
var t,mn,sl,u:QWord;
var mm:LongWord;
begin
t:=QWord(a)*b;
mm:=LongWord(QWord(LongWord(t))*nttPrime);
mn:=QWord(mm)*nttMod;
sl:=QWord(LongWord(t))+LongWord(mn);
u:=(t shr 32)+(mn shr 32)+(sl shr 32);
if u>=nttMod then u:=u-nttMod;
NTTMontMul:=LongWord(u);
end;

function NTTModPow(a,e:LongWord):LongWord;
var r0:QWord;
begin
r0:=1;
while e<>0 do
  begin
  if (e and 1)<>0 then r0:=(r0*a) mod nttMod;
  a:=(QWord(a)*a) mod nttMod;
  e:=e shr 1;
  end;
NTTModPow:=LongWord(r0);
end;

function NTTToMont(a:LongWord):LongWord; inline;
begin
NTTToMont:=NTTMontMul(a,nttR2);
end;

procedure InitNTT;
var x0:LongWord;
var k0:longint;
begin
x0:=nttMod;
for k0:=1 to 5 do x0:=LongWord(QWord(x0)*(2-LongWord(QWord(nttMod)*x0)));
nttPrime:=0-x0;
nttCacheN:=0;
end;

procedure PrepareNTT(nn:longint);
var i0,j0:longint;
var base:LongWord;
begin
if nttCacheN=nn then exit;
nttCacheN:=nn;
SetLength(nttRoots,nn); SetLength(nttRev,nn);
base:=NTTToMont(NTTModPow(nttRoot,(nttMod-1) div nn));
nttRoots[0]:=nttR;
for i0:=1 to nn-1 do nttRoots[i0]:=NTTMontMul(nttRoots[i0-1],base);
nttRev[0]:=0;
for i0:=1 to nn-1 do
  begin
  j0:=nttRev[i0 shr 1] shr 1;
  if (i0 and 1)<>0 then j0:=j0 or (nn shr 1);
  nttRev[i0]:=j0;
  end;
end;

procedure NTTTransform(var a:TModArray; invert:boolean);
var nn,i0,j0,len0,half,k0,step,ri:longint;
var u0,v0,tmp,invn:LongWord;
begin
nn:=Length(a); PrepareNTT(nn);
for i0:=1 to nn-1 do
  begin
  j0:=nttRev[i0];
  if i0<j0 then begin tmp:=a[i0]; a[i0]:=a[j0]; a[j0]:=tmp; end;
  end;
len0:=2;
while len0<=nn do
  begin
  half:=len0 shr 1; step:=nn div len0; i0:=0;
  while i0<nn do
    begin
    for k0:=0 to half-1 do
      begin
      u0:=a[i0+k0]; ri:=k0*step;
      if invert and (ri<>0) then ri:=nn-ri;
      v0:=NTTMontMul(a[i0+k0+half],nttRoots[ri]);
      if u0+v0>=nttMod then a[i0+k0]:=u0+v0-nttMod else a[i0+k0]:=u0+v0;
      if u0>=v0 then a[i0+k0+half]:=u0-v0 else a[i0+k0+half]:=u0+nttMod-v0;
      end;
    inc(i0,len0);
    end;
  len0:=len0 shl 1;
  end;
if invert then
  begin
  invn:=NTTToMont(NTTModPow(nn,nttMod-2));
  for i0:=0 to nn-1 do a[i0]:=NTTMontMul(a[i0],invn);
  end;
end;

procedure NTTMulBool(const a,b:TDynBool; var r:TDynBool; bitLen:longint);
var nn,i0:longint;
begin
nn:=bitLen shl 1;
PrepareNTT(nn);
SetLength(nttA,nn); SetLength(nttB,nn);
for i0:=0 to nn-1 do
  begin
  if (i0<Length(a)) and a[i0] then nttA[i0]:=nttR else nttA[i0]:=0;
  if (i0<Length(b)) and b[i0] then nttB[i0]:=nttR else nttB[i0]:=0;
  end;
NTTTransform(nttA,false); NTTTransform(nttB,false);
for i0:=0 to nn-1 do nttA[i0]:=NTTMontMul(nttA[i0],nttB[i0]);
NTTTransform(nttA,true);
SetLength(r,nn);
for i0:=0 to nn-1 do r[i0]:=(NTTMontMul(nttA[i0],1) and 1)<>0;
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

procedure ApplyFastUCombo(const va,vb,vsrc:TVec; var vdst:TVec; hi,degmax,mode:longint);
var period,pad,i0,p,center:longint;
var ka,kb,kernel,src,prod:TDynBool;
begin
period:=(hi+2) shl 1;
pad:=1;
while pad<period do pad:=pad shl 1;
BuildUKernelFast(va,degmax,ka,center);
BuildUKernelFast(vb,degmax,kb,center);
SetLength(kernel,pad);
if mode=0 then
  begin
  AddCircularKernel(kernel,kb,center,0,period);
  AddCircularKernel(kernel,ka,center,-1,period);
  AddCircularKernel(kernel,ka,center,1,period);
  end
else
  begin
  AddCircularKernel(kernel,ka,center,0,period);
  AddCircularKernel(kernel,kb,center,0,period);
  AddCircularKernel(kernel,kb,center,-1,period);
  AddCircularKernel(kernel,kb,center,1,period);
  end;
SetLength(src,pad);
for i0:=0 to hi do if vsrc[i0] then
  begin
  src[i0+1]:=not src[i0+1];
  src[period-i0-1]:=not src[period-i0-1];
  end;
NTTMulBool(kernel,src,prod,pad);
for i0:=0 to hi do
  begin
  p:=i0+1;
  vdst[i0]:=false;
  while p<=High(prod) do
    begin
    vdst[i0]:=vdst[i0] xor prod[p];
    inc(p,period);
    end;
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
var i0,r0,rU,kk,jmax,row1,row2,row3,l0,l1,l2,r1,r2:longint;
var m2,hiS,rr,du,dv:longint;
begin
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
writeln('gcd',#9,r0,#9);
write('U ');for i:=0 to n div 2 do if qu[i] then write(1) else write(0);writeln;
write('V ');for i:=0 to n div 2 do if qv[i] then write(1) else write(0);writeln;
write('G ');for i:=0 to n div 2 do if gu[i] then write(1) else write(0);writeln;
for i:=-1 to n do v[i]:=y[i];
write('y ');for i:=0 to n-1 do if v[i] then write(1) else write(0);writeln;
ApplyFastUCombo(qu,qv,y,z,n-1,longint(n div 2),0);
if r0=0 then
  for i:=0 to n-1 do x[i]:=z[i]
else
begin
write('z ');for i:=0 to n-1 do if z[i] then write(1) else write(0);writeln;
ApplyPolyU0(gu,g0,n-1,rU);
if n-r0-1<0 then jmax:=0 else jmax:=n-r0-1;
for i:=-2 to n do v[i]:=g0[i];
writeln('d');
write(0,#9);for i:=0 to n-1 do if g0[i] then write(1) else write(0);writeln;
pg0:=@g0; pg1:=@g1; pg2:=@g2;
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
    write(j,#9);for i:=0 to n-1 do if pg0^[i] then write(1) else write(0);writeln;
    pt:=pg0; pg0:=pg2; pg2:=pg1; pg1:=pt;
    end;
  for j:=jmax+1 to n-1 do begin write(j,#9);for i:=0 to n-1 do write(0);writeln; end;
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
write(i,#9,i0,#9);
for kk:=0 to n-1 do if z[kk] then write(1) else write(0);write(#9);
    for j:=l1 to r1 do z[j]:=z[j] xor pg1^[j];
    x[i0]:=true;
for kk:=0 to n-1 do if pg1^[kk] then write(1) else write(0);write(#9);
for kk:=0 to n-1 do if z[kk] then write(1) else write(0);write(#9);
for kk:=0 to n-1 do if x[kk] then write(1) else write(0);write(#9);
writeln();
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
write('x ');for i:=0 to n-1 do if x[i] then write(1) else write(0);writeln;
end;

function GeneMat():boolean;
var x2,x1,x0:TVec;
begin
for i:=-2 to n do begin x2[i]:=false; x1[i]:=false; end;
for i:=0 to n-1 do x1[i]:=x[i];
{$ifdef disp}
while IsNextMsg() do ;
for i:=0 to n-1 do
  if x1[i] then SetBBPixel(bb,i,0,black) else SetBBPixel(bb,i,0,white);
{$endif}
for j:=1 to n-1 do
  begin
  for i:=-2 to n do x0[i]:=false;
  for i:=0 to n-1 do x0[i]:=not(x1[i-1] xor x1[i] xor x1[i+1] xor x2[i]);
  {$ifdef disp}
  for i:=0 to n-1 do
    if x0[i] then SetBBPixel(bb,i,j,black) else SetBBPixel(bb,i,j,white);
  {$endif}
  for i:=-2 to n do x2[i]:=x1[i];
  for i:=-2 to n do x1[i]:=x0[i];
  end;
GeneMat:=true;
for i:=0 to n-1 do GeneMat:=GeneMat and (x1[i-1] xor x1[i] xor x1[i+1] xor x2[i]);
writeln(GeneMat);
end;

begin
{$ifdef disp}
CreateWin(m,m);
bb:=CreateBB(GetWin());
bp:=CreateBMP(m,m);
{$endif}
InitUKernel8;
InitNTT;
for n:=1 to 20 do
  begin
  writeln('#',n);
  MakeMat();
  CalcMat2();
  GeneMat();{$ifdef disp}SaveMat('_T2');{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
