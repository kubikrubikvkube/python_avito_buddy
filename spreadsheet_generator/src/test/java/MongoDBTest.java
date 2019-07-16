import org.junit.Test;

import java.util.logging.Logger;

import static org.junit.Assert.*;

public class MongoDBTest {


    @Test
    public void testMongoDBConnection() {
        MongoDB mongoDB = new MongoDB("avito");
        long count = mongoDB.getCollection("detailed").countDocuments();
        System.out.println(count);

    }
}