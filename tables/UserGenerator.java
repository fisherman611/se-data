import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.security.SecureRandom;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.*;
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.io.File;

public class UserGenerator {
    // Constants
    private static final String SECRET_PASSWORD = "myApplicationSecret";
    private static final List<String> MALE_NAMES = Arrays.asList(
        "Alexander", "Benjamin", "Caleb", "Carter", "Daniel", "David", "Dylan", "Elias",
        "Elijah", "Enzo", "Ethan", "Ezra", "Gabriel", "Grayson", "Henry", "Hudson",
        "Isaac", "Jack", "Jacob", "James", "Jaxon", "Joseph", "Joshua", "Kai",
        "Leo", "Liam", "Logan", "Luca", "Lucas", "Mason", "Michael", "Noah",
        "Oliver", "Roman", "Rowan", "Samuel", "Sebastian", "Theo", "Theodore", "Thomas",
        "Willian", "Walker", "Wesley", "Weston"
    );
    private static final List<String> FEMALE_NAMES = Arrays.asList(
        "Abigail", "Adeline", "Alyssa", "Amelia", "Aria", "Aubrey", "Aurora", "Autumn",
        "Bella", "Brielle", "Brooklyn", "Camila", "Charlotte", "Chloe", "Clara", "Ella",
        "Emily", "Emma", "Eva", "Everly", "Grace", "Hannah", "Harper", "Hazel",
        "Isabella", "Ivy", "Lily", "Luna", "Mia", "Nora", "Olivia", "Penelope",
        "Piper", "Scarlett", "Sienna", "Sophia", "Stella", "Violet", "Willow"
    );
    private static final List<String> FAMILY_NAMES = Arrays.asList(
        "Smith", "Jones", "Williams", "Brown", "Taylor", "Davies", "Wilson", "Evans",
        "Thomas", "Johnson", "Roberts", "Walker", "Wright", "Robinson", "Thompson", "White"
    );
    private static final List<String> EMAIL_DOMAINS = Arrays.asList("example.com", "mail.com");
    private static final LocalDate DOB_START = LocalDate.of(1980, 1, 1);
    private static final LocalDate DOB_END = LocalDate.of(2004, 12, 31);
    private static final LocalDateTime CREATED_START = LocalDateTime.of(2025, 1, 1, 0, 0, 0);
    private static final LocalDateTime CREATED_END = LocalDateTime.now();
    private static final int MALE_COUNT = 15;
    private static final int FEMALE_COUNT = 25;
    private static final int OTHER_COUNT = 10;

    // User class to hold user data
    static class User {
        int uId;
        String username;
        String email;
        String password;
        String name;
        String dob;
        String gender;
        String dateCreated;

        User(int uId, String username, String email, String password, String name, 
             String dob, String gender, String dateCreated) {
            this.uId = uId;
            this.username = username;
            this.email = email;
            this.password = password;
            this.name = name;
            this.dob = dob;
            this.gender = gender;
            this.dateCreated = dateCreated;
        }
    }

    // Random utilities
    private static final SecureRandom random = new SecureRandom();

    private static String generatePlainPassword() {
        String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        StringBuilder sb = new StringBuilder(10);
        for (int i = 0; i < 10; i++) {
            sb.append(chars.charAt(random.nextInt(chars.length())));
        }
        return sb.toString();
    }

    private static LocalDate randomDate(LocalDate start, LocalDate end) {
        long days = ChronoUnit.DAYS.between(start, end);
        long randomDays = random.nextLong(days + 1);
        return start.plusDays(randomDays);
    }

    private static LocalDateTime randomDateTime(LocalDateTime start, LocalDateTime end) {
        long seconds = ChronoUnit.SECONDS.between(start, end);
        long randomSeconds = random.nextLong(seconds + 1);
        return start.plusSeconds(randomSeconds);
    }

    // Encryption methods
    private static byte[] generateSalt() {
        byte[] salt = new byte[16];
        random.nextBytes(salt);
        return salt;
    }

    private static byte[] generateIV() {
        byte[] iv = new byte[16];
        random.nextBytes(iv);
        return iv;
    }

