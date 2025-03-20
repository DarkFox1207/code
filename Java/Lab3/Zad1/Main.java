class BookSeries {
    private int[] pagesPerBook; // Количество страниц в каждой книге серии
    private String seriesName;  // Название серии
    private int introPages;     // Количество страниц вводной информации в каждой книге

    // Конструктор по умолчанию
    public BookSeries() {
        this.pagesPerBook = new int[]{};
        this.seriesName = "Неизвестная серия";
        this.introPages = 0;
    }

    // Конструктор с параметрами
    public BookSeries(int[] pagesPerBook, String seriesName, int introPages) {
        this.pagesPerBook = pagesPerBook.clone();
        this.seriesName = seriesName;
        this.introPages = introPages;
    }

    // Методы доступа
    public int[] getPagesPerBook() {
        return pagesPerBook.clone();
    }

    public void setPagesPerBook(int[] pagesPerBook) {
        this.pagesPerBook = pagesPerBook.clone();
    }

    public String getSeriesName() {
        return seriesName;
    }

    public void setSeriesName(String seriesName) {
        this.seriesName = seriesName;
    }

    public int getIntroPages() {
        return introPages;
    }

    public void setIntroPages(int introPages) {
        this.introPages = introPages;
    }

    // Функциональный метод: подсчет общего количества страниц без учета вводных страниц
    public int totalContentPages() {
        int totalPages = 0;
        for (int pages : pagesPerBook) {
            totalPages += (pages - introPages);
        }
        return totalPages;
    }

    // Вывод информации о серии сочинений
    public void printInfo() {
        System.out.println("Серия: " + seriesName);
        System.out.println("Общее количество страниц без вводных: " + totalContentPages());
    }
}

class ArticleCollection {
    private int[] pagesPerArticle; // Количество страниц в каждой статье
    private String collectionName; // Название сборника
    private int maxAnnotationPages; // Максимально допустимое количество страниц аннотации

    // Конструктор по умолчанию
    public ArticleCollection() {
        this.pagesPerArticle = new int[]{};
        this.collectionName = "Неизвестный сборник";
        this.maxAnnotationPages = 0;
    }

    // Конструктор с параметрами
    public ArticleCollection(int[] pagesPerArticle, String collectionName, int maxAnnotationPages) {
        this.pagesPerArticle = pagesPerArticle.clone();
        this.collectionName = collectionName;
        this.maxAnnotationPages = maxAnnotationPages;
    }

    // Методы доступа
    public int[] getPagesPerArticle() {
        return pagesPerArticle.clone();
    }

    public void setPagesPerArticle(int[] pagesPerArticle) {
        this.pagesPerArticle = pagesPerArticle.clone();
    }

    public String getCollectionName() {
        return collectionName;
    }

    public void setCollectionName(String collectionName) {
        this.collectionName = collectionName;
    }

    public int getMaxAnnotationPages() {
        return maxAnnotationPages;
    }

    public void setMaxAnnotationPages(int maxAnnotationPages) {
        this.maxAnnotationPages = maxAnnotationPages;
    }

    // Функциональный метод: подсчет общего количества страниц без учета аннотаций
    public int totalContentPages() {
        int totalPages = 0;
        for (int pages : pagesPerArticle) {
            totalPages += (pages - Math.min(pages, maxAnnotationPages)); // Если статья короче аннотации, аннотация = всей статье
        }
        return totalPages;
    }

    // Вывод информации о сборнике статей
    public void printInfo() {
        System.out.println("Сборник: " + collectionName);
        System.out.println("Общее количество страниц без аннотаций: " + totalContentPages());
    }
}

public class Main {
    public static void main(String[] args) {
        int[] bookPages = {250, 300, 280, 320}; // Количество страниц в книгах серии
        BookSeries series = new BookSeries(bookPages, "Литературная классика", 20);
        series.printInfo();

        int[] articlePages = {10, 12, 15, 20, 25}; // Количество страниц в статьях
        ArticleCollection collection = new ArticleCollection(articlePages, "Современная наука", 2);
        collection.printInfo();
    }
}
