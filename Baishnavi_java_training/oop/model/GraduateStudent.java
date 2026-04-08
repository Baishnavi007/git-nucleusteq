package model;

/*
 * This class extends Student → demonstrates INHERITANCE
 * It also demonstrates POLYMORPHISM:
 * - Method Overriding (runtime polymorphism)
 * - Method Overloading (compile-time polymorphism)
 */
public class GraduateStudent extends Student {

    // Additional property specific to graduate students
    private String specialization;

    // Constructor → calling parent constructor using super()
    public GraduateStudent(String name, int rollNumber, double marks, String specialization) {
        super(name, rollNumber, marks);
        this.specialization = specialization;
    }

    /*
     * METHOD OVERRIDING (Runtime Polymorphism)
     * Same method name as parent class
     * but different implementation
     */
    @Override
    public void displayInfo() {
        super.displayInfo(); // calling parent method
        System.out.println("Specialization: " + specialization);
    }

    /*
     * METHOD OVERLOADING (Compile-time Polymorphism)
     * Same method name, different parameters
     */
    public void displayInfo(boolean showGrade) {
        super.displayInfo();

        if (showGrade) {
            // Adding extra behavior
            if (getMarks() >= 90) {
                System.out.println("Grade: A");
            } else if (getMarks() >= 75) {
                System.out.println("Grade: B");
            } else {
                System.out.println("Grade: C");
            }
        }
    }
}