package session3.userqueryengine.src.main.java.com.baishnavi.userqueryengine.model;

public class User {

   //Simple POJO class used to store user data
        private int id;
        private String name;
        private int age;
        private String role;

        // Constructor to initialize user data
        public User(int id, String name, int age, String role) {
            this.id = id;
            this.name = name;
            this.age = age;
            this.role = role;
        }

        // Getter methods
        public int getId() {
            return id;
        }


        public String getName() {
            return name;
        }

        public int getAge() {
            return age;
        }

        public String getRole() {
            return role;
        }
    }

