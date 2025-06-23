import pandas as pd

class Session:
    def __init__(self, row):
        self.user_id = row['user_id']
        self.activity = row['activity']
        self.start = pd.to_datetime(row['start_time'])
        self.end = pd.to_datetime(row['end_time'])
        self.duration = row['duration_minutes']
        self.category = row['activity_type']
        self.location = row['location']
        self.device = row['device_used']
        self.mood = row['mood']
        self.focus = row['focus_level']
        self.interrupted = row['interrupted']
        self.day_of_week = row['day_of_week']
        self.hour_of_day = row['hour_of_day']
    
    def get_summary(self):
        return {
            "activity": self.activity,
            "category": self.category,
            "duration": self.duration,
            "focus": self.focus,
            "mood": self.mood,
            "device": self.device,
            "interrupted": self.interrupted
        }

    def __repr__(self):
        return f"<{self.activity} | {self.category} | {self.duration} mins | Mood: {self.mood} | Focus: {self.focus}>"
