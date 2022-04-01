//{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=2000;
var n:longword;
var l:array[-1..m+1,-1..(m-1) shr 5+1]of longword;
var i,j,k:longint;

{$ifdef disp}
var bb:pbitbuf;
var s:longword;
{$endif}

procedure PrintMat();
var i,j:longint;
begin
writeln();
for j:=-1 to n-1 do
  begin
  if l[j,-1]>0 then write('#') else write('.');
  for i:=0 to n-1 do
    if l[j,i shr 5] and longword(1 shl (i and 31))>0 then write('#') else write('.');
  writeln();
  end;
end;

{$ifdef disp}
procedure DrawMat();
begin
while IsNextMsg() do ;
for j:=0 to n-1 do
  for i:=0 to n-1 do
    if l[j,i shr 5] and longword(1 shl (i and 31))>0 then
      SetBBPixel(bb,i,j,black)
    else
      SetBBPixel(bb,i,j,white);
SetBB(bb);
FreshWin();
end;
{$endif}

procedure MakeMat();
begin
for i:=0 to (n-1) shr 5 do
  l[n-1,i]:=0;
l[n,0]:=0;
for j:=n-2 downto -1 do
  begin
  for i:=0 to (n-1) shr 5 do
    l[j,i]:=not(l[j+1,i] xor (l[j+1,i+1] shl 31 or l[j+1,i] shr 1) xor (l[j+1,i-1] shr 31 or l[j+1,i] shl 1) xor l[j+2,i]);
  l[j,i]:=l[j,i] and (1 shl (n and 31)-1);
  end;
for i:=0 to (n-1) shr 5 do
  l[n,i]:=0;
l[n,0]:=1;
for j:=n-1 downto 0 do
  begin
  for i:=0 to (n-1) shr 5 do
    l[j,i]:=l[j+1,i] xor (l[j+1,i+1] shl 31 or l[j+1,i] shr 1) xor (l[j+1,i-1] shr 31 or l[j+1,i] shl 1) xor l[j+2,i];
  l[j,i]:=l[j,i] and (1 shl (n and 31)-1);
  end;
for j:=1 to n-1 do
  begin
  for i:=0 to (n-1) shr 5 do
    begin
    l[j,i]:=(l[j-1,i+1] shl 31 or l[j-1,i] shr 1) xor (l[j-1,i-1] shr 31 or l[j-1,i] shl 1);
    if j>1 then l[j,i]:=l[j,i] xor l[j-2,i];
    end;
  l[j,i]:=l[j,i] and (1 shl (n and 31)-1);
  end;
for j:=0 to n-1 do
  if l[-1,j shr 5] and longword(1 shl (j and 31))>0 then l[j,-1]:=1;
for i:=0 to (n-1) shr 5 do
  l[-1,i]:=0;
end;

procedure CalcMat();
var j0:longint;
begin
for k:=0 to n-1 do
  begin
  j0:=-1;
  for j:=n-1 downto k do
    if l[j,k shr 5] and longword(1 shl (k and 31))>0 then j0:=j;
  j:=j0;
  if j>=0 then
    begin
    if j<>k then
      for i:=-1 to (n-1) shr 5 do
        begin
        l[j,i]:=l[j,i] xor l[k,i];
        l[k,i]:=l[j,i] xor l[k,i];
        l[j,i]:=l[j,i] xor l[k,i];
//尝试不交换，用标记
        end;
    for j:=k+1 to n-1 do
      if l[j,k shr 5] and longword(1 shl (k and 31))>0 then
        begin
        for i:=k shr 5 to (n-1) shr 5 do
          l[j,i]:=l[j,i] xor l[k,i];
        l[j,-1]:=l[j,-1] xor l[k,-1];
//尝试多线程
        end;
    end;
  end;
for i:=n-1 downto 0 do
  if l[i,i shr 5] and longword(1 shl (i and 31))>0 then
    for j:=i-1 downto 0 do
      if l[j,i shr 5] and longword(1 shl (i and 31))>0 then
        begin
        l[j,i shr 5]:=l[j,i shr 5] xor longword(1 shl (i and 31));
        l[j,-1]:=l[j,-1] xor l[i,-1];
//尝试位运算
        end;
end;

procedure GeneMat();
begin
for i:=0 to (n-1) shr 5 do
  l[0,i]:=0;
for j:=0 to n-1 do
  begin
  l[0,j shr 5]:=l[0,j shr 5] xor longword(l[j,-1] shl (j and 31));
  l[j,-1]:=0;
  end;
for j:=1 to n-1 do
  begin
  for i:=0 to (n-1) shr 5 do
    l[j,i]:=not(l[j-1,i] xor (l[j-1,i+1] shl 31 or l[j-1,i] shr 1) xor (l[j-1,i-1] shr 31 or l[j-1,i] shl 1) xor l[j-2,i]);
  l[j,i]:=l[j,i] and (1 shl (n and 31)-1);
  end;
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
  write('c');CalcMat();
  write('g');GeneMat();
  //write('@');PrintMat();
  {$ifdef disp}
  write('%');DrawMat();
  write(#9,s,#9,n*n,#9,s/n/n:0:5);
  {$endif}
  writeln();
  end;
end.
