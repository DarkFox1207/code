import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

interface Readable extends Serializable {
    String getName();
    int totalContentPages();
    void printInfo();
}

// Исключения
class InvalidPageCountException extends Exception {
    public InvalidPageCountException(String message) {
        super(message);
    }
}

class InvalidAnnotationException extends RuntimeException {
    public InvalidAnnotationException(String message) {
        super(message);
    }
}

// Класс BookSeries
class BookSeries implements Readable {
    private static final long serialVersionUID = 1L;
    
    private int[] pagesPerBook;
    private String seriesName;
    private int introPages;

    public BookSeries(int[] pagesPerBook, String seriesName, int introPages) throws InvalidPageCountException {
        if (pagesPerBook == null || pagesPerBook.length == 0) {
            throw new InvalidPageCountException("Массив страниц книги пуст или равен null.");
        }
        this.pagesPerBook = pagesPerBook.clone();
        this.seriesName = seriesName;
        this.introPages = introPages;
    }

    @Override
    public String getName() {
        return seriesName;
    }

    @Override
    public int totalContentPages() {
        int totalPages = 0;
        for (int pages : pagesPerBook) {
            if (pages <= introPages) {
                throw new InvalidAnnotationException("Количество страниц книги не может быть меньше или равно страницам введения.");
            }
            totalPages += (pages - introPages);
        }
        return totalPages;
    }

    @Override
    public void printInfo() {
        System.out.println("Серия: " + getName());
        System.out.println("Общее количество страниц без вводных: " + totalContentPages());
    }
}

// Класс ArticleCollection
class ArticleCollection implements Readable {
    private static final long serialVersionUID = 1L;
    
    private int[] pagesPerArticle;
    private String collectionName;
    private int maxAnnotationPages;

    public ArticleCollection(int[] pagesPerArticle, String collectionName, int maxAnnotationPages) throws InvalidPageCountException {
        if (pagesPerArticle == null || pagesPerArticle.length == 0) {
            throw new InvalidPageCountException("Массив страниц статьи пуст или равен null.");
        }
        this.pagesPerArticle = pagesPerArticle.clone();
        this.collectionName = collectionName;
        this.maxAnnotationPages = maxAnnotationPages;
    }

    @Override
    public String getName() {
        return collectionName;
    }

    @Override
    public int totalContentPages() {
        int totalPages = 0;
        for (int pages : pagesPerArticle) {
            if (pages <= maxAnnotationPages) {
                throw new InvalidAnnotationException("Статья не может иметь количество страниц меньше или равно максимальному количеству аннотаций.");
            }
            totalPages += (pages - Math.min(pages, maxAnnotationPages));
        }
        return totalPages;
    }

    @Override
    public void printInfo() {
        System.out.println("Сборник: " + getName());
        System.out.println("Общее количество страниц без аннотаций: " + totalContentPages());
    }
}

// Класс для сериализации
class SerializationUtils {
    public static <T extends Serializable> void serialize(T obj, OutputStream out) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(out)) {
            oos.writeObject(obj);
        }
    }

    @SuppressWarnings("unchecked")
    public static <T extends Serializable> T deserialize(InputStream in) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(in)) {
            return (T) ois.readObject();
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List<Readable> items = new ArrayList<>();

        while (true) {
            System.out.println("Выберите действие:");
            System.out.println("1. Добавить серию книг");
            System.out.println("2. Добавить сборник статей");
            System.out.println("3. Показать все элементы");
            System.out.println("4. Сохранить в файл");
            System.out.println("5. Загрузить из файла");
            System.out.println("0. Выйти");

            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    try {
                        System.out.println("Введите название серии книг:");
                        String name = scanner.nextLine();
                        System.out.println("Введите количество вводных страниц:");
                        int introPages = scanner.nextInt();
                        scanner.nextLine();
                        System.out.println("Введите количество страниц в книгах (через пробел):");
                        int[] pages = Arrays.stream(scanner.nextLine().split(" "))
                                .mapToInt(Integer::parseInt).toArray();

                        items.add(new BookSeries(pages, name, introPages));
                    } catch (InvalidPageCountException | NumberFormatException e) {
                        System.out.println("Ошибка: " + e.getMessage());
                    }
                    break;

                case 2:
                    try {
                        System.out.println("Введите название сборника статей:");
                        String name = scanner.nextLine();
                        System.out.println("Введите максимальное количество страниц аннотации:");
                        int annotationPages = scanner.nextInt();
                        scanner.nextLine();
                        System.out.println("Введите количество страниц в статьях (через пробел):");
                        int[] pages = Arrays.stream(scanner.nextLine().split(" "))
                                .mapToInt(Integer::parseInt).toArray();

                        items.add(new ArticleCollection(pages, name, annotationPages));
                    } catch (InvalidPageCountException | NumberFormatException e) {
                        System.out.println("Ошибка: " + e.getMessage());
                    }
                    break;

                case 3:
                    for (Readable item : items) {
                        item.printInfo();
                        System.out.println();
                    }
                    break;

                case 4:
                    try (FileOutputStream fos = new FileOutputStream("data.ser")) {
                        SerializationUtils.serialize((Serializable) items, fos);
                        System.out.println("Данные сохранены.");
                    } catch (IOException e) {
                        System.out.println("Ошибка при сохранении: " + e.getMessage());
                    }
                    break;

                case 5:
                    try (FileInputStream fis = new FileInputStream("data.ser")) {
                        items = new ArrayList<>((List<Readable>) SerializationUtils.deserialize(fis));
                        System.out.println("Данные загружены.");
                    } catch (IOException | ClassNotFoundException e) {
                        System.out.println("Ошибка при загрузке: " + e.getMessage());
                    }
                    break;

                case 0:
                    System.out.println("Выход.");
                    scanner.close();
                    return;

                default:
                    System.out.println("Неверный ввод.");
            }
        }
    }
}
