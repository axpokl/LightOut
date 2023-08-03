uses display;
const m=1024;
var l:array[-1..m,-1..m+1]of boolean;
var j,i:longint;
var bb:pbitbuf;

begin
CreateWin(m,m);
bb:=CreateBB(GetWin());
l[0,0]:=true;
//writeln(0,#9,'#');
for j:=1 to m do
  begin
  write(j,#9);
  for i:=0 to j do
    begin
    l[j,i]:=l[j-1,i-1] xor l[j-1,i] xor l[j-1,i+1] xor l[j-2,i];
    //if l[j,i] then write('#') else write('.');
    if l[j,i] then SetBBPixel(bb,i,j,white) else SetBBPixel(bb,i,j,black);
    end;
  writeln();
  SetBB(bb);FreshWin();While IsNextMsg() do ;
  end;
readln();
end.
