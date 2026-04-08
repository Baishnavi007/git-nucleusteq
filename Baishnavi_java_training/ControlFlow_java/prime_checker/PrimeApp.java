
//MAIN CLASS
import java.util.Scanner;

public class PrimeApp {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        PrimeChecker checker = new PrimeChecker();

        System.out.print("Enter a number: ");
        int number = scanner.nextInt();

        if (checker.isPrime(number)) {
            System.out.println("The number is PRIME");
        } else {
            System.out.println("The number is NOT PRIME");
        }

        scanner.close();
    }
}