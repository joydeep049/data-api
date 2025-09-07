# student_scores.py - fetches student scores and makes a bar chart
# just a simple script to visualize test scores

import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StudentScoreProcessor:
    # handles fetching and processing student scores
    
    def __init__(self, api_url=None):
        # using jsonplaceholder again since we don't have a real scores API
        # in real life you'd pass in the actual API endpoint
        self.api_url = api_url or "https://jsonplaceholder.typicode.com/users"
    
    def fetch_scores(self):
        """
        Fetch student scores from the API.
        """
        try:
            logger.info(f"Fetching data from {self.api_url}")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            # jsonplaceholder gives us users, so we'll fake some scores
            raw_data = response.json()
            
            students = []
            # take first 10 users and give them random scores
            for i, user in enumerate(raw_data[:10]):
                # generate random score between 60-100 (more realistic)
                score = np.random.randint(60, 101)
                student = {
                    'name': user.get('name', f'Student {i+1}'),
                    'score': score
                }
                students.append(student)
            
            logger.info(f"Successfully fetched {len(students)} student scores")
            return students
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return []
    
    def calculate_average(self, students):
        # calculate average score across all students
        if not students:
            return 0
        
        total_score = sum(student['score'] for student in students)
        average = total_score / len(students)
        logger.info(f"Average score: {average:.2f}")
        return average
    
    def create_bar_chart(self, students, average=None):
        # make a bar chart of student scores
        if not students:
            print("No student data to plot")
            return
        
        # extract names and scores
        names = [student['name'] for student in students]
        scores = [student['score'] for student in students]
        
        # create the plot
        plt.figure(figsize=(12, 6))
        bars = plt.bar(names, scores, color='skyblue', edgecolor='navy', alpha=0.7)
        
        # add average line if provided
        if average is not None:
            plt.axhline(y=average, color='red', linestyle='--', linewidth=2, 
                       label=f'Average: {average:.1f}')
            plt.legend()
        
        # customize the plot
        plt.title('Student Test Scores', fontsize=16, fontweight='bold')
        plt.xlabel('Students', fontsize=12)
        plt.ylabel('Scores', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        # add value labels on top of bars
        for bar, score in zip(bars, scores):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(score), ha='center', va='bottom', fontweight='bold')
        
        # adjust layout so labels don't get cut off
        plt.tight_layout()
        
        # save the plot
        plt.savefig('student_scores_chart.png', dpi=300, bbox_inches='tight')
        logger.info("Chart saved as 'student_scores_chart.png'")
        
        # show the plot
        plt.show()
    
    def display_summary(self, students, average):
        # print a summary of the scores
        if not students:
            print("No student data available")
            return
        
        print(f"\n{'='*50}")
        print(f"STUDENT SCORES SUMMARY")
        print(f"{'='*50}")
        print(f"Total students: {len(students)}")
        print(f"Average score: {average:.2f}")
        print(f"Highest score: {max(student['score'] for student in students)}")
        print(f"Lowest score: {min(student['score'] for student in students)}")
        print(f"\nIndividual scores:")
        
        for student in students:
            print(f"  {student['name']}: {student['score']}")
        
        print(f"{'='*50}")


def main():
    # main function - does everything
    print("Starting student scores analysis...")
    
    # create the processor
    processor = StudentScoreProcessor()
    
    # fetch student scores
    students = processor.fetch_scores()
    
    if students:
        # calculate average
        average = processor.calculate_average(students)
        
        # display summary
        processor.display_summary(students, average)
        
        # create bar chart
        processor.create_bar_chart(students, average)
        
        print("\nAnalysis complete!")
    else:
        print("No student data fetched")


if __name__ == "__main__":
    main()