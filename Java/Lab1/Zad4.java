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

class SecondClass {   

    // Приватные поля типа int
    private int num1;
    private int num2;

    // Конструктор, инициализирующий значения полей
    public SecondClass(int num1, int num2) {
        this.num1 = num1;
        this.num2 = num2;
    }

    // Методы для получения значения num1 и num 2
    public int getNum1() {
        return num1;
    }

    public int getNum2() {
        return num2;
    }

    // Методы для установки значения num1 и num 2
    public void setNum1(int num1) {
        this.num1 = num1;
    }

    public void setNum2(int num2) {
        this.num2 = num2;
    }

    // Метод, выполняющий сложение двух чисел um1 и num2
    public int add() {
        return num1 + num2;
    }

}
