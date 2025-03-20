import java.util.Random;

// Интерфейс SharedArray
interface SharedArray {
    void write(int value, int position);
    int read(int position);
    int getSize();
}

// Реализация SharedArray
class SharedArrayImpl implements SharedArray {
    private int[] array;
    private boolean[] written;

    public SharedArrayImpl(int size) {
        array = new int[size];
        written = new boolean[size];
    }

    @Override
    public synchronized void write(int value, int position) {
        array[position] = value;
        written[position] = true;
        notifyAll(); // Уведомляем ожидающие нити
    }

    @Override
    public synchronized int read(int position) {
        while (!written[position]) {
            try {
                wait(); // Ожидаем, пока данные не будут записаны
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        return array[position];
    }

    @Override
    public int getSize() {
        return array.length;
    }
}

// Класс Synchronizer для управления порядком операций
class Synchronizer {
    private boolean isWriteTurn = true; // Флаг для определения, чья очередь

    public synchronized void waitForWrite() throws InterruptedException {
        while (!isWriteTurn) {
            wait(); // Ожидаем, пока не наступит очередь записи
        }
    }

    public synchronized void waitForRead() throws InterruptedException {
        while (isWriteTurn) {
            wait(); // Ожидаем, пока не наступит очередь чтения
        }
    }

    public synchronized void writeDone() {
        isWriteTurn = false; // Переключаем на чтение
        notifyAll(); // Уведомляем все ожидающие нити
    }

    public synchronized void readDone() {
        isWriteTurn = true; // Переключаем на запись
        notifyAll(); // Уведомляем все ожидающие нити
    }
}

// Нить для записи данных (реализует Runnable)
class WriterRunnable implements Runnable {
    private SharedArray sharedArray;
    private Synchronizer synchronizer;

    public WriterRunnable(SharedArray sharedArray, Synchronizer synchronizer) {
        this.sharedArray = sharedArray;
        this.synchronizer = synchronizer;
    }

    @Override
    public void run() {
        Random random = new Random();
        for (int i = 0; i < sharedArray.getSize(); i++) {
            try {
                synchronizer.waitForWrite(); // Ожидаем своей очереди
                int value = random.nextInt(100) + 1; // Случайное число от 1 до 100
                sharedArray.write(value, i);
                System.out.println("Write: " + value + " to position " + i);
                synchronizer.writeDone(); // Уведомляем, что запись завершена
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}

// Нить для чтения данных (реализует Runnable)
class ReaderRunnable implements Runnable {
    private SharedArray sharedArray;
    private Synchronizer synchronizer;

    public ReaderRunnable(SharedArray sharedArray, Synchronizer synchronizer) {
        this.sharedArray = sharedArray;
        this.synchronizer = synchronizer;
    }

    @Override
    public void run() {
        for (int i = 0; i < sharedArray.getSize(); i++) {
            try {
                synchronizer.waitForRead(); // Ожидаем своей очереди
                int value = sharedArray.read(i);
                System.out.println("Read: " + value + " from position " + i);
                synchronizer.readDone(); // Уведомляем, что чтение завершено
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}

// Главный класс
public class Main {
    public static void main(String[] args) {
        // Создаем общий объект с массивом размером 10
        SharedArray sharedArray = new SharedArrayImpl(10);

        // Создаем синхронизатор
        Synchronizer synchronizer = new Synchronizer();

        // Создаем нити
        Thread writerThread = new Thread(new WriterRunnable(sharedArray, synchronizer));
        Thread readerThread = new Thread(new ReaderRunnable(sharedArray, synchronizer));

        // Запускаем нити
        writerThread.start();
        readerThread.start();

        try {
            // Ожидаем завершения нитей
            writerThread.join();
            readerThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}