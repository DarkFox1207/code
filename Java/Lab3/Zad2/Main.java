public interface Readable {
    String getName(); // Получение названия (серии книг или сборника статей)
    int totalContentPages(); // Подсчет количества страниц без лишнего контента
    void printInfo(); // Вывод информации
}

class BookSeries implements Readable {
    private int[] pagesPerBook;
    private String seriesName;
    private int introPages;

    public BookSeries(int[] pagesPerBook, String seriesName, int introPages) {
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

class ArticleCollection implements Readable {
    private int[] pagesPerArticle;
    private String collectionName;
    private int maxAnnotationPages;

    public ArticleCollection(int[] pagesPerArticle, String collectionName, int maxAnnotationPages) {
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

public class Main {
    public static void main(String[] args) {
        Readable[] items = {
            new BookSeries(new int[]{250, 300, 280, 320}, "Литературная классика", 20),
            new ArticleCollection(new int[]{10, 12, 15, 20, 25}, "Современная наука", 2)
        };

        for (Readable item : items) {
            item.printInfo();
            System.out.println();
        }
    }
}
