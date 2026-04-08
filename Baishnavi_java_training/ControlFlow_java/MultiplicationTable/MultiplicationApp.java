import java.util.Scanner;

public class MultiplicationApp {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        MultiplicationTable table = new MultiplicationTable();

        System.out.print("Enter a number: ");
        int number = scanner.nextInt();
        System.out.print("Enter maximum multiplier: ");
        int maxMultiplier = scanner.nextInt();
     if (number <= 0 || maxMultiplier<=0) {
            System.out.println("Please enter a positive number.");
        } else {
            table.printTable(number,maxMultiplier);
        }

        scanner.close();
    }
}