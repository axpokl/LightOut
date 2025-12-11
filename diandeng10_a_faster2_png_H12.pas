//{$define disp}
program diandeng;

{$ifdef disp}
uses display;
const m=1000;
{$else}
const m=10000;
{$endif}

type TMat=array[-2..m,-2..m]of Boolean;
type TVec=array[-2..m]of boolean;

var n:longword;
var b,l,l0,t,f,k,d,c:TMat;
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
for j:=1 to n do if l0[j,-2]=false then
  begin
  for i:=1 to j-1 do l0[j,i]:=l0[j-1,i-1] xor l0[j-1,i] xor l0[j-1,i+1] xor l0[j-2,i];
  for i:=0 to j-1 do l[j,i]:=not(l[j-1,i-2] xor l[j-1,i-1] xor l[j-1,i] xor l[j-2,i-2] xor l0[j-1,i-1] xor l0[j-1,i] xor l0[j-1,i+1] xor l0[j-2,i-1] xor l0[j-2,i]);
  l0[j,0]:=l[j,0];
  l0[j,-2]:=true;
  end;
for j:=0 to n do if b[j,j]=false then
  if b[0,0]=false then b[0,0]:=true
  else for i:=0 to j do b[j,i]:=b[j-1,i-1] xor b[j-1,i] xor b[j-1,i+1] xor b[j-2,i];
for j:=0 to n do if f[j,j]=false then
  if f[0,0]=false then f[0,0]:=true
  else for i:=0 to j do f[j,i]:=f[j-1,i-1] xor f[j-2,i];
for j:=0 to n do if k[j,j]=false then
  if k[0,0]=false then k[0,0]:=true
  else for i:=0 to j do k[j,i]:=k[j-1,i-1] xor k[j-1,i+1];
for j:=0 to n do if c[j,j]=false then
  if c[0,0]=false then c[0,0]:=true
  else for i:=0 to j do c[j,i]:=c[j-1,i-1] xor c[j-2,i] xor c[j-1,i];
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
var p,q,x,y,z,y0,g:TVec;
var i0,r0:longint;
begin
write('p',#9);
for i:=0 to n do p[i]:=f[n,i] xor c[n,i];
write('q',#9);
r0:=gcd(f[n],p,g,q);
write('gcd',#9,r0,#9);
write('y',#9);
for i:=-1 to n do y[i]:=l[n,i];
write('z',#9);
for i:=0 to n do z[i]:=false;
for j:=0 to n-1 do 
  begin
  if q[j] then for i:=0 to n-1 do z[i]:=z[i] xor y[i];
  for i:=0 to n-1 do y0[i]:=y[i-1] xor y[i+1];
  for i:=0 to n-1 do y[i]:=y0[i];
  end;
if r0=0 then
  begin
  write('x',#9);
  for i:=0 to n-1 do x[i]:=z[i];
  end
else
begin
write('d',#9);
for i:=0 to n-1 do d[0,i]:=false;
for j:=0 to n-1 do if g[j] then for i:=0 to n-1 do d[0,i]:=d[0,i] xor k[j,i];
for j:=1 to n-1 do for i:=0 to n-1 do d[j,i]:=d[j-1,i-1] xor d[j-1,i+1] xor d[j-2,i];
write('x',#9);
for i:=0 to n-1 do x[i]:=false;
for i:=0 to n-1 do
 if z[i] then
 begin
  i0:=i+r0;
  for j:=0 to n-1 do z[j]:=z[j] xor d[j,i0];
  x[i0]:=true;
 end;
end;
write('t',#9);
for i:=0 to n-1 do t[0,i]:=x[i];
end;

function GeneMat():boolean;
begin
for j:=1 to n-1 do
  for i:=0 to n-1 do
    t[j,i]:=not(t[j-1,i-1] xor t[j-1,i] xor t[j-1,i+1] xor t[j-2,i]);
GeneMat:=true;
for i:=0 to n-1 do GeneMat:=GeneMat and (t[n-1,i-1] xor t[n-1,i] xor t[n-1,i+1] xor t[n-2,i]);
write(GeneMat);
end;

begin
{$ifdef disp}
CreateWin(m,m);
bb:=CreateBB(GetWin());
bp:=CreateBMP(m,m);
{$endif}
{$ifdef disp}
for n:=1 to m do
{$else}
for n:=9900 to m do
{$endif}
  begin
  write(n,#9);
  write('m',#9);MakeMat();
  write('c',#9);CalcMat2();
  write('g',#9);GeneMat();{$ifdef disp}write('%');PrintMat('_T2',t);{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
