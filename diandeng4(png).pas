program diandeng;
uses display;
var a:array[1..100*100,1..100*100+1]of shortint;
    i,j,k,l:longint;
    f:text;
    h,w,m,t:longint;
    s:longint;

             {
procedure output;
begin
append(f);
writeln(f,'#####################');
for i:=1 to m do
  begin
  if a[i,m+1]=0 then write(f,'��') else write(f,'��');
  if (i mod w=0) then writeln(f);
  end;
close(f);
end;          }

const ac:array[0..1]of longword=(black,white);

procedure outputpng();
var b:pbitmap;
begin
for i:=1 to m do SetPixel((i-1)mod w,(i-1)div w,ac[a[i,m+1]]);
while IsNextMsg do ;
freshwin();
b:=CreateBMP(w,h);
DrawBMP(_pmain,b,0,0,w,h,0,0,w,h);
SaveBMP(b,'png/'+i2s(w)+'.png');
ReleaseBMP(b);
end;

begin
//assign(f,'diandeng.txt');
//rewrite(f);
//close(f);
createwin();
for k:=1 to 100 do
  begin
  writeln('start: ',k);
  w:=k;
  h:=k;
  m:=w*h;
//�����￪ʼ�������Է�������
//�������ų�һ���У���1��25=m��
//j�д���ť��i�д���ơ�
//a[i,j]=1��������j����ť��򿪵�i���ơ�
//�����а�ť���������ã���ťҲ��1��25=m����
  for i:=1 to m do
    for j:=1 to m do
      begin
      l:=i-j;
      if (l=0)
      or ((l=-1) and not(j mod w=1))
      or ((l=1) and not(j mod w=0))
      or (l=w)
      or (l=-w)
      then
        a[i,j]:=1
      else
        a[i,j]:=0;
      end;
//����������þ���ĳ�ʼ״̬��
//a[i,m+1]�е�i�����i���ơ�
  for i:=1 to m do
    a[i,m+1]:=1;
//�����￪ʼ�����Է����顣����Ĳ��ֲ����޸ġ�
write('@');
  for j:=1 to m do
    begin
while IsNextMsg do ;
    if a[j,j]=0 then
      begin
      t:=0;
      for i:=j+1 to m do
        if a[i,j]=1 then t:=i;
      if t<>0 then
        for l:=j to m+1 do
          a[j,l]:=a[t,l] xor a[j,l];
      end;
while IsNextMsg do ;
    for i:=j+1 to m do
      if a[i,j]=1 then
        for l:=j to m+1 do
          a[i,l]:=a[j,l] xor a[i,l];
    end;
write('#');
//  outputpng();
  for j:=m downto 1 do
    begin
while IsNextMsg do ;
    for i:=j-1 downto 1 do
      if a[i,j]=1 then
        for l:=j to m+1 do
          a[i,l]:=a[j,l] xor a[i,l];
    end;
write('$');
  outputpng();
//���Է�������꣬������������ȡ�
  s:=0;
  for i:=1 to m do if a[i,i]=0 then s:=s+1;
//s=n�������黹��n��δ֪�����򷽳���2^n���⡣
//  append(f);
//  writeln(f,k:5,s:15);
//  close(f);
end;
writeln('end');
readln();
end.
