import java.util.Scanner;
public class EvenSumApp {

    public static void main(String[] args) {

        EvenSumCalculator calculator = new EvenSumCalculator();

        int result = calculator.calculateSum();

        System.out.println("Sum of even numbers from 1 to 10 is: " + result);
    }
}