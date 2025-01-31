{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=2000;
var n:longword;
var l:array[-1..m+1,-1..m+1]of Boolean;
var i,j,k:longint;

{$ifdef disp}
var bb:pbitbuf;
var s:longword=0;
{$endif}

procedure PrintMat();
var i,j:longint;
begin
writeln();
for j:=-1 to n-1 do
  begin
  if l[j,-1] then write('#') else write('.');
  for i:=0 to n-1 do
    if l[j,i] then write('#') else write('.');
  writeln();
  end;
end;

{$ifdef disp}
procedure DrawMat();
begin
while IsNextMsg() do ;
for j:=0 to n-1 do
  for i:=0 to n-1 do
    if l[j,i] then SetBBPixel(bb,i,j,black) else SetBBPixel(bb,i,j,white);
SetBB(bb);
FreshWin();
end;
{$endif}

procedure MakeMat();
begin
for i:=0 to n-1 do
  l[n-1,i]:=False;
l[n,0]:=False;
for j:=n-2 downto -1 do
  begin
  for i:=0 to n-1 do
    l[j,i]:=not((l[j+1,i] xor l[j+1,i+1]) xor (l[j+1,i-1] xor l[j+2,i]));
  l[j,i]:=l[j,i];
  end;
for i:=0 to n-1 do
  l[n,i]:=False;
l[n,0]:=True;
for j:=n-1 downto 0 do
  begin
  for i:=0 to n-1 do
    l[j,i]:=(l[j+1,i] xor l[j+1,i+1]) xor (l[j+1,i-1] xor l[j+2,i]);
  l[j,i]:=l[j,i];
  end;
for j:=1 to n-1 do
  begin
  for i:=0 to n-1 do
    begin
    l[j,i]:=(l[j-1,i+1] xor l[j-1,i-1]);
    if j>1 then l[j,i]:=l[j,i] xor l[j-2,i];
    end;
  l[j,i]:=l[j,i];
  end;
for j:=0 to n-1 do if l[-1,j] then l[j,-1]:=True;
for i:=0 to n-1 do l[-1,i]:=False;
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
        end;
    for j:=k+1 to n-1 do
      if l[j,k] then
        begin
        for i:=k to n-1 do
          l[j,i]:=l[j,i] xor l[k,i];
        l[j,-1]:=l[j,-1] xor l[k,-1];
        end;
    end;
  end;
for i:=n-1 downto 0 do
  if l[i,i] then
    for j:=i-1 downto 0 do
      if l[j,i] then
        l[j,-1]:=l[j,-1] xor l[i,-1];
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
{$endif}
for n:=1 to m do
  begin
  write(n,#9);
  write('m');MakeMat();
  {$ifdef disp}
  //write('%');DrawMat();
  //readln();
  {$endif}
  write('c');CalcMat();
  write('g');GeneMat();
  //write('@');PrintMat();
  {$ifdef disp}
  write('%');DrawMat();
  write(#9,s,#9,n*n,#9,s/n/n:0:5);
  if not(iswin()) then halt;
  {$endif}
  writeln();
  end;
end.
