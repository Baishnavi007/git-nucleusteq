import java.util.Scanner;
public class Factorial {
    static long factorial(int num){
        if(num==0 || num==1) return 1;
        return num*factorial(num-1); // uses recursive approach to find the factorial
    }

    public static void main(String[] args){

     Scanner sc=new Scanner(System.in);
     System.out.println("Enter an integer: ");
     int number = sc.nextInt();
     long result = factorial(number);
     System.out.println("The factorial is " + result);

     sc.close(); // release the system resource used by Scanner object
    }
    
}
