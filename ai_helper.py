import os
import openai
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AIHelper:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("OpenAI API key not found. AI features will be disabled.")
    
    def is_available(self) -> bool:
        """Check if AI features are available."""
        return self.client is not None
    
    async def generate_questions(self, topic: str, question_type: str = "multiple_choice", count: int = 5) -> Optional[str]:
        """Generate questions based on topic and type."""
        if not self.is_available():
            return "❌ AI features are not available. Please configure OpenAI API key."
        
        try:
            question_types = {
                "multiple_choice": "multiple choice questions with 4 options and correct answers",
                "short_answer": "short answer questions",
                "essay": "essay questions",
                "true_false": "true/false questions with explanations"
            }
            
            question_format = question_types.get(question_type, "multiple choice questions with 4 options and correct answers")
            
            prompt = f"""
            Generate {count} educational {question_format} about {topic}.
            
            Please format the output clearly with:
            - Question numbers
            - For multiple choice: A, B, C, D options
            - Correct answers clearly marked
            - Brief explanations where helpful
            
            Make the questions appropriate for university-level students studying {topic}.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an educational content creator who generates high-quality academic questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating questions: {e}")
            return f"❌ Error generating questions: {str(e)}"
    
    async def create_notes(self, topic: str, note_type: str = "summary", detail_level: str = "medium") -> Optional[str]:
        """Generate study notes for a given topic."""
        if not self.is_available():
            return "❌ AI features are not available. Please configure OpenAI API key."
        
        try:
            note_types = {
                "summary": "concise summary with key points",
                "detailed": "comprehensive notes with explanations",
                "outline": "structured outline format",
                "flashcards": "flashcard-style key terms and definitions"
            }
            
            detail_levels = {
                "basic": "introductory level with simple explanations",
                "medium": "intermediate level with moderate detail",
                "advanced": "advanced level with complex concepts"
            }
            
            note_format = note_types.get(note_type, "concise summary with key points")
            detail_desc = detail_levels.get(detail_level, "intermediate level with moderate detail")
            
            prompt = f"""
            Create {note_format} for the topic: {topic}
            
            Level: {detail_desc}
            
            Please structure the notes with:
            - Clear headings and subheadings
            - Key concepts highlighted
            - Important definitions
            - Examples where relevant
            - Easy to study format
            
            Make it suitable for university students studying this subject.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator who creates clear, well-structured study materials."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error creating notes: {e}")
            return f"❌ Error creating notes: {str(e)}"
    
    async def explain_concept(self, concept: str, subject: str = "") -> Optional[str]:
        """Provide a detailed explanation of a concept."""
        if not self.is_available():
            return "❌ AI features are not available. Please configure OpenAI API key."
        
        try:
            subject_context = f" in {subject}" if subject else ""
            
            prompt = f"""
            Explain the concept: {concept}{subject_context}
            
            Please provide:
            - Clear definition
            - Key characteristics
            - Real-world examples
            - How it relates to other concepts
            - Why it's important to understand
            
            Make the explanation clear and educational for university students.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable tutor who explains complex concepts in simple, understandable terms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return f"❌ Error explaining concept: {str(e)}"