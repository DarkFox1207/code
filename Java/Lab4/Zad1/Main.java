import java.io.*;
import java.util.Arrays;

interface Readable {
    String getName();
    int totalContentPages();
    void printInfo();
    void output(OutputStream out) throws IOException;
    void write(Writer out) throws IOException;
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
        return Arrays.stream(pagesPerBook).map(p -> p - introPages).sum();
    }

    @Override
    public void printInfo() {
        System.out.println(getName());
        System.out.println(totalContentPages());
    }

    @Override
    public void output(OutputStream out) throws IOException {
        DataOutputStream dos = new DataOutputStream(out);
        dos.writeUTF(seriesName);
        dos.writeInt(introPages);
        dos.writeInt(pagesPerBook.length);
        for (int pages : pagesPerBook) {
            dos.writeInt(pages);
        }
    }

    @Override
    public void write(Writer out) throws IOException {
        out.write(seriesName + " " + introPages + " " + pagesPerBook.length + " " +
                Arrays.toString(pagesPerBook).replaceAll("[\\[\\],]", "") + "\n");
    }
}

class ReadableUtils {
    public static void output(Readable o, OutputStream out) throws IOException {
        o.output(out);
    }

    public static Readable input(InputStream in) throws IOException {
        DataInputStream dis = new DataInputStream(in);
        String name = dis.readUTF();
        int extraPages = dis.readInt();
        int length = dis.readInt();
        int[] pages = new int[length];
        for (int i = 0; i < length; i++) {
            pages[i] = dis.readInt();
        }
        return new BookSeries(pages, name, extraPages);
    }

    public static void write(Readable o, Writer out) throws IOException {
        o.write(out);
    }

    public static Readable read(Reader in) throws IOException {
        BufferedReader br = new BufferedReader(in);
        String[] data = br.readLine().split(" ");
        String name = data[0];
        int extraPages = Integer.parseInt(data[1]);
        int length = Integer.parseInt(data[2]);
        int[] pages = new int[length];
        for (int i = 0; i < length; i++) {
            pages[i] = Integer.parseInt(data[i + 3]);
        }
        return new BookSeries(pages, name, extraPages);
    }
}

public class Main {
    public static void main(String[] args) {
        try {
            BookSeries book = new BookSeries(new int[]{100, 200, 150}, "Фэнтези", 10);
            System.out.println("Исходный объект:");
            book.printInfo();
            
            // Тест записи в байтовый поток
            ByteArrayOutputStream byteOut = new ByteArrayOutputStream();
            ReadableUtils.output(book, byteOut);
            ByteArrayInputStream byteIn = new ByteArrayInputStream(byteOut.toByteArray());
            Readable restoredBook = ReadableUtils.input(byteIn);
            
            System.out.println("Объект после чтения из байтового потока:");
            restoredBook.printInfo();
            
            // Тест записи в символьный поток
            StringWriter stringOut = new StringWriter();
            ReadableUtils.write(book, stringOut);
            StringReader stringIn = new StringReader(stringOut.toString());
            Readable restoredBookFromString = ReadableUtils.read(stringIn);
            
            System.out.println("Объект после чтения из символьного потока:");
            restoredBookFromString.printInfo();
            
        } catch (IOException e) {
            System.err.println("Ошибка при обработке потоков: " + e.getMessage());
        }
    }
}
