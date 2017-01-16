program diandeng;
uses display;

const m=1000;
type TMat=bitpacked array[0..m+1,0..m+1]of boolean;
var ma,mb,mc,mp:TMat;
var n,l,t:longword;
var i,j,k:longword;

procedure print(m:TMat);
const chm:array[false..true]of char=('.','x');
begin
for j:=1 to n do
  begin
  for i:=1 to n+1 do
    write(chm[m[i,j]]:2);
  writeln();
  end;
writeln();
end;

procedure printpng(m:TMat);
const clm:array[false..true]of longword=(white,black);
var b:pbitmap;
begin
b:=CreateBMP(n,n);
for j:=1 to n do
  for i:=1 to n do
    Bar(b,j-1,n-i,1,1,clm[m[i,j]]);
SaveBMP(b,'png/'+i2s(n)+'.png');
ReleaseBMP(b);
end;

procedure init(var m:TMat);
begin
for j:=0 to n+1 do
  for i:=0 to n+1 do
    m[i,j]:=false;
end;

procedure initE(var m:TMat);
begin
for k:=1 to n do
  m[k,k]:=true;
end;

procedure copy(a:TMat;var b:TMat);
begin
for j:=1 to n do
  for i:=1 to n+1 do
    b[i,j]:=a[i,j];
end;

procedure calc(var a,b,c:TMat);
begin
copy(b,c);
for j:=1 to n do
  for i:=1 to n+1 do
    b[i,j]:=a[i,j] xor c[i,j-1] xor c[i,j] xor c[i,j+1];
for k:=1 to n do
  b[n+1,k]:=not(b[n+1,k]);
copy(c,a);
end;

procedure solve(var m:TMat);
begin
for k:=1 to n do
  begin
  if m[k,k]=false then
    begin
    t:=0;
    for j:=k+1 to n do
      if m[k,j]=true then t:=j;
    if t<>0 then
      for i:=k to n+1 do
        m[i,k]:=m[i,k] xor m[i,t];
    end;
  for j:=k+1 to n do
    if m[k,j]=true then
      for i:=k to n+1 do
        m[i,j]:=m[i,j] xor m[i,k];
  end;
  for k:=n downto 1 do
    begin
    for j:=k-1 downto 1 do
      if m[k,j]=true then
        for i:=k to n+1 do
          m[i,j]:=m[i,j] xor m[i,k];
    end;
end;

procedure make(min:TMat;var mout:TMat);
begin
init(mout);
for j:=1 to n do
  mout[1,j]:=min[n+1,j];
for i:=2 to n do
  for j:=1 to n do
    mout[i,j]:=not(mout[i-1,j-1] xor mout[i-1,j] xor mout[i-1,j+1] xor mout[i-2,j]);
end;

begin
CreateWin(m,m);
for n:=1 to m do
  begin
  init(ma);
  init(mb);
  init(mb);
  initE(mb);
  for l:=0 to n-1 do
    calc(ma,mb,mc);
  solve(mb);
  make(mb,mp);
  printPNG(mp);
  writeln(n);
  end;
//waitkey();
end.
