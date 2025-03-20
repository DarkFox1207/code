import java.util.Iterator;
import java.util.NoSuchElementException;

// Интерфейс коллекции
interface MyCollection<T> extends Iterable<T> {
    void add(T element); // Добавление элемента
    int size(); // Получение размера коллекции
    Iterator<T> iterator(); // Метод итератора
}

interface MyCollectionFactory<T> {
    MyCollection<T> createInstance();
    MyCollection<T> createInstance(int initialCapacity);
    MyCollection<T> createInstance(T[] elements);
}

class MyListFactory<T> implements MyCollectionFactory<T> {
    @Override
    public MyCollection<T> createInstance() {
        return new MyList<>(); // Создаем MyList по умолчанию
    }

    @Override
    public MyCollection<T> createInstance(int initialCapacity) {
        MyList<T> list = new MyList<>();
        list.resizeArray(initialCapacity); // Устанавливаем начальную емкость
        return list;
    }

    @Override
    public MyCollection<T> createInstance(T[] elements) {
        MyList<T> list = new MyList<>();
        for (T element : elements) {
            list.add(element); // Добавляем начальные элементы
        }
        return list;
    }
}

class MySetFactory<T> implements MyCollectionFactory<T> {
    @Override
    public MyCollection<T> createInstance() {
        return new MySet<>(); // Создаем MySet по умолчанию
    }

    @Override
    public MyCollection<T> createInstance(int initialCapacity) {
        MySet<T> set = new MySet<>();
        set.resizeArray(initialCapacity); // Устанавливаем начальную емкость
        return set;
    }

    @Override
    public MyCollection<T> createInstance(T[] elements) {
        MySet<T> set = new MySet<>();
        for (T element : elements) {
            set.add(element); // Добавляем начальные элементы
        }
        return set;
    }
}

class Collections {
    private static MyCollectionFactory<?> factory = new MyListFactory<>(); // По умолчанию фабрика для MyList

    // Метод для установки фабрики
    public static <T> void setMyCollectionFactory(MyCollectionFactory<T> factory) {
        Collections.factory = factory;
    }

    // Метод для создания экземпляра коллекции
    @SuppressWarnings("unchecked")
    public static <T> MyCollection<T> createInstance() {
        return ((MyCollectionFactory<T>) factory).createInstance();
    }

    @SuppressWarnings("unchecked")
    public static <T> MyCollection<T> createInstance(int initialCapacity) {
        return ((MyCollectionFactory<T>) factory).createInstance(initialCapacity);
    }

    @SuppressWarnings("unchecked")
    public static <T> MyCollection<T> createInstance(T[] elements) {
        return ((MyCollectionFactory<T>) factory).createInstance(elements);
    }

    // Метод для создания неизменяемой оболочки
    public static <T> MyCollection<T> unmodifiableMyCollection(MyCollection<T> collection) {
        return new UnmodifiableMyCollection<>(collection);
    }
}

class UnmodifiableMyCollection<T> implements MyCollection<T> {
    private final MyCollection<T> collection; // Внутренний объект

    public UnmodifiableMyCollection(MyCollection<T> collection) {
        this.collection = collection;
    }

    @Override
    public void add(T element) {
        throw new UnsupportedOperationException("Невозможно изменить неизменяемую коллекцию");
    }

    @Override
    public int size() {
        return collection.size(); // Делегируем вызов
    }

    @Override
    public Iterator<T> iterator() {
        return collection.iterator(); // Делегируем вызов
    }
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
            resizeArray(elements.length * 2);
        }
        elements[size++] = element; // Добавляем элемент
    }

    @SuppressWarnings("unchecked")
    void resizeArray(int newCapacity) {
        T[] newElements = (T[]) new Object[newCapacity];
        System.arraycopy(elements, 0, newElements, 0, size);
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
                resizeArray(elements.length * 2);
            }
            elements[size++] = element; // Добавляем элемент
        }
    }

    @SuppressWarnings("unchecked")
    void resizeArray(int newCapacity) {
        T[] newElements = (T[]) new Object[newCapacity];
        System.arraycopy(elements, 0, newElements, 0, size);
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

public class Main {
    public static void main(String[] args) {
        // Устанавливаем фабрику для MyList
        Collections.setMyCollectionFactory(new MyListFactory<>());

        // Создаем экземпляр MyList по умолчанию
        MyCollection<String> defaultList = Collections.createInstance();
        defaultList.add("A");
        defaultList.add("B");
        System.out.println("MyList по умолчанию: " + defaultList.size());

        // Создаем экземпляр MyList с начальной емкостью
        MyCollection<String> listWithCapacity = Collections.createInstance(20);
        System.out.println("MyList с начальной емкостью: " + listWithCapacity.size());

        // Создаем экземпляр MyList с начальными элементами
        MyCollection<String> listWithElements = Collections.createInstance(new String[]{"X", "Y", "Z"});
        System.out.println("MyList с начальными элементами: " + listWithElements.size());

        // Устанавливаем фабрику для MySet
        Collections.setMyCollectionFactory(new MySetFactory<>());

        // Создаем экземпляр MySet по умолчанию
        MyCollection<String> defaultSet = Collections.createInstance();
        defaultSet.add("A");
        defaultSet.add("B");
        System.out.println("MySet по умолчанию: " + defaultSet.size());

        // Создаем экземпляр MySet с начальной емкостью
        MyCollection<String> setWithCapacity = Collections.createInstance(20);
        System.out.println("MySet с начальной емкостью: " + setWithCapacity.size());

        // Создаем экземпляр MySet с начальными элементами
        MyCollection<String> setWithElements = Collections.createInstance(new String[]{"X", "Y", "Z"});
        System.out.println("MySet с начальными элементами: " + setWithElements.size());
    }
}