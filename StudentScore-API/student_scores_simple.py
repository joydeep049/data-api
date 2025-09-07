# student_scores_simple.py - fetches student scores and shows basic stats
# version without matplotlib in case it's not installed

import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StudentScoreProcessor:
    
    def __init__(self, api_url=None):
        # using jsonplaceholder again since we don't have a real scores API
        self.api_url = api_url or "https://jsonplaceholder.typicode.com/users"
    
    def fetch_scores(self):
        """
        Fetch student scores from the API.
        """
        try:
            logger.info(f"Fetching data from {self.api_url}")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()

            raw_data = response.json()
            
            students = []
            for i, user in enumerate(raw_data[:10]):
                import random
                score = random.randint(60, 100)
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
    
    def create_text_chart(self, students, average):
        # create a simple text-based chart since matplotlib might not be available
        if not students:
            print("No student data to plot")
            return
        
        print(f"\n{'='*60}")
        print("STUDENT SCORES BAR CHART (Text Version)")
        print(f"{'='*60}")
        
        max_score = max(student['score'] for student in students)
        
        for student in students:
            bar_length = int((student['score'] / max_score) * 40)  # scale to 40 chars max
            bar = '█' * bar_length
            print(f"{student['name']:<20} {bar} {student['score']}")
        
        # show average line
        avg_bar_length = int((average / max_score) * 40)
        avg_bar = '─' * avg_bar_length
        print(f"{'AVERAGE':<20} {avg_bar} {average:.1f}")
        
        print(f"{'='*60}")
    
    def display_summary(self, students, average):
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
    print("Starting student scores analysis...")
    
    processor = StudentScoreProcessor()

    students = processor.fetch_scores()
    
    if students:
        average = processor.calculate_average(students)
        
        processor.display_summary(students, average)

        processor.create_text_chart(students, average)
        
        print("\nAnalysis complete!")
        print("Note: For a visual chart, install matplotlib and run student_scores.py")
    else:
        print("No student data fetched")


if __name__ == "__main__":
    main()