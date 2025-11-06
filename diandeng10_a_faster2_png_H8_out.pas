{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=1000;

type TMat=array[-1..m,-1..m]of Boolean;
type TVec=array[-1..m]of boolean;
type TVeci=array[-1..m]of longint;

var n:longword;
var b,l,t,f,e,h:TMat;
var i,j:longint;

{$ifdef disp}
var bb:pbitbuf;
var bp:pbitmap;
{$endif}

procedure PrintMat(mat:TMat);
begin
writeln();
for j:=0 to n-1 do
  begin
//  if mat[j,-1] then write('#') else write('.');
  for i:=0 to n-1 do
    if mat[j,i] then write('#') else write('.');
  writeln();
  end;
writeln();
end;

{$ifdef disp}
procedure DrawMat(mat:TMat);
begin
while IsNextMsg() do ;
for j:=0 to n-1 do
  for i:=0 to n-1 do
    if mat[j,i] then SetBBPixel(bb,i,j,black) else SetBBPixel(bb,i,j,white);
SetBB(bb);
FreshWin();
end;

procedure PrintMat(s:ansistring;mat:TMAT);
begin
DrawMat(mat);
bp:=CreateBMP(n,n);
DrawBMP(_pmain,bp,0,0,n,n,0,0,n,n);
SaveBMP(bp,'png'+s+'/'+i2s(n)+'.png');
ReleaseBMP(bp);
end;
{$endif}

procedure MakeMat();
begin
for i:=0 to n-1 do l[0,i]:=False;
for j:=1 to n do
  for i:=0 to n-1 do
    l[j,i]:=not(l[j-1,i-1] xor l[j-1,i] xor l[j-1,i+1] xor l[j-2,i]);
for j:=0 to n do if b[j,j]=false then
  if b[0,0]=false then b[0,0]:=true
  else for i:=0 to j do b[j,i]:=b[j-1,i-1] xor b[j-1,i] xor b[j-1,i+1] xor b[j-2,i];
write('b ');for i:=0 to n-1 do if b[n,i] then write(1) else write(0);writeln;
for j:=0 to n do if f[j,j]=false then
  if f[0,0]=false then f[0,0]:=true
  else for i:=0 to j do f[j,i]:=f[j-1,i-1] xor f[j-2,i];
write('f ');for i:=0 to n do if f[n,i] then write(1) else write(0);writeln;
for j:=0 to n do if e[j,j]=false then
  if e[0,0]=false then e[0,0]:=true
  else for i:=0 to j do e[j,i]:=e[j-1,i-1] xor e[j-1,i+1];
write('e ');for i:=0 to n-1 do if e[n,i] then write(1) else write(0);writeln;
end;

function gcd(vf,vg:TVEC; var vr:TVEC):longint;
var cn:TVEC;
var kg,kf,kt:longint;
begin
kf:=-1; for i:=n downto 0 do if vf[i] then begin kf:=i; break; end;
kg:=-1; for i:=n downto 0 do if vg[i] then begin kg:=i; break; end;
if kf<0 then begin for i:=0 to n do vr[i]:=vg[i]; gcd:=kg; exit; end;
if kg<0 then begin for i:=0 to n do vr[i]:=vf[i]; gcd:=kf; exit; end;
if kf<kg then begin for i:=0 to n do begin cn[i]:=vf[i]; vf[i]:=vg[i]; vg[i]:=cn[i];end; j:=kf; kf:=kg; kg:=j; end;
repeat
 kt:=-1;
 for i:=0 to kf do
  begin
   if i>=(kf-kg) then vf[i]:=vf[i] xor vg[i-(kf-kg)];
   if vf[i] then kt:=i;
  end;
 if kt=-1 then begin for i:=0 to n do vr[i]:=vg[i]; gcd:=kg; exit; end
 else if kt<kg then begin for i:=0 to n do begin cn[i]:=vf[i]; vf[i]:=vg[i]; vg[i]:=cn[i]; end; kf:=kg; kg:=kt; end
 else kf:=kt;
until false;
end;

procedure rev(vf,vg:TVec;var vr:TVec);
var kf,kg,sh:longint;
var done:boolean;
var vt,vx,vy:TVec;
begin
for i:=0 to n do begin vx[i]:=false; vy[i]:=false; end;vy[0]:=true;
kf:=-1; for i:=n downto 0 do if vf[i] then begin kf:=i; break; end;
kg:=-1; for i:=n downto 0 do if vg[i] then begin kg:=i; break; end;
done:=false;
while not done do
  begin
  if kf<0 then begin for i:=0 to n do vr[i]:=vy[i]; done:=true; end
  else if kg<0 then begin for i:=0 to n do vr[i]:=vx[i]; done:=true; end
  else
    begin
    if kf<kg then begin for i:=0 to n do begin vt[i]:=vf[i]; vf[i]:=vg[i]; vg[i]:=vt[i]; vt[i]:=vx[i]; vx[i]:=vy[i]; vy[i]:=vt[i]; end; j:=kf; kf:=kg; kg:=j; end;
    sh:=kf-kg;
    for i:=n downto sh do if vg[i-sh] then vf[i]:=vf[i] xor true;
    for i:=n downto sh do if vy[i-sh] then vx[i]:=vx[i] xor true;
    kf:=-1; for i:=n downto 0 do if vf[i] then begin kf:=i; break; end;
    end;
  end;
end;

procedure CalcMat2;
var p,q,x,y,z,c,g:TVec;
var r:TVeci;
var k:longint;
begin
for i:=0 to n do p[i]:=false;
for j:=0 to n-1 do if b[n,j] then for i:=0 to n-1 do p[i]:=p[i] xor f[j,i];
write('p ');for i:=0 to n-1 do if p[i] then write(1) else write(0);writeln;
rev(f[n],p,q);
write('q ');for i:=0 to n-1 do if q[i] then write(1) else write(0);writeln;
for i:=0 to n do y[i]:=l[n,i];
write('y ');for i:=0 to n-1 do if y[i] then write(1) else write(0);writeln;
for i:=0 to n do z[i]:=false;
for j:=0 to n-1 do 
  begin
  if q[j] then for i:=0 to n-1 do z[i]:=z[i] xor y[i];
  for i:=0 to n-1 do c[i]:=y[i-1] xor y[i+1];
  for i:=0 to n-1 do y[i]:=c[i];
  end;
write('z ');for i:=0 to n-1 do if z[i] then write(1) else write(0);writeln;
writeln('gcd',#9,gcd(f[n],p,g),#9);
write('g ');for i:=0 to n do if g[i] then write(1) else write(0);writeln;
for i:=0 to n-1 do h[0,i]:=false;
for j:=0 to n-1 do if g[j] then for i:=0 to n-1 do h[0,i]:=h[0,i] xor e[j,i];
write('h0 ');for i:=0 to n-1 do if h[0,i] then write(1) else write(0);writeln;
for j:=1 to n-1 do for i:=0 to n-1 do h[j,i]:=h[j-1,i-1] xor h[j-1,i+1] xor h[j-2,i];
write('hn ');for i:=0 to n-1 do if h[n-1,i] then write(1) else write(0);writeln;
for j:=0 to n-1 do begin r[j]:=-1; for i:=0 to n-1 do if h[i,j] then begin r[j]:=i; break; end; end;
write('r ');for i:=0 to n-1 do write(r[i]);writeln;
for j:=0 to n-1 do x[j]:=false;
for i:=0 to n-1 do
 if z[i] then
 begin
  k:=-1;
  for j:=i to n-1 do if r[j]=i then begin k:=j; break; end;
  if k<0 then break;
  for j:=0 to n-1 do z[j]:=z[j] xor h[j,k];
  x[k]:=not x[k];
 end;
write('x ');for i:=0 to n-1 do if x[i] then write(1) else write(0);writeln;
for i:=0 to n-1 do t[0,i]:=x[i];
end;

function GeneMat():boolean;
begin
for j:=1 to n-1 do
  for i:=0 to n-1 do
    t[j,i]:=not(t[j-1,i-1] xor t[j-1,i] xor t[j-1,i+1] xor t[j-2,i]);
GeneMat:=true;
for i:=0 to n-1 do GeneMat:=GeneMat and (t[n-1,i-1] xor t[n-1,i] xor t[n-1,i+1] xor t[n-2,i]);
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
  GeneMat();{$ifdef disp}PrintMat('_T2',t);{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
