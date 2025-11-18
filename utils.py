"""
Utility functions for SQL Interview Prep App
Handles database connections, query execution, and result comparison
"""

import os
import json
import psycopg2
from psycopg2 import sql, Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime, date
from decimal import Decimal


def load_questions(difficulty: str = "all") -> List[Dict]:
    """
    Load questions from JSON files

    Args:
        difficulty: "easy", "medium", "hard", or "all"

    Returns:
        List of question dictionaries
    """
    questions = []

    if difficulty in ["easy", "all"]:
        try:
            with open("data/easy_questions.json", "r") as f:
                questions.extend(json.load(f))
        except FileNotFoundError:
            print("Warning: easy_questions.json not found")

    if difficulty in ["medium", "all"]:
        try:
            with open("data/medium_questions.json", "r") as f:
                questions.extend(json.load(f))
        except FileNotFoundError:
            print("Warning: medium_questions.json not found")

    if difficulty in ["hard", "all"]:
        try:
            with open("data/hard_questions.json", "r") as f:
                questions.extend(json.load(f))
        except FileNotFoundError:
            print("Warning: hard_questions.json not found")

    return questions


def connect_db(autocommit: bool = False) -> psycopg2.extensions.connection:
    """
    Connect to PostgreSQL database using environment variables

    Args:
        autocommit: Set connection to autocommit mode

    Returns:
        Database connection object
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "interview_db"),
            user=os.getenv("POSTGRES_USER", "sql_interview"),
            password=os.getenv("POSTGRES_PASSWORD", "your_password")
        )

        if autocommit:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        raise


def execute_query(conn: psycopg2.extensions.connection,
                  query: str,
                  fetch: bool = True) -> Optional[Tuple[List[Tuple], List[str]]]:
    """
    Execute a SQL query and return results

    Args:
        conn: Database connection
        query: SQL query string
        fetch: Whether to fetch results (False for DDL/DML statements)

    Returns:
        Tuple of (results, column_names) if fetch=True, None otherwise
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query)

            if fetch and cur.description:
                results = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                return results, column_names

            conn.commit()
            return None

    except Error as e:
        conn.rollback()
        raise Exception(f"Query execution error: {e}")


def run_user_query(query: str) -> Dict[str, Any]:
    """
    Run user's SQL query in a safe transaction context

    Args:
        query: User's SQL query

    Returns:
        Dictionary with success status, results, column names, and error message
    """
    conn = None
    try:
        conn = connect_db()

        # Use a savepoint to safely test the query
        with conn.cursor() as cur:
            cur.execute("SAVEPOINT test_query;")

            try:
                cur.execute(query)

                if cur.description:
                    results = cur.fetchall()
                    column_names = [desc[0] for desc in cur.description]

                    # Rollback to savepoint to undo any changes
                    cur.execute("ROLLBACK TO SAVEPOINT test_query;")

                    return {
                        "success": True,
                        "results": results,
                        "columns": column_names,
                        "row_count": len(results),
                        "error": None
                    }
                else:
                    # Query doesn't return results (e.g., UPDATE, DELETE)
                    cur.execute("ROLLBACK TO SAVEPOINT test_query;")
                    return {
                        "success": True,
                        "results": [],
                        "columns": [],
                        "row_count": 0,
                        "error": None,
                        "message": "Query executed successfully (no results returned)"
                    }

            except Error as e:
                cur.execute("ROLLBACK TO SAVEPOINT test_query;")
                return {
                    "success": False,
                    "results": None,
                    "columns": None,
                    "row_count": 0,
                    "error": str(e)
                }

    except Exception as e:
        return {
            "success": False,
            "results": None,
            "columns": None,
            "row_count": 0,
            "error": str(e)
        }

    finally:
        if conn:
            conn.close()


def normalize_value(value: Any) -> Any:
    """
    Normalize a value for comparison (handle decimals, dates, etc.)

    Args:
        value: Value to normalize

    Returns:
        Normalized value
    """
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, (datetime, date)):
        return str(value)
    elif value is None:
        return None
    else:
        return value


