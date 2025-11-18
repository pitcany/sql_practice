#!/usr/bin/env python3
"""
SQL Interview Prep App - GUI Version
Graphical interface for practicing SQL interview questions
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
import utils


class SQLInterviewGUI:
    """Main GUI application class"""

    def __init__(self, root):
        """Initialize the GUI application"""
        self.root = root
        self.root.title("SQL Interview Prep")
        self.root.geometry("1400x900")

        # Load environment variables
        load_dotenv()

        # Application state
        self.questions = []
        self.filtered_questions = []
        self.current_question = None
        self.stats = {
            "attempted": 0,
            "correct": 0,
            "incorrect": 0
        }

        # Color scheme
        self.colors = {
            "bg": "#f5f5f5",
            "fg": "#333333",
            "primary": "#2196F3",
            "success": "#4CAF50",
            "error": "#f44336",
            "warning": "#FF9800",
            "easy": "#4CAF50",
            "medium": "#FF9800",
            "hard": "#f44336"
        }

        # Setup UI
        self.setup_menu()
        self.setup_ui()
        self.load_questions()
        self.update_stats_display()

    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Database menu
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database", menu=db_menu)
        db_menu.add_command(label="View Schema", command=self.show_schema)
        db_menu.add_separator()
        db_menu.add_command(label="Setup Database", command=self.setup_database)
        db_menu.add_command(label="Test Connection", command=self.test_connection)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_ui(self):
        """Setup main UI components"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab 1: Questions Practice
        questions_tab = ttk.Frame(self.notebook)
        self.notebook.add(questions_tab, text="Practice Questions")
        self.setup_questions_tab(questions_tab)

        # Tab 2: SQL Sandbox
        sandbox_tab = ttk.Frame(self.notebook)
        self.notebook.add(sandbox_tab, text="SQL Sandbox")
        self.setup_sandbox_tab(sandbox_tab)

    def setup_questions_tab(self, parent):
        """Setup questions practice tab"""
        # Main container
        main_container = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel - Question browser
        left_frame = ttk.Frame(main_container, width=350)
        main_container.add(left_frame, weight=1)
        self.setup_question_browser(left_frame)

        # Right panel - Question details and query
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=3)
        self.setup_question_panel(right_frame)

    def setup_question_browser(self, parent):
        """Setup question browser panel"""
        # Title
        title_label = ttk.Label(parent, text="Questions", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Filter frame
        filter_frame = ttk.LabelFrame(parent, text="Filter by Difficulty", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        self.difficulty_var = tk.StringVar(value="all")
        difficulties = [("All", "all"), ("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]

        for text, value in difficulties:
            ttk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.difficulty_var,
                value=value,
                command=self.filter_questions
            ).pack(anchor=tk.W)

        # Stats frame
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        self.stats_labels = {}
        for key in ["attempted", "correct", "incorrect", "accuracy"]:
            label = ttk.Label(stats_frame, text=f"{key.title()}: 0")
            label.pack(anchor=tk.W)
            self.stats_labels[key] = label

        # Question list
        list_frame = ttk.LabelFrame(parent, text="Available Questions", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.question_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            selectmode=tk.SINGLE
        )
        self.question_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.question_listbox.yview)

        self.question_listbox.bind('<<ListboxSelect>>', self.on_question_select)

    def setup_question_panel(self, parent):
        """Setup question details and query panel"""
        # Question details frame
        details_frame = ttk.Frame(parent)
        details_frame.pack(fill=tk.X, padx=10, pady=5)

        self.question_title = ttk.Label(
            details_frame,
            text="Select a question to begin",
            font=("Arial", 18, "bold"),
            wraplength=900
        )
        self.question_title.pack(anchor=tk.W)

        self.question_difficulty = ttk.Label(
            details_frame,
            text="",
            font=("Arial", 11)
        )
        self.question_difficulty.pack(anchor=tk.W, pady=2)

        self.question_topics = ttk.Label(
            details_frame,
            text="",
            font=("Arial", 10, "italic")
        )
        self.question_topics.pack(anchor=tk.W, pady=2)

        separator = ttk.Separator(details_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=10)

        self.question_description = tk.Text(
            details_frame,
            height=4,
            wrap=tk.WORD,
            font=("Arial", 11),
            relief=tk.FLAT,
            bg="#f9f9f9",
            state=tk.DISABLED
        )
        self.question_description.pack(fill=tk.X, pady=5)

        # Hint button
        hint_button_frame = ttk.Frame(details_frame)
        hint_button_frame.pack(fill=tk.X, pady=5)

        self.hint_button = ttk.Button(
            hint_button_frame,
            text="Show Hint",
            command=self.show_hint
        )
        self.hint_button.pack(side=tk.LEFT)

        self.hint_label = ttk.Label(
            hint_button_frame,
            text="",
            font=("Arial", 10, "italic"),
            foreground="#666"
        )
        self.hint_label.pack(side=tk.LEFT, padx=10)

        # Query editor frame
        editor_frame = ttk.LabelFrame(parent, text="Your SQL Query", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.query_editor = scrolledtext.ScrolledText(
            editor_frame,
            height=10,
            font=("Courier New", 11),
            wrap=tk.WORD,
            undo=True
        )
        self.query_editor.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(editor_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="Run Query",
            command=self.run_query
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_query
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Show Solution",
            command=self.show_solution
        ).pack(side=tk.LEFT, padx=5)

        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Results status
        self.results_status = ttk.Label(
            results_frame,
            text="",
            font=("Arial", 12, "bold")
        )
        self.results_status.pack(anchor=tk.W, pady=5)

        # Results table with scrollbars
        table_frame = ttk.Frame(results_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview for results
        self.results_tree = ttk.Treeview(
            table_frame,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            show="tree headings"
        )
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar.config(command=self.results_tree.yview)
        h_scrollbar.config(command=self.results_tree.xview)

    def load_questions(self):
        """Load questions from JSON files"""
        try:
            self.questions = utils.load_questions("all")
            self.filter_questions()
            messagebox.showinfo("Success", f"Loaded {len(self.questions)} questions")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {str(e)}")

    def filter_questions(self):
        """Filter questions by difficulty"""
        difficulty = self.difficulty_var.get()

        if difficulty == "all":
            self.filtered_questions = self.questions
        else:
            self.filtered_questions = [
                q for q in self.questions
                if q.get("difficulty") == difficulty
            ]

        self.update_question_list()

    def update_question_list(self):
        """Update question listbox"""
        self.question_listbox.delete(0, tk.END)

        for q in self.filtered_questions:
            difficulty_emoji = {
                "easy": "🟢",
                "medium": "🟡",
                "hard": "🔴"
            }.get(q.get("difficulty", ""), "⚪")

            text = f"{difficulty_emoji} {q['id']}. {q['title']}"
            self.question_listbox.insert(tk.END, text)

    def on_question_select(self, event):
        """Handle question selection"""
        selection = self.question_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        if 0 <= idx < len(self.filtered_questions):
            self.current_question = self.filtered_questions[idx]
            self.display_question()

    def display_question(self):
        """Display selected question"""
        if not self.current_question:
            return

        q = self.current_question

        # Update title
        self.question_title.config(text=f"Question #{q['id']}: {q['title']}")

        # Update difficulty
        difficulty = q.get('difficulty', 'N/A').upper()
        difficulty_color = self.colors.get(q.get('difficulty', ''), self.colors['fg'])
        self.question_difficulty.config(
            text=f"Difficulty: {difficulty}",
            foreground=difficulty_color
        )

        # Update topics
        topics = ", ".join(q.get('topics', []))
        self.question_topics.config(text=f"Topics: {topics}" if topics else "")

        # Update description
        self.question_description.config(state=tk.NORMAL)
        self.question_description.delete(1.0, tk.END)
        self.question_description.insert(1.0, q.get('description', ''))
        self.question_description.config(state=tk.DISABLED)

        # Reset hint
        self.hint_label.config(text="")

        # Clear query editor and results
        self.clear_query()
        self.clear_results()

    def show_hint(self):
        """Show hint for current question"""
        if not self.current_question:
            return

        hint = self.current_question.get('hint', 'No hint available')
        self.hint_label.config(text=f"💡 Hint: {hint}")

    def clear_query(self):
        """Clear query editor"""
        self.query_editor.delete(1.0, tk.END)

    def clear_results(self):
        """Clear results display"""
        self.results_status.config(text="")
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_tree["columns"] = ()

    def run_query(self):
        """Execute user's query"""
        if not self.current_question:
            messagebox.showwarning("Warning", "Please select a question first")
            return

        user_query = self.query_editor.get(1.0, tk.END).strip()

        if not user_query:
            messagebox.showwarning("Warning", "Please enter a SQL query")
            return

        # Execute user's query
        self.results_status.config(text="⏳ Executing query...", foreground=self.colors['warning'])
        self.root.update()

        user_result = utils.run_user_query(user_query)

        if not user_result["success"]:
            self.results_status.config(
                text=f"❌ Query Error",
                foreground=self.colors['error']
            )
            messagebox.showerror("Query Error", user_result['error'])
            self.stats["attempted"] += 1
            self.stats["incorrect"] += 1
            self.update_stats_display()
            return

        # Display user results
        self.display_results(user_result["results"], user_result["columns"])

        # Execute expected query
        expected_result = utils.run_user_query(self.current_question["solution"])

        if not expected_result["success"]:
            self.results_status.config(
                text="⚠️ Could not validate results",
                foreground=self.colors['warning']
            )
            return

        # Compare results
        comparison = utils.compare_results(
            user_result["results"],
            expected_result["results"],
            user_result["columns"],
            expected_result["columns"]
        )

        self.stats["attempted"] += 1

        if comparison["correct"]:
            self.results_status.config(
                text="✅ CORRECT! Your query produces the expected results!",
                foreground=self.colors['success']
            )
            self.stats["correct"] += 1
            messagebox.showinfo("Success", "Correct! Well done!")
        else:
            self.results_status.config(
                text="❌ INCORRECT. Results don't match expected output.",
                foreground=self.colors['error']
            )
            self.stats["incorrect"] += 1

            error_msg = "Your results don't match the expected output.\n\n"

            if not comparison["columns_match"]:
                error_msg += f"Column mismatch:\n"
                error_msg += f"Your columns: {user_result['columns']}\n"
                error_msg += f"Expected: {expected_result['columns']}\n\n"

            if not comparison["results_match"]:
                error_msg += f"Data mismatch:\n"
                error_msg += f"Your row count: {comparison['user_row_count']}\n"
                error_msg += f"Expected row count: {comparison['expected_row_count']}\n"

            messagebox.showerror("Incorrect", error_msg)

        self.update_stats_display()

    def display_results(self, results, columns):
        """Display query results in treeview"""
        self.clear_results()

        if not results:
            self.results_status.config(
                text="No results returned",
                foreground=self.colors['fg']
            )
            return

        # Configure columns
        self.results_tree["columns"] = columns
        self.results_tree.heading("#0", text="Row")

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)

        # Add rows
        for idx, row in enumerate(results, 1):
            values = [str(val) if val is not None else "NULL" for val in row]
            self.results_tree.insert("", tk.END, text=str(idx), values=values)

    def show_solution(self):
        """Show solution for current question"""
        if not self.current_question:
            messagebox.showwarning("Warning", "Please select a question first")
            return

        solution = self.current_question.get('solution', 'No solution available')

        # Create solution window
        solution_window = tk.Toplevel(self.root)
        solution_window.title(f"Solution - Question #{self.current_question['id']}")
        solution_window.geometry("800x600")

        # Solution text
        ttk.Label(
            solution_window,
            text="Solution",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        solution_text = scrolledtext.ScrolledText(
            solution_window,
            height=10,
            font=("Courier New", 11),
            wrap=tk.WORD
        )
        solution_text.pack(fill=tk.BOTH, expand=False, padx=10, pady=5)
        solution_text.insert(1.0, solution)
        solution_text.config(state=tk.DISABLED)

        # Execute and show results
        ttk.Label(
            solution_window,
            text="Expected Results",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        result = utils.run_user_query(solution)

        if result["success"]:
            # Results table
            table_frame = ttk.Frame(solution_window)
            table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
            h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

            results_tree = ttk.Treeview(
                table_frame,
                yscrollcommand=v_scrollbar.set,
                xscrollcommand=h_scrollbar.set,
                show="tree headings"
            )
            results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            v_scrollbar.config(command=results_tree.yview)
            h_scrollbar.config(command=results_tree.xview)

            # Configure columns
            results_tree["columns"] = result["columns"]
            results_tree.heading("#0", text="Row")

            for col in result["columns"]:
                results_tree.heading(col, text=col)
                results_tree.column(col, width=150)

            # Add rows
            for idx, row in enumerate(result["results"], 1):
                values = [str(val) if val is not None else "NULL" for val in row]
                results_tree.insert("", tk.END, text=str(idx), values=values)

        # Close button
        ttk.Button(
            solution_window,
            text="Close",
            command=solution_window.destroy
        ).pack(pady=10)

    def update_stats_display(self):
        """Update statistics display"""
        self.stats_labels["attempted"].config(text=f"Attempted: {self.stats['attempted']}")
        self.stats_labels["correct"].config(text=f"Correct: {self.stats['correct']}")
        self.stats_labels["incorrect"].config(text=f"Incorrect: {self.stats['incorrect']}")

        if self.stats["attempted"] > 0:
            accuracy = (self.stats["correct"] / self.stats["attempted"]) * 100
            self.stats_labels["accuracy"].config(text=f"Accuracy: {accuracy:.1f}%")
        else:
            self.stats_labels["accuracy"].config(text="Accuracy: 0%")

    def setup_database(self):
        """Setup database with sample data"""
        response = messagebox.askyesno(
            "Setup Database",
            "⚠️ Warning: This will drop and recreate all tables!\n\nContinue?"
        )

        if not response:
            return

        try:
            success = utils.setup_database()
            if success:
                messagebox.showinfo("Success", "Database setup completed successfully!")
            else:
                messagebox.showerror("Error", "Database setup failed. Check console for details.")
        except Exception as e:
            messagebox.showerror("Error", f"Database setup failed: {str(e)}")

    def test_connection(self):
        """Test database connection"""
        try:
            success = utils.test_connection()
            if success:
                messagebox.showinfo("Success", "Database connection successful!")
            else:
                messagebox.showerror("Error", "Database connection failed. Check your configuration.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection test failed: {str(e)}")

    def setup_sandbox_tab(self, parent):
        """Setup SQL sandbox tab"""
        # Main container
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_label = ttk.Label(
            container,
            text="SQL Sandbox - Free Query Mode",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)

        instructions = ttk.Label(
            container,
            text="Execute any SQL query against the database. Explore tables, run joins, test your ideas!",
            font=("Arial", 10)
        )
        instructions.pack(pady=5)

        # Button frame for quick actions
        button_frame = ttk.Frame(container)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="View Schema",
            command=self.show_schema
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Clear Query",
            command=self.clear_sandbox_query
        ).pack(side=tk.LEFT, padx=5)

        # Sample queries dropdown
        ttk.Label(button_frame, text="Sample Queries:").pack(side=tk.LEFT, padx=(20, 5))

        self.sample_query_var = tk.StringVar()
        sample_queries = {
            "Select all employees": "SELECT * FROM employees LIMIT 10;",
            "Count by department": "SELECT d.name, COUNT(e.id) AS emp_count\nFROM departments d\nLEFT JOIN employees e ON d.id = e.department_id\nGROUP BY d.id, d.name;",
            "Top selling products": "SELECT p.name, SUM(o.quantity * p.price) AS revenue\nFROM products p\nJOIN orders o ON p.product_id = o.product_id\nGROUP BY p.product_id, p.name\nORDER BY revenue DESC\nLIMIT 5;",
            "Employee hierarchy": "SELECT e.first_name || ' ' || e.last_name AS employee,\n       m.first_name || ' ' || m.last_name AS manager\nFROM employees e\nLEFT JOIN employees m ON e.manager_id = m.id;"
        }

        sample_combo = ttk.Combobox(
            button_frame,
            textvariable=self.sample_query_var,
            values=list(sample_queries.keys()),
            state="readonly",
            width=30
        )
        sample_combo.pack(side=tk.LEFT, padx=5)

        def load_sample_query(event):
            query_name = self.sample_query_var.get()
            if query_name in sample_queries:
                self.sandbox_editor.delete(1.0, tk.END)
                self.sandbox_editor.insert(1.0, sample_queries[query_name])

        sample_combo.bind('<<ComboboxSelected>>', load_sample_query)

        # Query editor frame
        editor_frame = ttk.LabelFrame(container, text="SQL Query Editor", padding=10)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.sandbox_editor = scrolledtext.ScrolledText(
            editor_frame,
            height=15,
            font=("Courier New", 11),
            wrap=tk.WORD,
            undo=True
        )
        self.sandbox_editor.pack(fill=tk.BOTH, expand=True)

        # Execute button
        execute_frame = ttk.Frame(editor_frame)
        execute_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            execute_frame,
            text="▶ Execute Query",
            command=self.execute_sandbox_query
        ).pack(side=tk.LEFT, padx=5)

        self.sandbox_status = ttk.Label(
            execute_frame,
            text="",
            font=("Arial", 11, "bold")
        )
        self.sandbox_status.pack(side=tk.LEFT, padx=10)

        # Results frame
        results_frame = ttk.LabelFrame(container, text="Query Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Results table with scrollbars
        table_frame = ttk.Frame(results_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview for results
        self.sandbox_results_tree = ttk.Treeview(
            table_frame,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            show="tree headings"
        )
        self.sandbox_results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar.config(command=self.sandbox_results_tree.yview)
        h_scrollbar.config(command=self.sandbox_results_tree.xview)

    def clear_sandbox_query(self):
        """Clear sandbox query editor"""
        self.sandbox_editor.delete(1.0, tk.END)
        self.sandbox_status.config(text="")
        for item in self.sandbox_results_tree.get_children():
            self.sandbox_results_tree.delete(item)
        self.sandbox_results_tree["columns"] = ()

    def execute_sandbox_query(self):
        """Execute query in sandbox"""
        query = self.sandbox_editor.get(1.0, tk.END).strip()

        if not query:
            messagebox.showwarning("Warning", "Please enter a SQL query")
            return

        # Execute query
        self.sandbox_status.config(text="⏳ Executing...", foreground=self.colors['warning'])
        self.root.update()

        result = utils.run_user_query(query)

        # Clear previous results
        for item in self.sandbox_results_tree.get_children():
            self.sandbox_results_tree.delete(item)
        self.sandbox_results_tree["columns"] = ()

        if not result["success"]:
            self.sandbox_status.config(
                text=f"❌ Error",
                foreground=self.colors['error']
            )
            messagebox.showerror("Query Error", result['error'])
            return

        # Display results
        if result["results"]:
            self.sandbox_status.config(
                text=f"✅ Success - {result['row_count']} rows",
                foreground=self.colors['success']
            )

            # Configure columns
            self.sandbox_results_tree["columns"] = result["columns"]
            self.sandbox_results_tree.heading("#0", text="Row")

            for col in result["columns"]:
                self.sandbox_results_tree.heading(col, text=col)
                self.sandbox_results_tree.column(col, width=150)

            # Add rows
            for idx, row in enumerate(result["results"], 1):
                values = [str(val) if val is not None else "NULL" for val in row]
                self.sandbox_results_tree.insert("", tk.END, text=str(idx), values=values)
        else:
            self.sandbox_status.config(
                text="✅ Query executed (no results)",
                foreground=self.colors['success']
            )

    def show_schema(self):
        """Show database schema in a new window"""
        schema_window = tk.Toplevel(self.root)
        schema_window.title("Database Schema")
        schema_window.geometry("900x700")

        # Title
        ttk.Label(
            schema_window,
            text="Database Schema",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Create scrolled text for schema
        schema_text = scrolledtext.ScrolledText(
            schema_window,
            font=("Courier New", 10),
            wrap=tk.WORD
        )
        schema_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Get schema information
        schema_info = self.get_schema_info()
        schema_text.insert(1.0, schema_info)
        schema_text.config(state=tk.DISABLED)

        # Close button
        ttk.Button(
            schema_window,
            text="Close",
            command=schema_window.destroy
        ).pack(pady=10)

    def get_schema_info(self):
        """Get database schema information as formatted text"""
        output = []
        output.append("=" * 80)
        output.append("DATABASE SCHEMA")
        output.append("=" * 80)

        # Query to get all tables
        tables_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """

        result = utils.run_user_query(tables_query)

        if not result["success"]:
            return f"Error fetching schema: {result['error']}"

        tables = [row[0] for row in result["results"]]

        for table in tables:
            # Get column information for each table
            columns_query = f"""
            SELECT
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = '{table}'
            ORDER BY ordinal_position;
            """

            col_result = utils.run_user_query(columns_query)

            if col_result["success"]:
                output.append(f"\n📋 Table: {table.upper()}")
                output.append("-" * 80)

                for col in col_result["results"]:
                    col_name = col[0]
                    data_type = col[1]
                    max_length = col[2]
                    nullable = col[3]
                    default = col[4]

                    type_str = data_type
                    if max_length:
                        type_str += f"({max_length})"

                    null_str = "NULL" if nullable == "YES" else "NOT NULL"
                    default_str = f" DEFAULT {default}" if default else ""

                    output.append(f"  • {col_name:30} {type_str:20} {null_str}{default_str}")

        # Get row counts
        output.append("\n" + "=" * 80)
        output.append("TABLE ROW COUNTS")
        output.append("=" * 80)

        for table in tables:
            count_query = f"SELECT COUNT(*) FROM {table};"
            count_result = utils.run_user_query(count_query)

            if count_result["success"]:
                count = count_result["results"][0][0]
                output.append(f"  {table:35} {count:>10} rows")

        output.append("=" * 80)

        return "\n".join(output)

    def show_about(self):
        """Show about dialog"""
        about_text = """SQL Interview Prep App

A comprehensive PostgreSQL-based application for
practicing SQL interview questions.

Features:
• 30+ curated questions
• Easy, Medium, and Hard difficulty levels
• Real-time query validation
• Instant feedback
• Statistics tracking
• SQL Sandbox for free exploration

Created for SQL interview preparation.
        """
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SQLInterviewGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
