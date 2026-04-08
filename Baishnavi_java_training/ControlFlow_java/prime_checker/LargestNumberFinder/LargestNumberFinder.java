//package Baishnavi_java_training.ControlFlow_java.prime_checker.LargestNumberFinder;

public class LargestNumberFinder {

    public int findLargest(int first, int second, int third) {

        if (first >= second && first >= third) {
            return first;
        } else if (second >= first && second >= third) {
            return second;
        } else {
            return third;
        }
    }
}