    private static SecretKey deriveKey(String password, byte[] salt) throws Exception {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 10000, 256);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA512");
        byte[] key = skf.generateSecret(spec).getEncoded();
        return new SecretKeySpec(key, "AES");
    }

    private static String encrypt(String data, SecretKey key, byte[] iv) throws Exception {
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
        byte[] encrypted = cipher.doFinal(data.getBytes());
        return Base64.getEncoder().encodeToString(encrypted);
    }

    private static String encryptPassword(String plainPassword) throws Exception {
        byte[] salt = generateSalt();
        byte[] iv = generateIV();
        SecretKey key = deriveKey(SECRET_PASSWORD, salt);
        String encrypted = encrypt(plainPassword, key, iv);
        return Base64.getEncoder().encodeToString(salt) + ":" +
               Base64.getEncoder().encodeToString(iv) + ":" +
               encrypted;
    }

    // Generate a single user
    private static User generateUser(int uId, String gender, List<String> firstNames,
                                     List<String> familyNames, List<String> emailDomains,
                                     Set<String> usedUsernames) throws Exception {
        String first = firstNames.get(random.nextInt(firstNames.size()));
        String last = familyNames.get(random.nextInt(familyNames.size()));
        String name = first + " " + last;

        String username;
        do {
            int num = 100 + random.nextInt(900);
            username = first.toLowerCase() + num;
        } while (usedUsernames.contains(username));
        usedUsernames.add(username);

        String email = last.toLowerCase() + username + "@" + 
                       emailDomains.get(random.nextInt(emailDomains.size()));
        String plainPassword = generatePlainPassword();
        String encryptedPassword = encryptPassword(plainPassword);

        DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String dob = randomDate(DOB_START, DOB_END).format(dateFormatter);
        String dateCreated = randomDateTime(CREATED_START, CREATED_END).format(dateTimeFormatter);

        return new User(uId, username, email, encryptedPassword, name, dob, gender, dateCreated);
    }

    public static void main(String[] args) {
        try {
            Set<String> usedUsernames = new HashSet<>();
            List<User> users = new ArrayList<>();
            int currentId = 1;

            // Generate male users
            for (int i = 0; i < MALE_COUNT; i++) {
                users.add(generateUser(currentId++, "Male", MALE_NAMES, FAMILY_NAMES, 
                                       EMAIL_DOMAINS, usedUsernames));
            }

            // Generate female users
            for (int i = 0; i < FEMALE_COUNT; i++) {
                users.add(generateUser(currentId++, "Female", FEMALE_NAMES, FAMILY_NAMES, 
                                       EMAIL_DOMAINS, usedUsernames));
            }

            // Generate other users
            List<String> combinedNames = new ArrayList<>(MALE_NAMES);
            combinedNames.addAll(FEMALE_NAMES);
            for (int i = 0; i < OTHER_COUNT; i++) {
                users.add(generateUser(currentId++, "Other", combinedNames, FAMILY_NAMES, 
                                       EMAIL_DOMAINS, usedUsernames));
            }

            // Shuffle users
            Collections.shuffle(users);

            // Reset u_id
            for (int i = 0; i < users.size(); i++) {
                users.get(i).uId = i + 1;
            }

            // Ensure the "../data" directory exists
            File dataDir = new File("../data");
            if (!dataDir.exists()) {
                if (!dataDir.mkdir()) {
                    throw new IOException("Failed to create '../data' directory");
                }
            }

            // Write to CSV
            try (BufferedWriter writer = new BufferedWriter(new FileWriter("../data/users.csv"))) {
                writer.write("u_id,username,email,password,name,dob,gender,date_created\n");
                for (User user : users) {
                    writer.write(String.format("%d,%s,%s,%s,%s,%s,%s,%s\n",
                        user.uId, user.username, user.email, user.password, user.name,
                        user.dob, user.gender, user.dateCreated));
                }
                System.out.println("Successfully generated " + users.size() + 
                                   " users and stored them in '../data/users.csv'.");
            } catch (IOException e) {
                System.err.println("Error writing CSV: " + e.getMessage());
            }
        } catch (Exception e) {
            System.err.println("Error generating users: " + e.getMessage());
        }
    }
}