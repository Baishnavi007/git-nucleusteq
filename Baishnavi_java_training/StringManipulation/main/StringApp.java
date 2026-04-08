package StringManipulation.main;

import StringManipulation.service.ReverseString;
import StringManipulation.service.CountVowelString;
import StringManipulation.service.AnagramString;

import java.util.Scanner;

/*
 * Main class to run string operations
 */
public class StringApp {

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {

        ReverseString reverseService = new ReverseString();
        CountVowelString vowelService = new CountVowelString();
        AnagramString anagramService = new AnagramString();

        while (true) {

            System.out.println("\n===== STRING OPERATIONS =====");
            System.out.println("1. Reverse String");
            System.out.println("2. Count Vowels");
            System.out.println("3. Check Anagram");
            System.out.println("4. Exit");

            System.out.print("Enter choice: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // fix input issue

            switch (choice) {

                case 1:
                    System.out.print("Enter string: ");
                    String input = scanner.nextLine();

                    System.out.println("Reversed: " +
                            reverseService.reverse(input));
                    break;

                case 2:
                    System.out.print("Enter string: ");
                    input = scanner.nextLine();

                    System.out.println("Vowel Count: " +
                            vowelService.countVowels(input));
                    break;

                case 3:
                    System.out.print("Enter first string: ");
                    String str1 = scanner.nextLine();

                    System.out.print("Enter second string: ");
                    String str2 = scanner.nextLine();

                    boolean result =
                            anagramService.areAnagrams(str1, str2);

                    System.out.println(result ? "Anagram" : "Not Anagram");
                    break;

                case 4:
                    System.out.println("Exiting...");
                    return;

                default:
                    System.out.println("Invalid choice!");
            }
        }
    }
}