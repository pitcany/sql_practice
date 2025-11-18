# SQL Interview Prep App

A PostgreSQL-based application for practicing SQL interview questions. Available in both **CLI** and **GUI** versions, this app provides a comprehensive environment for learning and mastering SQL queries, from basic SELECT statements to advanced window functions and recursive CTEs.

## Features

- **30+ Curated Questions**: Questions ranging from easy to hard, covering all major SQL concepts
- **Dual Interface**: Choose between CLI (command-line) or GUI (graphical) interface
- **Real-time Validation**: Instant feedback on query correctness
- **Comprehensive Database**: Realistic toy database with multiple related tables
- **Statistics Tracking**: Monitor your progress with built-in statistics
- **Topics Coverage**:
  - Basic SELECT, filtering, and sorting
  - JOINs (INNER, LEFT, self-joins)
  - Aggregations and GROUP BY
  - Subqueries and CTEs
  - Window functions
  - Recursive queries
  - Date/time operations
  - Advanced SQL patterns

## Project Structure

```
sql_interview_prep/
│
├── app.py                   # CLI application (command-line interface)
├── app_gui.py              # GUI application (graphical interface)
├── utils.py                 # Helper functions for database operations
├── requirements.txt         # Python dependencies
├── setup_db.sql            # Database schema and sample data
├── env.example             # Example environment configuration
├── data/                   # Question metadata
│   ├── easy_questions.json
│   ├── medium_questions.json
│   └── hard_questions.json
└── README.md              # This file
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 12+**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **pip**: Python package installer (usually comes with Python)

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd sql_practice
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary`: PostgreSQL database adapter
- `python-dotenv`: Environment variable management

### 3. Set Up PostgreSQL Database

#### Option A: Create Database Using psql

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# In psql prompt:
CREATE DATABASE interview_db;
CREATE USER sql_interview WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE interview_db TO sql_interview;

# Connect to the new database
\c interview_db

# Grant schema privileges (required for PostgreSQL 15+)
GRANT CREATE ON SCHEMA public TO sql_interview;
GRANT USAGE ON SCHEMA public TO sql_interview;
\q
```

**Note**: The schema privilege grants are essential for PostgreSQL 15 and later versions, which removed default CREATE privileges on the `public` schema for security reasons.

#### Option B: Using pgAdmin

1. Open pgAdmin
2. Right-click "Databases" → Create → Database
3. Name: `interview_db`
4. Create a new user: `sql_interview` with password
5. Grant all privileges on the database to this user
6. **Important for PostgreSQL 15+**: Open the Query Tool and run:
   ```sql
   GRANT CREATE ON SCHEMA public TO sql_interview;
   GRANT USAGE ON SCHEMA public TO sql_interview;
   ```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp env.example .env
```

Edit `.env` with your database credentials:

