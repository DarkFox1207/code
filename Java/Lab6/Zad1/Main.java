import java.util.Iterator;
import java.util.NoSuchElementException;

// Интерфейс коллекции
interface MyCollection<T> extends Iterable<T> {
    void add(T element); // Добавление элемента
    int size(); // Получение размера коллекции
    Iterator<T> iterator(); // Метод итератора
}

// Общий итератор
class CommonIterator<T> implements Iterator<T> {
    private final T[] elements; // Массив элементов
    private int currentIndex = 0; // Текущий индекс

    public CommonIterator(T[] elements) {
        this.elements = elements;
    }

    @Override
    public boolean hasNext() {
        // Проверяем, есть ли следующий элемент
        return currentIndex < elements.length && elements[currentIndex] != null;
    }

    @Override
    public T next() {
        if (!hasNext()) {
            throw new NoSuchElementException("Нет больше элементов");
        }
        return elements[currentIndex++]; // Возвращаем текущий элемент и увеличиваем индекс
    }

    @Override
    public void remove() {
        throw new UnsupportedOperationException("Метод remove не поддерживается");
    }
}

// Реализация списка
class MyList<T> implements MyCollection<T> {
    private T[] elements; // Массив элементов
    private int size; // Текущий размер коллекции

    @SuppressWarnings("unchecked")
    public MyList() {
        elements = (T[]) new Object[10]; // Начальный размер массива
        size = 0;
    }

    @Override
    public void add(T element) {
        if (size == elements.length) {
            // Увеличиваем массив, если он заполнен
            resizeArray();
        }
        elements[size++] = element; // Добавляем элемент
    }

    @SuppressWarnings("unchecked")
    private void resizeArray() {
        T[] newElements = (T[]) new Object[elements.length * 2];
        System.arraycopy(elements, 0, newElements, 0, elements.length);
        elements = newElements;
    }

    @Override
    public int size() {
        return size; // Возвращаем размер коллекции
    }

    @Override
    public Iterator<T> iterator() {
        return new CommonIterator<>(elements); // Возвращаем итератор
    }
}

// Реализация множества
class MySet<T> implements MyCollection<T> {
    private T[] elements; // Массив элементов
    private int size; // Текущий размер коллекции

    @SuppressWarnings("unchecked")
    public MySet() {
        elements = (T[]) new Object[10]; // Начальный размер массива
        size = 0;
    }

    @Override
    public void add(T element) {
        if (!contains(element)) { // Проверяем, есть ли элемент в коллекции
            if (size == elements.length) {
                // Увеличиваем массив, если он заполнен
                resizeArray();
            }
            elements[size++] = element; // Добавляем элемент
        }
    }

    @SuppressWarnings("unchecked")
    private void resizeArray() {
        T[] newElements = (T[]) new Object[elements.length * 2];
        System.arraycopy(elements, 0, newElements, 0, elements.length);
        elements = newElements;
    }

    private boolean contains(T element) {
        for (int i = 0; i < size; i++) {
            if (elements[i] != null && elements[i].equals(element)) {
                return true;
            }
        }
        return false;
    }

    @Override
    public int size() {
        return size; // Возвращаем размер коллекции
    }

    @Override
    public Iterator<T> iterator() {
        return new CommonIterator<>(elements); // Возвращаем итератор
    }
}

// Пример использования
public class Main {
    public static void main(String[] args) {
        // Пример с MyList
        MyCollection<String> list = new MyList<>();
        list.add("A");
        list.add("B");
        list.add("C");

        System.out.println("Элементы MyList:");
        for (String element : list) {
            System.out.println(element);
        }

        // Пример с MySet
        MyCollection<String> set = new MySet<>();
        set.add("X");
        set.add("Y");
        set.add("X"); // Дубликат не добавится

        System.out.println("Элементы MySet:");
        for (String element : set) {
            System.out.println(element);
        }
    }
}