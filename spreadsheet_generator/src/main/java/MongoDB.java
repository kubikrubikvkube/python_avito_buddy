import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class MongoDB {
    private final MongoClient client;
    private final MongoDatabase database;

    public MongoDB(String databaseName) {
        var client = MongoClients.create();
        var database = client.getDatabase(databaseName);
        this.client = client;
        this.database = database;

    }

    public MongoCollection getCollection(String collectionName) {
        return this.database.getCollection(collectionName);
    }
}
