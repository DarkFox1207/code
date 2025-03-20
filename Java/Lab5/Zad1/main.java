// Импорт класса Random
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        // Создаем общий объект с массивом размером 10
        SharedArray sharedArray = new SharedArrayImpl(10);

        // Создаем нити
        WriterThread writerThread = new WriterThread(sharedArray);
        ReaderThread readerThread = new ReaderThread(sharedArray);

        // Устанавливаем приоритеты (опционально)
        writerThread.setPriority(Thread.MAX_PRIORITY); // Высокий приоритет для записи
        readerThread.setPriority(Thread.MIN_PRIORITY); // Низкий приоритет для чтения

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

// Нить для записи данных
class WriterThread extends Thread {
    private SharedArray sharedArray;

    public WriterThread(SharedArray sharedArray) {
        this.sharedArray = sharedArray;
    }

    @Override
    public void run() {
        Random random = new Random();
        for (int i = 0; i < sharedArray.getSize(); i++) {
            int value = random.nextInt(100) + 1; // Случайное число от 1 до 100
            sharedArray.write(value, i);
            System.out.println("Write: " + value + " to position " + i);
        }
    }
}

// Нить для чтения данных
class ReaderThread extends Thread {
    private SharedArray sharedArray;

    public ReaderThread(SharedArray sharedArray) {
        this.sharedArray = sharedArray;
    }

    @Override
    public void run() {
        for (int i = 0; i < sharedArray.getSize(); i++) {
            int value = sharedArray.read(i);
            System.out.println("Read: " + value + " from position " + i);
        }
    }
}