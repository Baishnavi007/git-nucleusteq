package session1.multithreading;



public class MultiThreading {

    public static void main(String[] args) {

        // Thread using Thread class
        Thread t1 = new Thread() {
            @Override
            public void run() {
                for (int i = 1; i <= 5; i++) {
                    System.out.println("Thread Class: " + i);

                    try {
                        Thread.sleep(300);
                    } catch (InterruptedException e) {
                        System.out.println("Thread interrupted");
                    }
                }
            }
        };

        // Thread using Runnable
        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                for (int i = 1; i <= 5; i++) {
                    System.out.println("Runnable: " + i);

                    try {
                        Thread.sleep(300);
                    } catch (InterruptedException e) {
                        System.out.println("Runnable interrupted");
                    }
                }
            }
        });

        // start threads
        t1.start();
        t2.start();
    }
}