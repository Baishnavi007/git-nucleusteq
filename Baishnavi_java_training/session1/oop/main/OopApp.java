package Baishnavi_java_training.session1.oop.main;

import model.Student;
import model.GraduateStudent;

/*
 * Main class to demonstrate OOP concepts:
  - Encapsulation (in Student class)
  - Inheritance (GraduateStudent extends Student)
  - Polymorphism (method overriding + overloading)
 */
public class OOPApp {

    public static void main(String[] args) {

        // Creating object of parent class
        Student student = new Student("Baishnavi", 101, 85.5);

        System.out.println("----- Student Info -----");

        // Calling method → simple method execution
        student.displayInfo();

        // Creating object of child class
        GraduateStudent gradStudent =
                new GraduateStudent("Ananya", 102, 92.0, "Computer Science");

        System.out.println("\n----- Graduate Student Info (Override) -----");

        /*
          POLYMORPHISM (Runtime)
          Same method name displayInfo() but different behavior (child version is executed)
         */
        gradStudent.displayInfo();

        System.out.println("\n----- Graduate Student Info with Grade (Overloading) -----");

        /*
          POLYMORPHISM (Compile-time)
         Same method name but different parameters
         */
        gradStudent.displayInfo(true);
    }
}