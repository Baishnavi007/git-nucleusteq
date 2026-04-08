public class MultiplicationTable {

    public void printTable(int number, int maxMultiplier) {
     
        for (int i = 1; i <= maxMultiplier; i++) {
            System.out.println(number + " x " + i + " = " + (number * i));
        }
    }
}