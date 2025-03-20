import java.util.Arrays;

// Объявляемое исключение, которое нужно будет явно обрабатывать
class InvalidPageCountException extends Exception {
    public InvalidPageCountException(String message) {
        super(message);
    }
}

// Необъявляемое исключение, которое не нужно будет явно обрабатывать
class InvalidAnnotationException extends RuntimeException {
    public InvalidAnnotationException(String message) {
        super(message);
    }
}

interface Readable {
    String getName(); // Получение названия (серии книг или сборника статей)
    int totalContentPages(); // Подсчет количества страниц без лишнего контента
    void printInfo(); // Вывод информации
}

class BookSeries implements Readable {
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

    @Override
    public String toString() {
        return "BookSeries{" +
                "seriesName='" + seriesName + '\'' +
                ", pagesPerBook=" + Arrays.toString(pagesPerBook) +
                ", introPages=" + introPages +
                '}';
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        BookSeries that = (BookSeries) obj;
        return introPages == that.introPages &&
               Arrays.equals(pagesPerBook, that.pagesPerBook) &&
               seriesName.equals(that.seriesName);
    }

    @Override
    public int hashCode() {
        int result = Arrays.hashCode(pagesPerBook);
        result = 31 * result + seriesName.hashCode();
        result = 31 * result + introPages;
        return result;
    }
}

class ArticleCollection implements Readable {
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

    @Override
    public String toString() {
        return "ArticleCollection{" +
                "collectionName='" + collectionName + '\'' +
                ", pagesPerArticle=" + Arrays.toString(pagesPerArticle) +
                ", maxAnnotationPages=" + maxAnnotationPages +
                '}';
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        ArticleCollection that = (ArticleCollection) obj;
        return maxAnnotationPages == that.maxAnnotationPages &&
               Arrays.equals(pagesPerArticle, that.pagesPerArticle) &&
               collectionName.equals(that.collectionName);
    }

    @Override
    public int hashCode() {
        int result = Arrays.hashCode(pagesPerArticle);
        result = 31 * result + collectionName.hashCode();
        result = 31 * result + maxAnnotationPages;
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        try {
            // Инициализация массива объектов типа Readable
            Readable[] items = new Readable[]{
                new BookSeries(new int[]{250, 300, 280, 320}, "Литературная классика", 20),
                new ArticleCollection(new int[]{10, 12, 15, 20, 25}, "Современная наука", 2),
                new BookSeries(new int[]{100, 150, 120}, "Классическая литература", 15),
                new ArticleCollection(new int[]{5, 7, 8, 10}, "Научные исследования", 3)
            };

            // Вывод полной информации обо всех объектах
            System.out.println("Информация о всех объектах:");
            for (Readable item : items) {
                item.printInfo();
                System.out.println();
            }

        } catch (InvalidPageCountException e) {
            System.out.println("Ошибка: " + e.getMessage());
        } catch (InvalidAnnotationException e) {
            System.out.println("Ошибка аннотации: " + e.getMessage());
        }
    }
}
