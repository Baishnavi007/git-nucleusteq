package session1.fileio;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

// handles reading from file
public class FileReaderUtil {

    public void readFile(String path) {

        try (BufferedReader br = new BufferedReader(new FileReader(path))) {

            String line;

            // read each line
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }

        } catch (IOException e) {
            // if file not found or error occurs
            System.out.println("Error: " + e.getMessage());
        }
    }
}