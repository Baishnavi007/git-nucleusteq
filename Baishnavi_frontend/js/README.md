Student Performance Analyzer

About
This is a simple JavaScript console program where I worked with student data and tried to analyze it in different ways.
The idea was to take marks of students and calculate things like totals, averages, subject-wise performance and grades.

Everything runs in the console only.

Output Screenshots

1. Total Marks
This functions calculates the total marks for each student.I calculated it by using a for loop
![Function of total marks](Screenshots/Screenshot 2026-03-22 080946.png)
![Output of function total marks](image.png)

2. Student's Average Marks
Average is calculated using total marks divided by number of subjects.
I reused the total marks function here instead of writing logic again.
![Function of Student's Average Marks](Screenshots/image-1.png)
![Output of the function that calculated average marks of students](Screenshots/image-2.png)

3. Subject-wise Highest
This shows who scored the highest in each subject.
I compared marks across all students and updated the highest value whenever needed.
![Function of Subject-wise highest marks](Screenshots/image-3.png)
![Output of function that calculates Subject-wise highest marks](Screenshots/image-4.png)

4. Subject-wise Average
For each subject, I stored total marks and how many entries are there.
Then I calculated the average using total/count.
![Function of Subject-wise average marks](Screenshots/image-5.png)
![Output](Screenshots/image-6.png)

5. Class Topper
The student with the highest total marks is printed here.
I looped through all students and tracked the maximum.
![Function that gives class topper](Screenshots/image-7.png)
![Output](Screenshots/image-8.png)

6. Grades
Grades are assigned based on average marks.
Before that, I checked fail conditions like low marks in any subject or low attendance.
![Function to find grades](Screenshots/image-9.png)
![Output](Screenshots/image-10.png)


How to Run

• Open the file in browser console or Node

• Run the script

• Output will be visible in console/terminal