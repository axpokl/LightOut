program diandeng;
var a:array[1..100*100,1..100*100+1]of shortint;
    i,j,k,l:longint;
    f:text;
    h,w,m,t:longint;
    s:longint;


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
end;

begin
assign(f,'diandeng.txt');
rewrite(f);
close(f);
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
  for j:=1 to m do
    begin
    if a[j,j]=0 then
      begin
      t:=0;
      for i:=j+1 to m do
        if a[i,j]=1 then t:=i;
      if t<>0 then
        for l:=j to m+1 do
          a[j,l]:=a[t,l] xor a[j,l];
      end;
    for i:=j+1 to m do
      if a[i,j]=1 then
        for l:=j to m+1 do
          a[i,l]:=a[j,l] xor a[i,l];
    end;
    {
  output();}
  for j:=m downto 1 do
    begin
    for i:=j-1 downto 1 do
      if a[i,j]=1 then
        for l:=j to m+1 do
          a[i,l]:=a[j,l] xor a[i,l];
    end;

  output();
//���Է�������꣬������������ȡ�
  s:=0;
  for i:=1 to m do if a[i,i]=0 then s:=s+1;
//s=n�������黹��n��δ֪�����򷽳���2^n���⡣
  append(f);
  writeln(f,k:5,s:15);
  close(f);
end;
writeln('end');
readln();
end.