def normalize_row(row: Tuple) -> Tuple:
    """
    Normalize a row of data for comparison

    Args:
        row: Tuple of values

    Returns:
        Normalized tuple
    """
    return tuple(normalize_value(v) for v in row)


def compare_results(user_results: List[Tuple],
                   expected_results: List[Tuple],
                   user_columns: List[str],
                   expected_columns: List[str]) -> Dict[str, Any]:
    """
    Compare user's query results with expected results

    Args:
        user_results: User's query results
        expected_results: Expected query results
        user_columns: User's column names
        expected_columns: Expected column names

    Returns:
        Dictionary with comparison results
    """
    # Normalize results
    user_normalized = [normalize_row(row) for row in user_results]
    expected_normalized = [normalize_row(row) for row in expected_results]

    # Sort both for comparison (order might differ)
    user_sorted = sorted(user_normalized)
    expected_sorted = sorted(expected_normalized)

    # Check column names (case-insensitive)
    user_cols_lower = [col.lower() for col in user_columns]
    expected_cols_lower = [col.lower() for col in expected_columns]

    columns_match = set(user_cols_lower) == set(expected_cols_lower)

    # Check if results match
    results_match = user_sorted == expected_sorted

    return {
        "columns_match": columns_match,
        "results_match": results_match,
        "correct": columns_match and results_match,
        "user_row_count": len(user_results),
        "expected_row_count": len(expected_results),
        "user_columns": user_columns,
        "expected_columns": expected_columns
    }


def format_table(results: List[Tuple], columns: List[str], max_rows: int = 20) -> str:
    """
    Format query results as a readable table

    Args:
        results: Query results
        columns: Column names
        max_rows: Maximum number of rows to display

    Returns:
        Formatted table string
    """
    if not results:
        return "No results returned"

    # Calculate column widths
    col_widths = [len(col) for col in columns]

    for row in results[:max_rows]:
        for i, val in enumerate(row):
            val_str = str(val) if val is not None else "NULL"
            col_widths[i] = max(col_widths[i], len(val_str))

    # Create separator
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

    # Format header
    header = "|" + "|".join(f" {col:{w}} " for col, w in zip(columns, col_widths)) + "|"

    # Format rows
    rows = []
    for row in results[:max_rows]:
        formatted_vals = []
        for val, w in zip(row, col_widths):
            val_str = str(val) if val is not None else "NULL"
            formatted_vals.append(f" {val_str:{w}} ")
        rows.append("|" + "|".join(formatted_vals) + "|")

    # Combine all parts
    table = [separator, header, separator] + rows + [separator]

    if len(results) > max_rows:
        table.append(f"\n... ({len(results) - max_rows} more rows)")

    return "\n".join(table)


def validate_question(question: Dict) -> bool:
    """
    Validate that a question has all required fields

    Args:
        question: Question dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["id", "title", "description", "solution", "difficulty"]

    for field in required_fields:
        if field not in question:
            print(f"Warning: Question missing required field: {field}")
            return False

    return True


def setup_database(sql_file: str = "setup_db.sql") -> bool:
    """
    Set up the database by executing the setup SQL script

    Args:
        sql_file: Path to SQL setup file

    Returns:
        True if successful, False otherwise
    """
    try:
        conn = connect_db(autocommit=True)

        with open(sql_file, 'r') as f:
            sql_script = f.read()

        with conn.cursor() as cur:
            cur.execute(sql_script)

        conn.close()
        print("Database setup completed successfully!")
        return True

    except FileNotFoundError:
        print(f"Error: SQL file '{sql_file}' not found")
        return False

    except Error as e:
        print(f"Error setting up database: {e}")
        return False


def test_connection() -> bool:
    """
    Test database connection

    Returns:
        True if connection successful, False otherwise
    """
    try:
        conn = connect_db()
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"Connected to: {version[0]}")
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
