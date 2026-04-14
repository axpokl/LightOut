{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=2000;
const sosN=2048;

type TVec=array[-2..m]of boolean;
     TSos=array[0..sosN-1]of byte;

var n:longword;
var i,j:longint;
var x,y,y1,y_,y_1,f,f1:TVec;
var k:longint;
var o:boolean;

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
write('f ');for i:=0 to n do if f[i] then write(1) else write(0);writeln;
end;

function gcd(vf,vg:TVec; var vd,vr:TVec):longint;
var vt,vx,vy:TVec;
var kf,kg:longint;
var done:boolean;
begin
kf:=-1; for i:=n downto 0 do if vf[i] then begin kf:=i; break; end;
kg:=-1; for i:=n downto 0 do if vg[i] then begin kg:=i; break; end;
done:=false;
for i:=0 to n do begin vx[i]:=false; vy[i]:=false; end; vy[0]:=true;
repeat
if kf<kg then begin for i:=0 to n do begin vt[i]:=vf[i]; vf[i]:=vg[i]; vg[i]:=vt[i]; vt[i]:=vx[i]; vx[i]:=vy[i]; vy[i]:=vt[i]; end; j:=kf; kf:=kg; kg:=j; end;
if kg<0 then begin for i:=0 to n do begin vd[i]:=vf[i]; vr[i]:=vx[i]; end; gcd:=kf; done:=true; end;
if not(done) then
  begin
  for i:=n downto (kf-kg) do if vg[i-(kf-kg)] then vf[i]:=vf[i] xor true;
  for i:=n downto (kf-kg) do if vy[i-(kf-kg)] then vx[i]:=vx[i] xor true;
  kf:=-1; for i:=n downto 0 do if vf[i] then begin kf:=i; break; end;
  end;
until done;
end;

procedure CalcMat2;
var c,q,g:TVec;
var v,v0,z:TVec;
var g0,g1,g2:TVec;
var i0,r0,kk,jmax,row1,row2,row3,l0,l1,l2,r1,r2:longint;
begin
BuildC(f,c);
write('c ');for i:=0 to n-1 do if c[i] then write(1) else write(0);writeln;

r0:=gcd(f,c,g,q);
writeln('gcd',#9,r0,#9);
write('q ');for i:=0 to n-1 do if q[i] then write(1) else write(0);writeln;
write('g ');for i:=0 to n do if g[i] then write(1) else write(0);writeln;
for i:=-1 to n do v[i]:=y[i];
write('y ');for i:=0 to n-1 do if v[i] then write(1) else write(0);writeln;
for i:=0 to n do z[i]:=false;
for j:=0 to n-1 do 
  begin
  if q[j] then for i:=0 to n-1 do z[i]:=z[i] xor v[i];
  for i:=0 to n-1 do v0[i]:=v[i-1] xor v[i+1];
  for i:=0 to n-1 do v[i]:=v0[i];
  if VecIsZero(v,n-1) then break;
  end;
if r0=0 then
  for i:=0 to n-1 do x[i]:=z[i]
else
begin
write('z ');for i:=0 to n-1 do if z[i] then write(1) else write(0);writeln;
for i:=-2 to n do begin g0[i]:=false; g1[i]:=false; g2[i]:=false; v[i]:=false; v0[i]:=false; end;
v[0]:=true;
for j:=0 to r0 do 
  begin
  if g[j] then for i:=0 to n-1 do g0[i]:=g0[i] xor v[i];
  for i:=0 to n-1 do v0[i]:=v[i-1] xor v[i+1];
  for i:=-2 to n do v[i]:=v0[i];
  if VecIsZero(v,n-1) then break;
  end;
if n-r0-1<0 then jmax:=0 else jmax:=n-r0-1;
for i:=-2 to n do v[i]:=g0[i];
writeln('d');
write(0,#9);for i:=0 to n-1 do if g0[i] then write(1) else write(0);writeln;
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
    write(j,#9);for i:=0 to n-1 do if g0[i] then write(1) else write(0);writeln;
    g2:=g1;
    g1:=g0;
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
    for j:=l1 to r1 do z[j]:=z[j] xor g1[j];
    x[i0]:=true;
for kk:=0 to n-1 do if g1[kk] then write(1) else write(0);write(#9);
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

{
for i:=-1 to n do v[i]:=y[i];
write('y ');for i:=0 to n-1 do if v[i] then write(1) else write(0);writeln;

for i:=0 to n-1 do b0[0,i]:=b[n,i];
for j:=1 to n-1 do for i:=0 to n-1 do b0[j,i]:=b0[j-1,i-1] xor b0[j-1,i+1] xor b0[j-2,i];
writeln('b');for j:=0 to n-1 do begin write(j,#9);for i:=0 to n-1 do if b0[j,i] then write(1) else write(0);writeln;end;

for i:=0 to n-1 do begin r[i]:=-1; for j:=0 to n-1 do if b0[j,i] then begin r[i]:=j; break; end; end;
write('r ');for i:=0 to n-1 do write(r[i]);writeln;
for i:=0 to n-1 do x[i]:=false;
for i:=0 to n-1 do
 if v[i] then
 begin
  i0:=-1;
  for j:=0 to n-1 do if r[j]=i then begin i0:=j; break; end;
write(i,#9,i0,#9);
  if i0>=0 then begin
for kk:=0 to n-1 do if v[kk] then write(1) else write(0);write(#9);
  for j:=0 to n-1 do y[j]:=(y[j] or b0[j,i0]) and not (y[j] and b0[j,i0]);
  x[i0]:=not x[i0];
for kk:=0 to n-1 do if b0[kk,i0] then write(1) else write(0);write(#9);
for kk:=0 to n-1 do if v[kk] then write(1) else write(0);write(#9);
for kk:=0 to n-1 do if x[kk] then write(1) else write(0);write(#9);
end;
writeln();
 end;
}

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
