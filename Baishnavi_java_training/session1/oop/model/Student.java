package Baishnavi_java_training.session1.oop.model;

/*
 * This class represents a basic Student.
 * It demonstrates ENCAPSULATION:
 * - Data members are private
 * - Access is controlled via getters and setters
 */
public class Student {

    // Encapsulation: data is hidden using private access modifier
    private String name;
    private int rollNumber;
    private double marks;

    // Constructor to initialize student details
    public Student(String name, int rollNumber, double marks) {
        this.name = name;
        this.rollNumber = rollNumber;
        this.marks = marks;
    }

    // Getter methods → provide controlled access to private data
    public String getName() {
        return name;
    }

    public int getRollNumber() {
        return rollNumber;
    }

    public double getMarks() {
        return marks;
    }

    // Setter method → allows controlled modification (validation can be added)
    public void setMarks(double marks) {
        if (marks >= 0) {
            this.marks = marks;
        }
    }

    // Method to display student details
    public void displayInfo() {
        System.out.println("Name: " + name);
        System.out.println("Roll Number: " + rollNumber);
        System.out.println("Marks: " + marks);
    }
}