import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Spliterator;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;

public class SpreadSheetGenerator {
    public static void main(String[] args) throws IOException {
        MongoDB mongoDB = new MongoDB("avito");

        MongoCollection collection = mongoDB.getCollection("detailed");
        FindIterable allDocumentsFindIterable = collection.find();
        Spliterator spliterator = allDocumentsFindIterable.limit(1000).spliterator();
        StreamSupport.stream(spliterator, true);

        try(FileWriter out = new FileWriter("book_new.csv");CSVPrinter printer = new CSVPrinter(out, CSVFormat.EXCEL)) {

            printer.printRecord("1","2");
        }
    }
}