```
POSTGRES_DB=interview_db
POSTGRES_USER=sql_interview
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

**Note**: Replace `your_password` with your actual PostgreSQL password.

You can use either the **CLI** (command-line) or **GUI** (graphical) version of the application.

### Starting the Application

**GUI Version (Recommended for Beginners):**
```bash
python app_gui.py
```

**CLI Version:**
```bash
psql -U sql_interview -d interview_db -f setup_db.sql
```

This will create the following tables with sample data:
- **Departments**: 5 departments with budgets and locations
- **Employees**: 15 employees with salaries and managers
- **Projects**: 5 projects with different statuses
- **Employee_Projects**: Many-to-many relationships
- **Customers**: 10 customers from various countries
- **Products**: 15 products across multiple categories
- **Orders**: 20 orders with different statuses

**For GUI Version:**
1. Launch the app: `python app_gui.py`
2. Go to **Database → Setup Database** in the menu
3. Confirm the setup by clicking **Yes**
4. Test connection with **Database → Test Connection**

**For CLI Version:**
1. Launch the app: `python app.py`
2. Select option **5** (Setup Database)
3. Confirm the setup by typing `yes`
4. Test connection with option **6** (Test Database Connection)

### CLI Main Menu Options

```bash
python app.py
```

Or make it executable:

```bash
chmod +x app.py
./app.py
```

### CLI - Practicing Questions

### Main Menu Options

### CLI Example Session

```
============================================================
SQL INTERVIEW PREP - Main Menu
============================================================
1. Browse Questions
2. Practice by Difficulty
3. Random Question
4. View Statistics
5. Setup Database
6. Test Database Connection
7. Exit
============================================================
```

### Option 1: Browse Questions

- View all available questions with their difficulty levels
- Select any question by number to practice
- Questions show topics like "basic select", "joins", "aggregation", etc.

### Option 2: Practice by Difficulty

- Filter questions by difficulty: Easy, Medium, or Hard
- Perfect for progressive learning
- Start with Easy questions and work your way up

### Option 3: Random Question

- Get a random question from all difficulty levels
- Great for testing your overall knowledge
- Keeps practice sessions unpredictable

### Option 4: View Statistics

- See how many questions you've attempted
- Track correct vs. incorrect answers
- Monitor your accuracy percentage

### Option 5: Setup Database

- Initialize or reset the database with sample data
- **Warning**: This will drop all existing tables and recreate them
- Use this if you need a fresh start

### Option 6: Test Database Connection

- Verify your database connection is working
- Displays PostgreSQL version information
- Useful for troubleshooting connection issues

### Answering Questions

### GUI Version Features

The GUI version provides a modern, user-friendly interface with the following features:

**Main Window Components:**
- **Question Browser**: Left panel with difficulty filters and statistics
- **Question Details**: Display of question title, difficulty, topics, and description
- **Query Editor**: Multi-line SQL editor with syntax support
- **Results Display**: Table view of query results with scrolling
- **Real-time Feedback**: Instant validation with color-coded status messages

**Menu Options:**
- **Database → Setup Database**: Initialize or reset the database
- **Database → Test Connection**: Verify database connectivity
- **Help → About**: View application information

**Features:**
- Filter questions by difficulty (All, Easy, Medium, Hard)
- View statistics (attempted, correct, incorrect, accuracy)
- Show hints for each question
- Run queries with instant feedback
- View solutions in a separate window
- Color-coded difficulty indicators:
  - 🟢 Green for Easy
  - 🟡 Yellow/Orange for Medium
  - 🔴 Red for Hard
- Tabular display of query results
- Error messages with detailed feedback

**How to Use the GUI:**

1. **Launch the GUI**: Run `python app_gui.py`
2. **Setup Database** (first time): Go to Database → Setup Database
3. **Select a Question**: Click on any question from the list
4. **Read the Question**: Review the description and topics
5. **Optional Hint**: Click "Show Hint" if you need help
6. **Write Your Query**: Enter your SQL query in the editor
7. **Run Query**: Click "Run Query" button
8. **View Results**: See your results and validation status
9. **Check Solution**: If stuck, click "Show Solution"

**Keyboard Tips:**
- The query editor supports standard text editing shortcuts
- Use Ctrl+A to select all text
- Use Ctrl+Z to undo

## Database Schema

1. **Read the Question**: Carefully read the description
2. **View Hint** (Optional): Type `y` if you need a hint
3. **Write Your Query**: Enter your SQL query line by line
4. **Submit**: Type `END` on a new line when finished
5. **Get Feedback**: See your results compared to expected output

#### Special Commands While Answering

- **`END`**: Submit your query
- **`SKIP`**: Skip the current question
- **`SOLUTION`**: View the correct solution

#### Example Session

```sql
-- Question: Find employees with salary > 80000

SELECT first_name, last_name, salary
FROM employees
WHERE salary > 80000
ORDER BY salary DESC;
END
```

### Understanding Results

After submitting your query, you'll see:

1. **Your Results**: A formatted table of your query output
2. **Comparison**:
   - ✅ **CORRECT**: Your query matches expected results
   - ❌ **INCORRECT**: Differences are highlighted
3. **Details** (if incorrect):
   - Column name mismatches
   - Row count differences
   - Expected results displayed

## Project Structure

```
sql_practice/
├── app.py                      # Main application entry point
├── utils.py                    # Database utilities and query execution
├── setup_db.sql                # Database schema and sample data
├── requirements.txt            # Python dependencies
├── env.example                 # Environment variable template
├── .env                        # Your configuration (create this)
├── data/                       # Question files
│   ├── easy_questions.json     # Beginner-level questions
│   ├── medium_questions.json   # Intermediate questions
│   └── hard_questions.json     # Advanced questions
└── README.md                   # This file
```

## Adding Custom Questions

You can add your own questions to the JSON files in the `data/` directory.

### Question Format

```json
{
    "id": 100,
    "title": "Your Question Title",
    "description": "Detailed description of what the query should do.",
    "hint": "Optional hint for the user",
    "difficulty": "easy",
    "topics": ["topic1", "topic2"],
    "solution": "SELECT * FROM table_name;",
    "expected_columns": ["col1", "col2"]
}
```

### Required Fields

- **id**: Unique identifier (integer)
- **title**: Short, descriptive title
- **description**: Full question description
- **difficulty**: "easy", "medium", or "hard"
- **solution**: The correct SQL query
- **topics**: Array of topic tags (e.g., ["joins", "aggregation"])

### Optional Fields

- **hint**: Helpful hint for users
- **expected_columns**: Array of column names in the result

## Database Schema Overview

### Employees & Departments
- Practice basic queries, joins, and aggregations
- Includes hierarchical data (employee-manager relationships)
- Sample salaries and hire dates for date/numeric operations

### Projects & Employee_Projects
- Many-to-many relationship practice
- Complex joins and aggregations
- Project statuses and budget analysis

### Customers, Products & Orders
- E-commerce style data
- Practice with timestamps and date filtering
- Order status tracking and revenue calculations

## Troubleshooting

### "Connection failed" Error

**Possible causes**:
1. PostgreSQL is not running
2. Incorrect credentials in `.env`
3. Database doesn't exist
4. Firewall blocking port 5432

**Solutions**:
```bash
# Check if PostgreSQL is running (Linux/Mac)
sudo systemctl status postgresql

