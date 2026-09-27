package Baishnavi_java_training.session1.Basic_java;
import java.util.Scanner;

public class Pattern {

    // Square pattern
    static void printSquare(int n) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    // Triangle pattern
    static void printTriangle(int n) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    // Rectangle pattern
    static void printRectangle(int rows, int cols) {
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= cols; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        // Menu
        System.out.println("Choose a pattern:");
        System.out.println("1. Square");
        System.out.println("2. Triangle");
        System.out.println("3. Rectangle");

        int choice = sc.nextInt();

        switch (choice) {

            case 1:
                System.out.print("Enter size: ");
                int n1 = sc.nextInt();
                printSquare(n1);
                break;

            case 2:
                System.out.print("Enter size: ");
                int n2 = sc.nextInt();
                printTriangle(n2);
                break;

            case 3:
                System.out.print("Enter rows and columns: ");
                int rows = sc.nextInt();
                int cols = sc.nextInt();
                printRectangle(rows, cols);
                break;

            default:
                System.out.println("Invalid choice");
        }

        sc.close();
    }
}