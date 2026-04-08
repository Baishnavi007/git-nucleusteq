import java.util.Scanner;

public class OperatorsMenu {

    //  Arithmetic Operators
    public static void arithmetic(int a, int b) {
        System.out.println("\n--- Arithmetic Operators ---");
        System.out.println("Addition: " + (a + b));
        System.out.println("Subtraction: " + (a - b));
        System.out.println("Multiplication: " + (a * b));
        System.out.println("Division: " + (a / b));
        System.out.println("Modulus: " + (a % b));
    }

    // Relational Operators
    public static void relational(int a, int b) {
        System.out.println("\n--- Relational Operators ---");
        System.out.println("a > b: " + (a > b));
        System.out.println("a < b: " + (a < b));
        System.out.println("a == b: " + (a == b));
        System.out.println("a != b: " + (a != b));
        System.out.println("a >= b: " + (a >= b));
        System.out.println("a <= b: " + (a <= b));
    }

    // Logical Operators
    public static void logical(int a, int b) {
        System.out.println("\n--- Logical Operators ---");
        System.out.println("(a > 0 && b > 0): " + (a > 0 && b > 0));
        System.out.println("(a > 0 || b > 0): " + (a > 0 || b > 0));
        System.out.println("!(a > b): " + !(a > b));
    }

    // Menu display
    public static void showMenu() {
        System.out.println("\nChoose an option:");
        System.out.println("1. Arithmetic Operators");
        System.out.println("2. Relational Operators");
        System.out.println("3. Logical Operators");
        System.out.println("4. Exit");
    }

    //Main method
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter first number: ");
        int a = sc.nextInt();

        System.out.print("Enter second number: ");
        int b = sc.nextInt();

        int choice;

        do {
            showMenu();
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    arithmetic(a, b);
                    break;
                case 2:
                    relational(a, b);
                    break;
                case 3:
                    logical(a, b);
                    break;
                case 4:
                    System.out.println("Exiting program...");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 4);

        sc.close();
    }
}