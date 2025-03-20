import java.util.Arrays;
interface Readable {
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
        BookSeries series1 = new BookSeries(new int[]{250, 300, 280, 320}, "Литературная классика", 20);
        BookSeries series2 = new BookSeries(new int[]{250, 300, 280, 320}, "Литературная классика", 20);
        ArticleCollection collection = new ArticleCollection(new int[]{10, 12, 15, 20, 25}, "Современная наука", 2);

        // Пример вывода toString()
        System.out.println(series1);
        System.out.println(collection);

        // Пример сравнения объектов с помощью equals()
        System.out.println("Сравнение series1 и series2: " + series1.equals(series2));

        // Пример хэш-кодов
        System.out.println("HashCode series1: " + series1.hashCode());
        System.out.println("HashCode collection: " + collection.hashCode());
    }
}
