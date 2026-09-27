package session1.fileio;

import java.util.Scanner;

public class FileApp {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        // take file path from user
        System.out.print("Enter file path: ");
        String path = sc.nextLine();

        FileReaderUtil reader = new FileReaderUtil();
        reader.readFile(path);

        sc.close();
    }
}