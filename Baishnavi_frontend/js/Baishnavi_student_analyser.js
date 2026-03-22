// Student Performance Analyzer

const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 30 },
      { subject: "English", score: 82 },
      { subject: "Science", score: 74 },
      { subject: "History", score: 69 },
      { subject: "Computer", score: 88 }
    ],
    attendance: 82
  },
  {
    name: "Rahul",
    marks: [
      { subject: "Math", score: 90 },
      { subject: "English", score: 85 },
      { subject: "Science", score: 80 },
      { subject: "History", score: 35 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 91
  },
    {
    name: "Rishi",
    marks: [
      { subject: "Math", score: 42 },
      { subject: "English", score: 80 },
      { subject: "Science", score: 75 },
      { subject: "History", score: 77 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 91
  },
      {
    name: "Ravi",
    marks: [
      { subject: "Math", score: 92 },
      { subject: "English", score: 90 },
      { subject: "Science", score: 95 },
      { subject: "History", score: 97 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 77
  },
   {
    name: "Ramesh",
    marks: [
      { subject: "Math", score: 50 },
      { subject: "English", score: 50 },
      { subject: "Science", score: 55 },
      { subject: "History", score: 70 },
      { subject: "Computer", score: 50 }
    ],
    attendance: 77
  },
     {
    name: "John",
    marks: [
      { subject: "Math", score: 50 },
      { subject: "English", score: 50 },
      { subject: "Science", score: 55 },
      { subject: "History", score: 70 },
      { subject: "Computer", score: 50 }
    ],
    attendance: 74
  }
];

//Function to calculate total marks of students, it uses a simple for loop for this
function calculateTotalMarks(student) {
  let total = 0;

  for (let i = 0; i < student.marks.length; i++) {
    total += student.marks[i].score;
  }

  return total;
}

//  Prints the result of calculateTotalMarks function
students.forEach(student => {
  const total = calculateTotalMarks(student);
  

  console.log(`${student.name} Total Marks: ${total}`);
 
});

//Function to calculate the average marks of each student
function calculateAverageMarks(student) {
  const total = calculateTotalMarks(student);
  const numberOfSubjects = student.marks.length;

  return total / numberOfSubjects;
}

//Prints the result of calculateAverageMarks function
students.forEach(student => {
  const total = calculateAverageMarks(student);
  

  console.log(`${student.name} Average Marks: ${total}`);
 
});

//Functipn to get the highest marks subject-wise
function getSubjectWiseHighest(students) {
  const highestScores = {};

  for (let i = 0; i < students.length; i++) {
    const student = students[i];

    for (let j = 0; j < student.marks.length; j++) {
      const subject = student.marks[j].subject;
      const score = student.marks[j].score;

      if (!highestScores[subject] || score > highestScores[subject].score) {
        highestScores[subject] = {
          name: student.name,
          score: score
        };
      }
    }
  }

  return highestScores;
}

//Prints the output of getSubjectWiseHighest function which return the highest marks per subject
const highest = getSubjectWiseHighest(students);
for (let subject in highest) {
  console.log(
    `Highest in ${subject}: ${highest[subject].name} (${highest[subject].score})`
  );
}

//Function to calculate the average marks subject wise
function getSubjectWiseAverage(students) {
  const subjectData = {};

  for (let i = 0; i < students.length; i++) {
    const student = students[i];

    for (let j = 0; j < student.marks.length; j++) {
      const mark = student.marks[j];
      const subject = mark.subject;
      const score = mark.score;

      // if the subject is coming for the furst time
      if (!subjectData[subject]) {
        subjectData[subject] = {
          total: 0,
          count: 0
        };
      }

      subjectData[subject].total += score;
      subjectData[subject].count += 1;
    }
  }

  return subjectData;
}

//to print the output of getSubjectWiseAverage function which will print the average marks subject-wise
const subjectAvg = getSubjectWiseAverage(students);
for (let subject in subjectAvg) {
  const avg = subjectAvg[subject].total / subjectAvg[subject].count;
  console.log(`Average ${subject} Score: ${avg}`);
}

//Function to get the class topper(student with the highest marks in the class)
function getClassTopper(students) {
  let topper = null;
  let highestMarks = 0;

  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    const total = calculateTotalMarks(student);

    if (total > highestMarks) {
      highestMarks = total;
      topper = student.name;
    }
  }

  return { name: topper, marks: highestMarks };
}

//prints the output of the function getClassTopper which returns class topper's name and respective marks
const topper = getClassTopper(students);
console.log(`Class Topper: ${topper.name} with ${topper.marks} marks`);

//logic of the function to get the grades of the student and check if they are fail
function getStudentGrade(student) {
  // Check subject fail
  for (let i = 0; i < student.marks.length; i++) {
    if (student.marks[i].score <= 40) {
      return `Fail (Failed in ${student.marks[i].subject})`;
    }
  }

  // Check attendance fail
  if (student.attendance < 75) {
    return "Fail (Low Attendance)";
  }

  // If passed, calculate grade
  const average = calculateAverageMarks(student);

  if (average >= 85) return "A";
  else if (average >= 70) return "B";
  else if (average >= 50) return "C";
  else return "Fail";
}

//Prints the grade of the student which we have received from the function getStudentGrade
students.forEach(student => {
  const grade = getStudentGrade(student);
  console.log(`${student.name} Grade: ${grade}`);
});