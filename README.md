# SQL Interview Prep App

A PostgreSQL-based application for practicing SQL interview questions. Available in both **CLI** and **GUI** versions, this app provides a comprehensive environment for learning and mastering SQL queries, from basic SELECT statements to advanced window functions and recursive CTEs.

## Features

- **30+ Curated Questions**: Questions ranging from easy to hard, covering all major SQL concepts
- **Dual Interface**: Choose between CLI (command-line) or GUI (graphical) interface
- **SQL Sandbox**: Free query mode to explore and experiment with the database
- **Schema Viewer**: View complete database structure with table definitions and row counts
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

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

### 1. Install PostgreSQL

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### macOS (using Homebrew)
```bash
brew install postgresql
brew services start postgresql
```

#### Windows
Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

### 2. Create Database and User

Connect to PostgreSQL as superuser:
```bash
sudo -u postgres psql
```

Run the following commands:
```sql
CREATE USER sql_interview WITH PASSWORD 'your_password';
CREATE DATABASE interview_db OWNER sql_interview;
GRANT ALL PRIVILEGES ON DATABASE interview_db TO sql_interview;
\q
```

### 3. Clone and Setup

```bash
cd sql_interview_prep

# Install Python dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp env.example .env
# Edit .env with your database credentials
```

### 4. Configure Environment

Edit the `.env` file with your database credentials:
```
POSTGRES_DB=interview_db
POSTGRES_USER=sql_interview
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Usage

You can use either the **CLI** (command-line) or **GUI** (graphical) version of the application.

### Starting the Application

**GUI Version (Recommended for Beginners):**
```bash
python app_gui.py
```

**CLI Version:**
```bash
python app.py
```

### First-Time Setup

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

1. **Browse Questions**: View and select from all available questions
2. **Practice by Difficulty**: Filter questions by Easy, Medium, or Hard
3. **Random Question**: Get a random question to practice
4. **View Statistics**: See your practice stats (attempted, correct, accuracy)
5. **SQL Sandbox**: Free query mode - run any SQL query against the database
6. **View Database Schema**: Display all table structures, columns, and row counts
7. **Setup Database**: Initialize or reset the database
8. **Test Database Connection**: Verify your database connection
9. **Exit**: Exit the application

### CLI - Practicing Questions

1. Select a question from the menu
2. Read the description and optional hint
3. Type your SQL query (multi-line supported)
4. Type `END` on a new line when finished
5. Get instant feedback on correctness
6. View expected results if incorrect
7. See the solution if needed

### CLI Example Session

```
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

Enter your choice (1-7): 2

Select difficulty:
1. Easy
2. Medium
3. Hard

Enter choice (1-3): 1

[List of easy questions displayed]

Enter question number to practice: 1

============================================================
🟢 Question #1: Select All Employees
============================================================

Difficulty: EASY
Topics: basic select

Write a query to select all columns from the employees table.

Show hint? (y/n): n

------------------------------------------------------------
Enter your SQL query (type 'END' on a new line when done):
SELECT * FROM employees;
END

⏳ Executing your query...
✓ Query executed successfully!

📊 Your Results:
[Table with results displayed]

============================================================
RESULTS
============================================================
✅ CORRECT! Your query produces the expected results!
============================================================
```

### GUI Version Features

The GUI version provides a modern, user-friendly interface with the following features:

**Main Window Components:**
- **Tabbed Interface**: Switch between "Practice Questions" and "SQL Sandbox" tabs
- **Question Browser**: Left panel with difficulty filters and statistics (Practice tab)
- **Question Details**: Display of question title, difficulty, topics, and description (Practice tab)
- **SQL Sandbox**: Free query mode with sample queries and schema viewer (Sandbox tab)
- **Query Editor**: Multi-line SQL editor with syntax support
- **Results Display**: Table view of query results with scrolling
- **Real-time Feedback**: Instant validation with color-coded status messages

**Menu Options:**
- **Database → View Schema**: Display complete database schema in a popup window
- **Database → Setup Database**: Initialize or reset the database
- **Database → Test Connection**: Verify database connectivity
- **Help → About**: View application information

**Features:**
- Filter questions by difficulty (All, Easy, Medium, Hard)
- View statistics (attempted, correct, incorrect, accuracy)
- Show hints for each question
- Run queries with instant feedback
- View solutions in a separate window
- **SQL Sandbox** with sample queries dropdown
- **Schema Viewer** showing all tables, columns, and types
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

### SQL Sandbox Mode

Both CLI and GUI versions include a **SQL Sandbox** for free-form query exploration.

**CLI Sandbox:**
- Select option **5** from the main menu
- Type any SQL query (multi-line supported)
- Type `END` when finished to execute
- Type `SCHEMA` to view database schema
- Type `BACK` to return to main menu
- Type `CLEAR` to clear the screen

**GUI Sandbox:**
- Click on the **"SQL Sandbox"** tab
- Use the query editor to write any SQL
- Click **"View Schema"** button to see table structures
- Select from **Sample Queries** dropdown for quick examples
- Click **"Execute Query"** to run
- Results display in a scrollable table below

**Sample Queries to Try:**
```sql
-- Explore employees and their departments
SELECT e.first_name, e.last_name, d.name AS department, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
ORDER BY e.salary DESC;

