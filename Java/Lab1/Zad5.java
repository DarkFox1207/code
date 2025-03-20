import FirstPackage.SecondClass;

class FirstClass {
    public static void main(String[] args) {
        SecondClass o=new SecondClass(1, 2);
        int i, j;
        for(i=1;i<=8;i++){
            for(j=1;j<=8;j++){
                o.setNum1(i);
                o.setNum2(j);
                System.out.print(o.add());
                System.out.print(" ");
            }
            System.out.println();
        }
    }
}