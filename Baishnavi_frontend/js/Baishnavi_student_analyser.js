// Student Performance Analyzer

const students = [
  {
    name: "Lalit",
    marks: [
      { subject: "Math", score: 78 },
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
      { subject: "History", score: 76 },
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
      { subject: "English", score: 80 },
      { subject: "Science", score: 75 },
      { subject: "History", score: 77 },
      { subject: "Computer", score: 92 }
    ],
    attendance: 74
  }
];

function calculateTotalMarks(student) {
  let total = 0;

  for (let i = 0; i < student.marks.length; i++) {
    total += student.marks[i].score;
  }

  return total;
}

function calculateAverageMarks(student) {
  const total = calculateTotalMarks(student);
  const numberOfSubjects = student.marks.length;

  return total / numberOfSubjects;
}

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
