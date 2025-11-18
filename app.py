#!/usr/bin/env python3
"""
SQL Interview Prep App - Main Application
Interactive CLI for practicing SQL interview questions
"""

import os
import sys
from dotenv import load_dotenv
from typing import Optional, List, Dict
import utils


class SQLInterviewApp:
    """Main application class for SQL interview preparation"""

    def __init__(self):
        """Initialize the application"""
        load_dotenv()
        self.questions = []
        self.current_question = None
        self.stats = {
            "attempted": 0,
            "correct": 0,
            "incorrect": 0
        }

    def load_questions(self, difficulty: str = "all") -> None:
        """Load questions from JSON files"""
        self.questions = utils.load_questions(difficulty)
        print(f"\n✓ Loaded {len(self.questions)} questions")

    def display_menu(self) -> None:
        """Display main menu"""
        print("\n" + "=" * 60)
        print("SQL INTERVIEW PREP - Main Menu")
        print("=" * 60)
        print("1. Browse Questions")
        print("2. Practice by Difficulty")
        print("3. Random Question")
        print("4. View Statistics")
        print("5. Setup Database")
        print("6. Test Database Connection")
        print("7. Exit")
        print("=" * 60)

    def display_question_list(self, questions: List[Dict]) -> None:
        """Display list of questions"""
        print("\n" + "=" * 60)
        print("Available Questions")
        print("=" * 60)

        for i, q in enumerate(questions, 1):
            difficulty_emoji = {
                "easy": "🟢",
                "medium": "🟡",
                "hard": "🔴"
            }.get(q.get("difficulty", ""), "⚪")

            topics = ", ".join(q.get("topics", []))
            print(f"{i}. {difficulty_emoji} [{q.get('difficulty', 'N/A').upper()}] {q['title']}")
            if topics:
                print(f"   Topics: {topics}")

        print("=" * 60)

    def display_question(self, question: Dict) -> None:
        """Display a question"""
        difficulty_emoji = {
            "easy": "🟢",
            "medium": "🟡",
            "hard": "🔴"
        }.get(question.get("difficulty", ""), "⚪")

        print("\n" + "=" * 60)
        print(f"{difficulty_emoji} Question #{question['id']}: {question['title']}")
        print("=" * 60)
        print(f"\nDifficulty: {question.get('difficulty', 'N/A').upper()}")

        if "topics" in question:
            print(f"Topics: {', '.join(question['topics'])}")

        print(f"\n{question['description']}")

        if "hint" in question:
            show_hint = input("\nShow hint? (y/n): ").strip().lower()
            if show_hint == 'y':
                print(f"\n💡 Hint: {question['hint']}")

        print("\n" + "-" * 60)

    def practice_question(self, question: Dict) -> None:
        """Practice a specific question"""
        self.current_question = question
        self.display_question(question)

        print("\nEnter your SQL query (type 'END' on a new line when done):")
        print("Type 'SKIP' to skip this question")
        print("Type 'SOLUTION' to see the solution")
        print("-" * 60)

        # Collect multi-line query
        query_lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            elif line.strip().upper() == 'SKIP':
                print("\nQuestion skipped.")
                return
            elif line.strip().upper() == 'SOLUTION':
                self.show_solution(question)
                return
            query_lines.append(line)

        user_query = "\n".join(query_lines).strip()

        if not user_query:
            print("\n❌ No query entered.")
            return

        # Execute user's query
        print("\n⏳ Executing your query...")
        user_result = utils.run_user_query(user_query)

        if not user_result["success"]:
            print(f"\n❌ Query Error: {user_result['error']}")
            self.stats["attempted"] += 1
            self.stats["incorrect"] += 1

            retry = input("\nTry again? (y/n): ").strip().lower()
            if retry == 'y':
                self.practice_question(question)
            return

        # Execute expected query
        print("✓ Query executed successfully!")
        print("\n📊 Your Results:")
        print(utils.format_table(user_result["results"], user_result["columns"]))

        # Get expected results
        expected_result = utils.run_user_query(question["solution"])

        if not expected_result["success"]:
            print("\n⚠️  Warning: Could not execute expected solution")
            return

        # Compare results
        comparison = utils.compare_results(
            user_result["results"],
            expected_result["results"],
            user_result["columns"],
            expected_result["columns"]
        )

        self.stats["attempted"] += 1

        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)

        if comparison["correct"]:
            print("✅ CORRECT! Your query produces the expected results!")
            self.stats["correct"] += 1
        else:
            print("❌ INCORRECT. Your results don't match the expected output.")
            self.stats["incorrect"] += 1

            if not comparison["columns_match"]:
                print(f"\n⚠️  Column mismatch:")
                print(f"   Your columns: {user_result['columns']}")
                print(f"   Expected: {expected_result['columns']}")

            if not comparison["results_match"]:
                print(f"\n⚠️  Data mismatch:")
                print(f"   Your row count: {comparison['user_row_count']}")
                print(f"   Expected row count: {comparison['expected_row_count']}")

                print("\n📊 Expected Results:")
                print(utils.format_table(expected_result["results"],
                                       expected_result["columns"]))

        print("=" * 60)

        # Ask if user wants to see the solution
        if not comparison["correct"]:
            show_solution = input("\nWould you like to see the solution? (y/n): ").strip().lower()
            if show_solution == 'y':
                self.show_solution(question)

    def show_solution(self, question: Dict) -> None:
        """Show the solution for a question"""
        print("\n" + "=" * 60)
        print("SOLUTION")
        print("=" * 60)
        print(f"\n{question['solution']}")
        print("\n" + "=" * 60)

        # Execute and show results
        result = utils.run_user_query(question["solution"])
        if result["success"]:
            print("\n📊 Expected Results:")
            print(utils.format_table(result["results"], result["columns"]))

    def browse_questions(self) -> None:
        """Browse and select questions"""
        if not self.questions:
            print("\n❌ No questions loaded. Please load questions first.")
            return

        self.display_question_list(self.questions)

        choice = input("\nEnter question number to practice (or 0 to go back): ").strip()

        try:
            idx = int(choice) - 1
            if idx == -1:
                return
            if 0 <= idx < len(self.questions):
                self.practice_question(self.questions[idx])
            else:
                print("\n❌ Invalid question number")
        except ValueError:
            print("\n❌ Please enter a valid number")

    def practice_by_difficulty(self) -> None:
        """Practice questions filtered by difficulty"""
        print("\nSelect difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("\nEnter choice (1-3): ").strip()

        difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}

        if choice not in difficulty_map:
            print("\n❌ Invalid choice")
            return

        difficulty = difficulty_map[choice]
        filtered = [q for q in self.questions if q.get("difficulty") == difficulty]

        if not filtered:
            print(f"\n❌ No {difficulty} questions found")
            return

        self.display_question_list(filtered)

        choice = input("\nEnter question number to practice (or 0 to go back): ").strip()

        try:
            idx = int(choice) - 1
            if idx == -1:
                return
            if 0 <= idx < len(filtered):
                self.practice_question(filtered[idx])
            else:
                print("\n❌ Invalid question number")
        except ValueError:
            print("\n❌ Please enter a valid number")

    def random_question(self) -> None:
        """Practice a random question"""
        if not self.questions:
            print("\n❌ No questions loaded")
            return

        import random
        question = random.choice(self.questions)
        self.practice_question(question)

    def show_statistics(self) -> None:
        """Display practice statistics"""
        print("\n" + "=" * 60)
        print("PRACTICE STATISTICS")
        print("=" * 60)
        print(f"Questions Attempted: {self.stats['attempted']}")
        print(f"Correct: {self.stats['correct']}")
        print(f"Incorrect: {self.stats['incorrect']}")

        if self.stats['attempted'] > 0:
            accuracy = (self.stats['correct'] / self.stats['attempted']) * 100
            print(f"Accuracy: {accuracy:.1f}%")

        print("=" * 60)

    def setup_database(self) -> None:
        """Setup the database with sample data"""
        print("\n⚠️  Warning: This will drop and recreate all tables!")
        confirm = input("Continue? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Database setup cancelled.")
            return

        print("\n⏳ Setting up database...")
        success = utils.setup_database()

        if success:
            print("✅ Database setup completed successfully!")
        else:
            print("❌ Database setup failed. Please check the error messages above.")

    def test_connection(self) -> None:
        """Test database connection"""
        print("\n⏳ Testing database connection...")
        success = utils.test_connection()

        if success:
            print("✅ Database connection successful!")
        else:
            print("❌ Database connection failed. Please check your configuration.")

    def run(self) -> None:
        """Main application loop"""
        print("\n" + "=" * 60)
        print("Welcome to SQL Interview Prep!")
        print("=" * 60)

        # Load questions
        print("\nLoading questions...")
        self.load_questions()

        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == "1":
                self.browse_questions()
            elif choice == "2":
                self.practice_by_difficulty()
            elif choice == "3":
                self.random_question()
            elif choice == "4":
                self.show_statistics()
            elif choice == "5":
                self.setup_database()
            elif choice == "6":
                self.test_connection()
            elif choice == "7":
                print("\n👋 Thank you for practicing! Good luck with your interviews!")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please enter 1-7.")


def main():
    """Main entry point"""
    try:
        app = SQLInterviewApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Good luck with your interviews!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
