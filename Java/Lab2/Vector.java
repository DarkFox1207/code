public class Vector {
    private final double[] elements;

    public Vector(double[] elements) {
        this.elements = elements.clone();
    }

    // Доступ к элементам вектора
    public double getElement(int index) {
        return elements[index];
    }

    public void setElement(int index, double value) {
        elements[index] = value;
    }

    // Получение длины вектора
    public int length() {
        return elements.length;
    }

    // Поиск минимального значения
    public double min() {
        double min = elements[0];
        for (int i = 1; i < elements.length; i++) {
            if (elements[i] < min) min = elements[i];
        }
        return min;
    }

    // Поиск максимального значения
    public double max() {
        double max = elements[0];
        for (int i = 1; i < elements.length; i++) {
            if (elements[i] > max) max = elements[i];
        }
        return max;
    }

    // Сортировка вектора по возрастанию
    public void sort() {
        for (int i = 0; i < elements.length - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < elements.length; j++) {
                if (elements[j] < elements[minIndex]) {
                    minIndex = j;
                }
            }
            double temp = elements[i];
            elements[i] = elements[minIndex];
            elements[minIndex] = temp;
        }
    }

    // Нахождение евклидовой нормы
    public double evnorm() {
        double sum = 0;
        for (double e : elements) {
            sum += e * e;
        }
        return Math.sqrt(sum);
    }

    // Умножение вектора на число
    public Vector multiply(double scalar) {
        double[] result = new double[elements.length];
        for (int i = 0; i < elements.length; i++) {
            result[i] = elements[i] * scalar;
        }
        return new Vector(result);
    }

    // Сложение двух векторов
    public Vector add(Vector other) {
        if (this.length() != other.length()) {
            throw new IllegalArgumentException("Векторы должны быть одной длины");
        }
        double[] result = new double[elements.length];
        for (int i = 0; i < elements.length; i++) {
            result[i] = this.elements[i] + other.elements[i];
        }
        return new Vector(result);
    }

    // Нахождение скалярного произведения
    public Vector multiply(Vector other) {
        if (this.length() != other.length()) {
            throw new IllegalArgumentException("Векторы должны быть одной длины");
        }
        double[] result = new double[elements.length];
        for (int i = 0; i < elements.length; i++) {
            result[i] = this.elements[i] * other.elements[i];
        }
        return new Vector(result);
    }

    // Вывод элементов вектора в консоль в одну строку, разделяя их пробелами
    public void print() {
        for (double e : elements) {
            System.out.print(e + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        double[] data1 = {3.0, 1.0, 4.0, 1.5};
        double[] data2 = {2.0, 3.5, 0.5, 1.0};
        
        Vector v1 = new Vector(data1);
        Vector v2 = new Vector(data2);

        System.out.println("Вектор 1:");
        v1.print();
        System.out.println("Вектор 2:");
        v2.print();

        System.out.println("Элемент с индексом 2: " + v1.getElement(2));

        v1.setElement(2, 5.0);
        System.out.println("После установки элемента с индексом 2 в 5.0:");
        v1.print();

        System.out.println("Длина вектора: " + v1.length());
        System.out.println("Минимальный элемент: " + v1.min());
        System.out.println("Максимальный элемент: " + v1.max());

        v1.sort();
        System.out.println("Отсортированный вектор:");
        v1.print();

        System.out.println("Евклидова норма: " + v1.evnorm());
        
        Vector v3 = v1.multiply(2);
        System.out.println("Умножение вектора 1 на 2:");
        v3.print();

        System.out.println("Сложение вектора 1 и 2:");
        Vector sumVector = v1.add(v2);
        sumVector.print();

        System.out.println("Покомпонентное умножение вектора 1 и 2:");
        Vector v4 = v1.multiply(v2);
        v4.print();
    }
}
