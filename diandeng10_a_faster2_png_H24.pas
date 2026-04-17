//{$define disp}
program diandeng;

{$ifdef disp}
uses Windows, display;
const m=1000;
const sosN=1024;
{$else}
uses Windows;
const m=10000;
const sosN=16384;
{$endif}

type TVec=array[-2..m]of boolean;
     TSos=array[0..sosN-1]of byte;

var n:longword;
var i,j:longint;
var x,y,y1,y_,y_1,f,f1:TVec;
var k:longint;
var o:boolean;
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

function VecIsZero(const a:TVec;hi:longint):boolean;
var k2:longint;
begin
for k2:=0 to hi do if a[k2] then begin VecIsZero:=false; exit; end;
VecIsZero:=true;
end;

procedure BuildC(const vf:TVec; var vc:TVec);
var tmp:TSos;
var bit,base,t:longint;
begin
for base:=0 to sosN-1 do tmp[base]:=0;
for base:=0 to n do if vf[base] then tmp[base]:=1;
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
for base:=0 to n do vc[base]:=tmp[base]<>0;
end;

procedure MakeMat();
var y2,y_2,f2:TVec;
begin
TimeMark('m');
if (not o) or (longint(n)<k) then
  begin
  for i:=-2 to m do
    begin
    y1[i]:=false; y[i]:=false; y_1[i]:=false; y_[i]:=false;
    f1[i]:=false; f[i]:=false;
    end;
  f[0]:=true;
  k:=0; o:=true;
  end;
for j:=k+1 to n do
  begin
  for i:=-2 to m do begin y_2[i]:=false; y2[i]:=false; end;
  for i:=1 to j-1 do y_2[i]:=y_[i-1] xor y_[i] xor y_[i+1] xor y_1[i];
  for i:=0 to j-1 do y2[i]:=not(y[i-2] xor y[i-1] xor y[i] xor y1[i-2] xor y_[i-1] xor y_[i] xor y_[i+1] xor y_1[i-1] xor y_1[i]);
  y_2[0]:=y2[0];
  y_2[-2]:=true;
  y_1:=y_; y_:=y_2; y1:=y; y:=y2;
  end;
for j:=k+1 to n do
  begin
  for i:=-2 to m do f2[i]:=false;
  for i:=0 to j do f2[i]:=f[i-1] xor f1[i];
  f1:=f; f:=f2;
  end;
k:=n;
end;

function gcd(const vf,vg:TVec; var vd,vr:TVec):longint;
var f0,g0,vt,vx,vy:TVec;
var kf,kg,kvx,kvy,shift,p,top,lim:longint;
begin
for p:=0 to n do
  begin
  f0[p]:=vf[p]; g0[p]:=vg[p];
  vx[p]:=false; vy[p]:=false;
  end;
kf:=n; while (kf>=0) and not(f0[kf]) do dec(kf);
kg:=n; while (kg>=0) and not(g0[kg]) do dec(kg);
kvx:=-1;
kvy:=0;
vy[0]:=true;
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
    vd:=f0;
    vr:=vx;
    gcd:=kf;
    exit;
    end;
  while kf>=kg do
    begin
    shift:=kf-kg;
    for p:=0 to kg do if g0[p] then f0[p+shift]:=f0[p+shift] xor true;
    top:=kf-1;
    while (top>=0) and not(f0[top]) do dec(top);
    kf:=top;
    if kvy>=0 then
      begin
      top:=kvx;
      if kvy+shift>longint(n) then top:=longint(n)
      else if kvy+shift>top then top:=kvy+shift;
      lim:=kvy;
      if lim>longint(n)-shift then lim:=longint(n)-shift;
      for p:=0 to lim do if vy[p] then vx[p+shift]:=vx[p+shift] xor true;
      while (top>=0) and not(vx[top]) do dec(top);
      kvx:=top;
      end;
    end;
  end;
end;


procedure CalcMat2;
var c,q,g:TVec;
var v,v0,z:TVec;
var g0,g1,g2:TVec;
var i0,r0,jmax,row1,row2,row3,l0,l1,l2,r1,r2:longint;
begin
TimeMark('c');
BuildC(f,c);
TimeMark('q');
r0:=gcd(f,c,g,q);
TimeMark('z');
for i:=-1 to n do v[i]:=y[i];
for i:=0 to n do z[i]:=false;
for j:=0 to n-1 do 
  begin
  if q[j] then for i:=0 to n-1 do z[i]:=z[i] xor v[i];
  for i:=0 to n-1 do v0[i]:=v[i-1] xor v[i+1];
  for i:=0 to n-1 do v[i]:=v0[i];
  if VecIsZero(v,n-1) then break;
  end;
TimeMark('d');
if r0=0 then
  begin
  for i:=0 to n-1 do x[i]:=z[i];
  end
else
begin
for i:=-2 to n do begin g0[i]:=false; g1[i]:=false; g2[i]:=false; v[i]:=false; v0[i]:=false; end;
v[0]:=true;
for j:=0 to r0 do 
  begin
  if g[j] then for i:=0 to n-1 do g0[i]:=g0[i] xor v[i];
  for i:=0 to n-1 do v0[i]:=v[i-1] xor v[i+1];
  for i:=-2 to n do v[i]:=v0[i];
  if VecIsZero(v,n-1) then break;
  end;
TimeMark('x');
if n-r0-1<0 then jmax:=0 else jmax:=n-r0-1;
if jmax=0 then g1:=g0
else if r0<jmax then
  begin
  for i:=-2 to n do v[i]:=false;
  for i:=0 to n-1 do v[i]:=g0[i-1] xor g0[i+1];
  for i:=-2 to n do begin g1[i]:=false; g2[i]:=false; end;
  for i:=0 to n-1 do begin g1[i]:=g0[n-1-i]; g2[i]:=v[n-1-i]; end;
  for j:=1 to r0 do
    begin
    for i:=-2 to n do g0[i]:=false;
    for i:=0 to n-1 do g0[i]:=g1[i] xor g2[i-1] xor g2[i+1];
    g1:=g2;
    g2:=g0;
    end;
  end
else
  begin
  g1:=g0;
  for j:=1 to jmax do
    begin
    for i:=-2 to n do g0[i]:=false;
    for i:=0 to n-1 do g0[i]:=g1[i-1] xor g1[i+1] xor g2[i];
    g2:=g1;
    g1:=g0;
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
    for j:=l1 to r1 do z[j]:=z[j] xor g1[j];
    x[i0]:=true;
    end;
  if i>r0 then
    begin
    l2:=row2-(r0 shl 1); if l2<0 then l2:=0; r2:=row2;
    row3:=row2-1;
    l0:=row3-(r0 shl 1); if l0<0 then l0:=0;
    for j:=l0 to row3 do
      g0[j]:=(((j>=l1) and (j<=r1)) and g1[j]) xor
             (((j-1>=l2) and (j-1<=r2)) and g2[j-1]) xor
             (((j+1>=l2) and (j+1<=r2)) and g2[j+1]);
    g1:=g2;
    g2:=g0;
    row1:=row2;
    row2:=row3;
    end;
  end;
end;
end;

function GeneMat():boolean;
var x2,x1,x0:TVec;
begin
TimeMark('g');
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
  write(n,#9);
  MakeMat();
  CalcMat2();
  GeneMat();{$ifdef disp}write('%');SaveMat('_T2');{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