-- Find top customers by spending
SELECT c.name, SUM(o.quantity * p.price) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- Employee hierarchy (manager relationships)
SELECT
    e.first_name || ' ' || e.last_name AS employee,
    m.first_name || ' ' || m.last_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Window function example - ranking
SELECT
    first_name,
    last_name,
    department_id,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```

## Database Schema

The application includes comprehensive sample data across multiple tables:

### Tables

- **departments**: Company departments with budgets and locations
- **employees**: Employee information with salaries, hire dates, and manager relationships
- **projects**: Company projects with dates, budgets, and status
- **employee_projects**: Many-to-many relationship between employees and projects
- **customers**: Customer information
- **products**: Product catalog with prices and categories
- **orders**: Customer orders

### Sample Queries

```sql
-- Get average salary by department
SELECT d.name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.id, d.name;

-- Find customers who never ordered
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Rank employees by salary within department (Window Function)
SELECT
    first_name || ' ' || last_name AS employee_name,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank
FROM employees;
```

## Question Difficulty Levels

### Easy (10 Questions)
- Basic SELECT statements
- Filtering with WHERE
- Sorting with ORDER BY
- Simple aggregations (COUNT, AVG, SUM)
- DISTINCT and LIMIT

### Medium (10 Questions)
- INNER and LEFT JOINs
- GROUP BY with multiple columns
- Subqueries
- Self-joins
- Date functions
- Complex filtering

### Hard (10 Questions)
- Window functions (RANK, ROW_NUMBER, LAG, LEAD)
- Recursive CTEs
- Advanced aggregations
- Pivot tables
- Complex multi-table joins
- Performance optimization

## Tips for Success

1. **Read Carefully**: Understand what the question is asking before writing your query
2. **Use Hints Wisely**: Try to solve without hints first, then use them if stuck
3. **Test Incrementally**: Build your query step by step
4. **Learn from Solutions**: Study the provided solutions to learn best practices
5. **Practice Regularly**: Consistent practice improves retention
6. **Experiment**: Try different approaches to solve the same problem

## Troubleshooting

### Connection Issues

If you get connection errors:

1. Verify PostgreSQL is running:
   ```bash
   sudo systemctl status postgresql  # Linux
   brew services list                 # macOS
   ```

2. Check your `.env` file has correct credentials

3. Test connection manually:
   ```bash
   psql -U sql_interview -d interview_db -h localhost
   ```

### Permission Errors

If you get permission errors when setting up the database:

```sql
-- As PostgreSQL superuser:
GRANT ALL PRIVILEGES ON DATABASE interview_db TO sql_interview;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sql_interview;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sql_interview;
```

### Module Not Found

If you get module import errors:

```bash
pip install -r requirements.txt --upgrade
```

## Advanced Features

### Adding Custom Questions

Create your own questions by adding them to the JSON files in the `data/` directory:

```json
{
    "id": 31,
    "title": "Your Question Title",
    "description": "Question description",
    "hint": "Optional hint",
    "difficulty": "medium",
    "topics": ["joins", "aggregation"],
    "solution": "SELECT ...",
    "expected_columns": ["col1", "col2"]
}
```

### Extending the Database

You can add more tables or data to `setup_db.sql` to create additional practice scenarios.

## Contributing

Feel free to contribute by:
- Adding new questions
- Improving existing questions
- Enhancing the CLI interface
- Adding new features
- Fixing bugs

## License

This project is open source and available for educational purposes.

## Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQL Tutorial - W3Schools](https://www.w3schools.com/sql/)
- [PostgreSQL Exercises](https://pgexercises.com/)
- [LeetCode Database Problems](https://leetcode.com/problemset/database/)

## Acknowledgments

Designed for SQL interview preparation with a focus on practical, real-world scenarios commonly encountered in technical interviews.

---

**Happy Learning! Good luck with your SQL interviews!**
