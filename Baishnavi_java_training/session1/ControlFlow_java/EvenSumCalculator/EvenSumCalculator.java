

public class EvenSumCalculator {

    public int calculateSum() {

        int sum = 0;
        int number = 1;

        while (number <= 10) {

            if (number % 2 == 0) {
                sum += number;
            }

            number++;
        }

        return sum;
    }
}
