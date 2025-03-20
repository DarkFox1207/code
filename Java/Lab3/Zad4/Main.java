import java.util.Arrays;
import java.util.ArrayList;

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

        // Поиск объектов с одинаковым результатом totalContentPages()
        System.out.println("Объекты с одинаковым количеством страниц без лишнего контента:");
        ArrayList<Readable> samePagesItems = new ArrayList<>();
        for (int i = 0; i < items.length; i++) {
            for (int j = i + 1; j < items.length; j++) {
                if (items[i].totalContentPages() == items[j].totalContentPages()) {
                    samePagesItems.add(items[i]);
                    samePagesItems.add(items[j]);
                }
            }
        }

        for (Readable item : samePagesItems) {
            item.printInfo();
            System.out.println();
        }

        // Разбиение массива на два массива: один для BookSeries, второй для ArticleCollection
        ArrayList<Readable> bookSeriesList = new ArrayList<>();
        ArrayList<Readable> articleCollectionList = new ArrayList<>();

        for (Readable item : items) {
            if (item instanceof BookSeries) {
                bookSeriesList.add(item);
            } else if (item instanceof ArticleCollection) {
                articleCollectionList.add(item);
            }
        }

        // Вывод результатов после разбиения
        System.out.println("Массив объектов типа BookSeries:");
        for (Readable item : bookSeriesList) {
            item.printInfo();
            System.out.println();
        }

        System.out.println("Массив объектов типа ArticleCollection:");
        for (Readable item : articleCollectionList) {
            item.printInfo();
            System.out.println();
        }
    }
}
