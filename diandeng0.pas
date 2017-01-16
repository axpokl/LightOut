var switch,light:array[0..6,0..6]of boolean;
var n,k:longword;
var x,y:longword;
var fine:boolean;
begin
for n:=0 to 33554432-1 do
  begin
  k:=n;
  for x:=1 to 5 do
    for y:=1 to 5 do
     begin
     switch[x,y]:=(k and 1)=1;
     k:=k shr 1;
     end;
  for x:=1 to 5 do
    for y:=1 to 5 do
      light[x,y]:=switch[x,y] xor switch[x-1,y] xor
                  switch[x+1,y] xor switch[x,y-1] xor switch[x,y+1];
  fine:=true;
  for x:=1 to 5 do
    for y:=1 to 5 do
      fine:=fine and light[x,y];
  if fine then
    begin
    for x:=1 to 5 do
      begin
      for y:=1 to 5 do
        begin
        if switch[x,y] then write('*') else write(' ');
        end;
      writeln();
      end;
    writeln('###########');
    end;
  end;
end.