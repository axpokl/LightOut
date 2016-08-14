program diandeng;
uses display;
const maxn=200;
var a:packed array[1..maxn*maxn,1..maxn*maxn+1]of boolean;
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

const ac:array[boolean]of longword=(black,white);

procedure outputall();
var i,j:longword;
var b:pbitmap;
begin
for j:=1 to m do
  for i:=1 to m+1 do
    SetPixel(i,j,ac[a[j,i]]);
while IsNextMsg do ;
freshwin();
end;

procedure outputpng();
var i:longword;
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
createwin(maxn,maxn);
for k:=1 to 200 do
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
    for j:=max(1,i-w-w) to min(i+w+w,m) do
      begin
      l:=i-j;
      if (l=0)
      or ((l=-1) and not(j mod w=1))
      or ((l=1) and not(j mod w=0))
      or (l=w)
      or (l=-w)
      then
        a[i,j]:=true
      else
        a[i,j]:=false;
      end;
//����������þ���ĳ�ʼ״̬��
//a[i,m+1]�е�i�����i���ơ�
  for i:=1 to m do
    a[i,m+1]:=true;
//�����￪ʼ�����Է����顣����Ĳ��ֲ����޸ġ�
write('@');
  for j:=1 to m do
    begin
//outputall();waitkey();
while IsNextMsg do ;
    if a[j,j]=false then
      begin
      t:=0;
      for i:=min(j+h,m) downto j+1 do
        if a[i,j]=true then t:=i;
      if t<>0 then
        begin
        for l:=j to min(j+w+w,m) do
          a[j,l]:=a[t,l] xor a[j,l];
        l:=m+1;
          a[j,l]:=a[t,l] xor a[j,l];
        end;
      end;
while IsNextMsg do ;
    for i:=j+1 to min(j+h,m) do
      if a[i,j]=true then
        begin
        for l:=j to min(j+w+w,m) do
          a[i,l]:=a[j,l] xor a[i,l];
        l:=m+1;
          a[i,l]:=a[j,l] xor a[i,l];
        end;
    end;
write('#');
//  outputpng();
  for j:=m downto 1 do
    begin
//outputall();waitkey();
while IsNextMsg do ;
    for i:=j-1 downto max(j-h-h,1) do
      if a[i,j]=true then
        begin
        l:=j;
          a[i,l]:=a[j,l] xor a[i,l];
        l:=m+1;
          a[i,l]:=a[j,l] xor a[i,l];
        end;
    end;
write('$');
  outputpng();
//���Է�������꣬������������ȡ�
  s:=0;
  for i:=1 to m do if a[i,i]=false then s:=s+1;
//s=n�������黹��n��δ֪�����򷽳���2^n���⡣
//  append(f);
//  writeln(f,k:5,s:15);
//  close(f);
end;
writeln('end');
readln();
end.
