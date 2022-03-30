program diandeng;
uses display;

const m=1000;
var n:longword;
var lk:array[-1..m,-2..m,-1..m]of boolean;
var lb:array[-1..m,-1..m]of boolean;
var l:array[-1..m,-2..m]of boolean;
var i,j,k:longint;

procedure PrintMat();
var i,j,k:longint;
begin
writeln();
for j:=0 to n-1 do
  begin
  if l[j,-1] then write('#') else write(' ');
  for i:=0 to n-1 do
    if l[j,i] then write('#') else write(' ');
  writeln();
  end;
end;

procedure InitMat();
begin
for j:=0 to n-1 do
  begin
  for i:=-1 to n-1 do
    lk[j,i,0]:=false;
  lk[j,j,0]:=true;
  for k:=1 to n do
    lb[j,k]:=true;
  end;
end;

procedure MakeMat(j,k:longint);
begin
if (k>0) and (j>=0) and (j<n) then
  begin
  if lb[j,k-2]=true then MakeMat(j,k-2);
  if lb[j,k-1]=true then MakeMat(j,k-1);
  if lb[j-1,k-1]=true then MakeMat(j-1,k-1);
  if lb[j+1,k-1]=true then MakeMat(j+1,k-1);
  for i:=-1 to n-1 do
    lk[j,i,k]:=lk[j-1,i,k-1] xor lk[j,i,k-1] xor lk[j+1,i,k-1] xor lk[j,i,k-2] xor (i=-1);
  lb[j,k]:=false;
  end;
end;

procedure MakeMat();
begin
for j:=0 to n-1 do
  MakeMat(j,n);
for j:=0 to n-1 do
  for i:=-1 to n-1 do
    l[j,i]:=lk[j,i,k];
end;

procedure CalcMat();
var j0:longint;
begin
for k:=0 to n-1 do
  begin
  j0:=-1;
  for j:=n-1 downto k do
    if l[j,k]=true then j0:=j;
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
      if l[j,k]=true then
        begin
        for i:=k to n-1 do
          l[j,i]:=l[j,i] xor l[k,i];
        l[j,-1]:=l[j,-1] xor l[k,-1];
        end;
    end;
  end;
for i:=n-1 downto 0 do
  if l[i,i]=true then
    for j:=i-1 downto 0 do
      if l[j,i]=true then
        begin
        l[j,i]:=false;
        l[j,-1]:=l[j,-1] xor l[i,-1];
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
for n:=1 to m do
  begin
  write(n,#9);
  write('i');InitMat();
  write('m');MakeMat();
  write('c');CalcMat();
  write('g');GeneMat();
  //write('#');PrintMat();
  writeln('');
  end;
end.