# Or (Mac with Homebrew)
brew services list

# Start PostgreSQL if needed
sudo systemctl start postgresql
brew services start postgresql

# Test connection manually
psql -U sql_interview -d interview_db
```

### "No questions loaded" Error

**Cause**: Missing or corrupted JSON files

**Solution**:
- Verify all three JSON files exist in the `data/` directory
- Check JSON syntax is valid
- Ensure proper permissions to read files

### "Table does not exist" Error

**Cause**: Database not initialized

**Solution**:
- Run option **5. Setup Database** from the main menu
- Or manually run: `psql -U sql_interview -d interview_db -f setup_db.sql`

### Import Errors (psycopg2, dotenv)

**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt

# If using Python 3 specifically
pip3 install -r requirements.txt
```

### Permission Denied Errors

#### "permission denied for schema public" (PostgreSQL 15+)

**Cause**: PostgreSQL 15 and later versions removed default CREATE privileges on the `public` schema as a security enhancement. This is a breaking change from earlier versions.

**Symptoms**:
- Error message: `permission denied for schema public`
- Occurs when running the database setup (option 5 in the app)
- Tables cannot be created even though the user exists

**Solution**:
```bash
# Connect to the database (without specifying a user, uses your system user)
psql -d interview_db

# Grant necessary schema privileges
GRANT CREATE ON SCHEMA public TO sql_interview;
GRANT USAGE ON SCHEMA public TO sql_interview;

# If needed, reset the user password
ALTER USER sql_interview WITH PASSWORD 'your_password';
```

**Why this happens**: Prior to PostgreSQL 15, all users had CREATE privilege on the `public` schema by default through the `PUBLIC` role. This was changed for security reasons, requiring explicit privilege grants.

#### General Permission Issues

**Cause**: Other insufficient database privileges

**Solution**:
```sql
-- Connect as superuser
psql -U postgres

-- Grant database-level privileges
GRANT ALL PRIVILEGES ON DATABASE interview_db TO sql_interview;

-- Grant privileges on existing tables and sequences (if any)
\c interview_db
GRANT ALL ON ALL TABLES IN SCHEMA public TO sql_interview;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO sql_interview;
```

## Tips for Success

1. **Start with Easy Questions**: Build confidence before tackling harder problems
2. **Read Carefully**: Pay attention to column names and sorting requirements
3. **Use Hints Wisely**: Try on your own first, then use hints if stuck
4. **Analyze Incorrect Answers**: Learn from the differences between your query and the solution
5. **Practice Regularly**: Consistency is key to mastering SQL
6. **Experiment**: The database is safe to query - your queries won't modify data
7. **Review Solutions**: Even if you get it right, check the official solution for alternative approaches

## Advanced Usage

### Running Specific Query Files

You can test queries directly in PostgreSQL:

```bash
psql -U sql_interview -d interview_db
```

### Backing Up Your Progress

Since statistics are session-based, consider keeping a practice log:

```bash
# Export your statistics to a file (manual tracking)
# Or extend the app to save stats to a file
```

### Customizing the Database

You can modify `setup_db.sql` to add your own tables and data:

1. Add your table definitions
2. Insert sample data
3. Re-run the setup: `psql -U sql_interview -d interview_db -f setup_db.sql`

## Learning Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [SQL Style Guide](https://www.sqlstyle.guide/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [SQL Joins Visualizer](https://sql-joins.leopard.in.ua/)

## Contributing

Want to add more questions? Here's how:

1. Add your question to the appropriate JSON file (`data/easy_questions.json`, etc.)
2. Follow the question format shown above
3. Test your question in the app
4. Ensure the solution produces the expected results

## License

This project is created for educational purposes. Feel free to use and modify it for learning SQL.

## Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Verify your `.env` configuration
3. Ensure PostgreSQL is running and accessible
4. Test the database connection using option 6 in the menu

---

**Happy SQL practicing! Good luck with your interviews! 🎯**
