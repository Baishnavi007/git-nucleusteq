import java.util.Scanner;

public class TemperatureConverter {

    // Celsius to Fahrenheit
    public static double celsiusToFahrenheit(double c) {
        return (c * 9 / 5) + 32;
    }

    // Fahrenheit to Celsius
    public static double fahrenheitToCelsius(double f) {
        return (f - 32) * 5 / 9;
    }

    // Menu
    public static void showMenu() {
        System.out.println("\nTemperature Converter:");
        System.out.println("1. Celsius to Fahrenheit");
        System.out.println("2. Fahrenheit to Celsius");
        System.out.println("3. Exit");
    }

    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int choice;

        do {
            showMenu();
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter temperature in Celsius: ");
                    double c = sc.nextDouble();
                    double f = celsiusToFahrenheit(c);
                    System.out.println("Fahrenheit: " + f);
                    break;

                case 2:
                    System.out.print("Enter temperature in Fahrenheit: ");
                    double fInput = sc.nextDouble();
                    double cResult = fahrenheitToCelsius(fInput);
                    System.out.println("Celsius: " + cResult);
                    break;

                case 3:
                    System.out.println("Exiting...");
                    break;

                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 3);

        sc.close();
    }
}