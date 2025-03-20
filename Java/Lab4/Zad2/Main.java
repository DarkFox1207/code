import java.io.*;
import java.util.Arrays;

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

interface Readable extends Serializable {
    String getName();
    int totalContentPages();
    void printInfo();
}

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

class SerializationUtils {
    public static <T extends Serializable> void serialize(T o, OutputStream out) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(out)) {
            oos.writeObject(o);
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
        try {
            Readable bookSeries = new BookSeries(new int[]{250, 300, 280, 320}, "Литературная классика", 20);
            Readable articleCollection = new ArticleCollection(new int[]{10, 12, 15, 20, 25}, "Современная наука", 2);

            System.out.println("До сериализации:");
            bookSeries.printInfo();
            articleCollection.printInfo();

            // Сериализация
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            SerializationUtils.serialize(bookSeries, baos);
            SerializationUtils.serialize(articleCollection, baos);

            // Десериализация
            ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
            Readable deserializedBookSeries = SerializationUtils.deserialize(bais);
            Readable deserializedArticleCollection = SerializationUtils.deserialize(bais);

            System.out.println("После десериализации:");
            deserializedBookSeries.printInfo();
            deserializedArticleCollection.printInfo();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
