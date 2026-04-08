package Baishnavi_java_training.session1.Basic_java;
import java.util.Scanner;

public class AreaCalculator {

    public static double calculateCircleArea(double radius) {
        return Math.PI * radius * radius;
    }

    public static double calculateRectangleArea(double length, double width) {
        return length * width;
    }

    public static double calculateTriangleArea(double base, double height) {
        return 0.5 * base * height;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("1. Circle\n2. Rectangle\n3. Triangle");
        int choice = sc.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter radius: ");
                double r = sc.nextDouble();
                System.out.println("Area: " + calculateCircleArea(r));
                break;

            case 2:
                System.out.print("Enter length and width: ");
                double l = sc.nextDouble();
                double w = sc.nextDouble();
                System.out.println("Area: " + calculateRectangleArea(l, w));
                break;

            case 3:
                System.out.print("Enter base and height: ");
                double b = sc.nextDouble();
                double h = sc.nextDouble();
                System.out.println("Area: " + calculateTriangleArea(b, h));
                break;

            default:
                System.out.println("Invalid choice");
        }

        sc.close();
    }
}