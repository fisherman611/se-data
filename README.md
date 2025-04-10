# Software Engineering Data

## Database Diagram Overview
This data is made for our SE project here: [Vietnamese Learning Website](https://github.com/Pearlcentt/Vietnamese_Learning_Web)
![Diagram](image.png)

### Tables
This database is designed to manage users, lessons, topics, and related linguistic data for a language-learning application. Here's a brief description of each table and how they connect:
1. **User**
    - Store user account information (username, email, password, etc.)
    - Each user has a unique `u_id`.
2. **Topic**
    - Contains language-learning topics.
    - Each topic has a `topic_id` and a descriptive name.
3. **Sentence**
    - Holds example sentences in both English (`eng`) and Vietnamese (`viet`).
    - The `topic_name` column associates each sentence with a topic for organization.
4. **Word**
    - Breaks each sentence into words.
    - Uses `s_id` to link back to the sentence.
    - `w_id` uniquely identifies each word, and `similar_words` stores alternative words or closely related terms.
5. **Lesson** 
    - Represents individual lessons and ties them to a `topic_id`.
    - References a specific sentence (`s_id`) for content and has a `lesson_type` (e.g. Vocab, Fill-in-the-blank, Re-order-words, etc.)
6. **Progress**
    - Tracks a user's progress on a specific lesson.
    - Stores the user's score, current status (not started, in progress, or completed), and a `last_updated` timestamp.

### Relationships
- **User ↔ Progress** : A user can have multiple records in the `Progress` table, one for each lesson, storing their scores and statuses.
- **Topic ↔ Lesson**: Each lesson belongs to one topic, helping organize lessons by thematic category.
- **Lesson ↔ Sentence**: A lesson often focuses on a particular sentence. The `s_id` column indicates which sentence is central to that lesson’s content.
- **Sentence ↔ Word**: Each sentence can be split into multiple words, with the `Word` table capturing each token’s position (`idx`), similar words, and reference back to the sentence ID.
## Usage
1. Clone the repository:
    ```sh
    git clone https://github.com/fisherman611/se-data.git
    ```
2. Navigate to the project directory:
    ```sh
    cd se-data
    ```
## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes or improvements.
