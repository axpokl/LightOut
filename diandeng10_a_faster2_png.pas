{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=1000;

type TMat=array[-1..m+1,-1..m+1]of Boolean;

var n:longword;
var l,a:TMat;
var i,j,k:longint;

{$ifdef disp}
var bb:pbitbuf;
var s:longword=0;
var b:pbitmap;
{$endif}

procedure PrintMat(mat:TMat);
var i,j:longint;
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

procedure DrawMat();begin DrawMat(l);end;

procedure PrintMat(s:ansistring;mat:TMAT);
begin
DrawMat(mat);
b:=CreateBMP(n,n);
DrawBMP(_pmain,b,0,0,n,n,0,0,n,n);
SaveBMP(b,'png'+s+'/'+i2s(n)+'.png');
ReleaseBMP(b);
end;

procedure PrintMat(s:ansistring);begin PrintMat(s,l);end;
{$endif}

procedure MakeMat();
begin
for i:=0 to n-1 do
  l[n-1,i]:=False;
l[n,0]:=False;
for j:=n-2 downto -1 do
  for i:=0 to n-1 do
    l[j,i]:=not((l[j+1,i] xor l[j+1,i+1]) xor (l[j+1,i-1] xor l[j+2,i]));
for i:=0 to n-1 do
  l[n,i]:=False;
l[n,0]:=True;
for j:=n-1 downto 0 do
  for i:=0 to n-1 do
    l[j,i]:=(l[j+1,i] xor l[j+1,i+1]) xor (l[j+1,i-1] xor l[j+2,i]);
for j:=1 to n-1 do
  for i:=0 to n-1 do
    begin
    l[j,i]:=(l[j-1,i+1] xor l[j-1,i-1]);
    if j>1 then l[j,i]:=l[j,i] xor l[j-2,i];
    end;
for j:=0 to n-1 do if l[-1,j] then l[j,-1]:=True;
for i:=0 to n-1 do l[-1,i]:=False;
for i:=0 to n-1 do for j:=0 to n-1 do a[i,j]:=(i=j);
end;

procedure CalcMat();
var j0:longint;
begin
for k:=0 to n-1 do
  begin
  j0:=-1;
  for j:=n-1 downto k do
    if l[j,k] then j0:=j;
  j:=j0;
  if j>=0 then
    begin
    if j<>k then
      for i:=-1 to n-1 do
        begin
        l[j,i]:=l[j,i] xor l[k,i];
        l[k,i]:=l[j,i] xor l[k,i];
        l[j,i]:=l[j,i] xor l[k,i];
        a[j,i]:=a[j,i] xor a[k,i];
        a[k,i]:=a[j,i] xor a[k,i];
        a[j,i]:=a[j,i] xor a[k,i];
        end;
    for j:=k+1 to n-1 do
      if l[j,k] then
        begin
        for i:=0 to n-1 do //for a-1
          begin
          l[j,i]:=l[j,i] xor l[k,i];
          a[j,i]:=a[j,i] xor a[k,i];
          end;
        l[j,-1]:=l[j,-1] xor l[k,-1];
        a[j,-1]:=a[j,-1] xor a[k,-1];
        end;
    end;
  end;
for i:=n-1 downto 0 do
  if l[i,i] then
    for j:=i-1 downto 0 do
      if l[j,i] then
        begin
        for k:=j to n-1 do
          begin
          l[j,k]:=l[j,k] xor l[i,k];
          a[j,k]:=a[j,k] xor a[i,k];
          end;
        l[j,-1]:=l[j,-1] xor l[i,-1];
        a[j,-1]:=a[j,-1] xor a[i,-1];
        end;
end;

procedure GeneMat();
begin
for i:=0 to n-1 do
  begin
  l[0,i]:=l[i,-1];
  l[i,-1]:=false;
  end;
for j:=1 to n-1 do
  for i:=0 to n-1 do
    l[j,i]:=not(l[j-1,i-1] xor l[j-1,i] xor l[j-1,i+1] xor l[j-2,i]);
end;

begin
{$ifdef disp}
CreateWin(m,m);
bb:=CreateBB(GetWin());
b:=CreateBMP(m,m);
{$endif}
for n:=1 to m do
  begin
  write(n,#9);
  write('m');MakeMat();
  {$ifdef disp}
  write('%');PrintMat('_A');
  //readln();
  {$endif}
  write('c');CalcMat();
  {$ifdef disp}
  write('%');PrintMat('_E');
  write('%');PrintMat('_A-1',a);
  {$endif}
  write('g');GeneMat();
  //write('@');PrintMat();
  {$ifdef disp}
  write('%');PrintMat('');
  write(#9,s,#9,n*n,#9,s/n/n:0:5);
  if not(iswin()) then halt;
  {$endif}
  writeln();
  end;
end.
